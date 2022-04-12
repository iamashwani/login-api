import traceback

from django.conf import settings
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import ugettext_lazy as _

from rest_framework import exceptions, serializers, status
from rest_framework.exceptions import ValidationError as RestFrameworkValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler
from sentry_sdk import capture_exception, configure_scope

from apps.metronom_commons.logging import logger
from apps.users.mixins import MeURLMixin


class ObjectValidationError(RestFrameworkValidationError):
    """
        The ObjectValidationError received an identifier of the Object. It can be used to give an
        error on a specific object (you can use the uuid or the position)
    """

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Invalid object input.")
    default_code = "object invalid"

    def __init__(self, detail=None, code=None, identifier=None):
        super(ObjectValidationError, self).__init__(detail, code)

        if identifier is not None:

            self.detail = {str(identifier): self.detail}


def core_exception_handler(exc, context):
    """
        For some errors we have special handlers for explicit handling. If an exception is thrown that we don't
        explicitly handle here, we want to delegate to the default exception handler offered by DRF - we just have
        a little cleanup then.
        All errors will be sent to the Frontend with the following format:
        {
            "errors": {
                "__all__": [
                    "I am general error not specific for one special field"
                ],
                "name": [
                    "I am error for a given field"
                ]
                "activity_steps": [
                    {
                        "start_date": [
                            "I am a nested error within the given activity steps"
                        ],
                        "step": {
                            "uuid": {
                                "098bd5a5-137b-49f3-87e3-9cbf240fe0d7": [
                                    "I am an error for that specific object."
                                ]
                            }
                        }
                    },
                ],
            },
            "status_code": 400  // We still send the HTTP Status code so this is redundant
        }
        When API_LOGGING=True, we also send some debugging information s
            "debugging_information": {
                "exception_class": "ValidationError",  // the thrown Exception class
                "exception_raw_message": "{'name': 'No name with this'",  // the raw and not yet formatted error
                // the URL context (e.g. /api/projects/<project_pk>/)
                "url_context": {
                    "project_pk": "6c415171-d07d-4b3b-92af-a93b88c39164"
                },
                "received_context": {                                     // the full received POST context
                    "name": "test",
                    ....
                }
            }
    """
    if settings.PRINT_TRACEBACK_TO_CONSOLE:
        traceback.print_exc()
    response = exception_handler(exc, context)
    handlers = {
        "NotFound": _handle_not_found_error,
        "Http404": _handle_not_found_error,
        "ValidationError": _handle_validation_error,
        "ImproperlyConfigured": _handle_improperly_configured_error,
        "NotAuthenticated": _handle_not_authenticated,
    }

    # Lets dentify the type of the current exception to check if we should handle it
    exception_class = exc.__class__.__name__

    # This is the error given, if all things go wrong
    response_data_default = {"errors": _("Could not process this request because of an internal error")}

    # Some errors do not give an Response. We need to handle this case as well
    if response is None:
        response = Response(
            data=response_data_default, content_type="application/json", status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # If this exception is one that we can handle, handle it.
    if exception_class in handlers:
        logger.debug(f"Exception class {exception_class} ({exc.__class__}) found - using handler.")

        try:
            return handlers[exception_class](exc, context, response)
        except Exception:
            pass

    if hasattr(context["request"], "user") and hasattr(context["request"].user, "email"):
        with configure_scope() as scope:
            scope.user = {"email": context["request"].user.email}
    capture_exception(exc)

    return _handle_generic_error(exc, context, response)


def _handle_generic_error(exc, context, response):
    """
        The generic error handling is used both as a fallback and for all other handlers.
        We take the response generated by DRF and wrap it in the `errors` key.
    """
    import traceback

    if "errors" not in response.data:

        response.data = {"errors": response.data}

    response.data.update({"status_code": response.status_code})
    response.data.update(
        {
            "debugging_information": {
                "exception_class": exc.__class__.__name__,
                "exception_raw_message": str(exc),
                "url_context": dict(context["kwargs"], **context["request"].query_params.dict()),
                "received_context": context["request"].data,
            }
        }
    )

    if settings.DEBUG is True:

        response.data.update({"traceback": traceback.format_exception(exc.__class__, exc, exc.__traceback__)})

    headers = {}

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, "auth_header", None):
            headers["WWW-Authenticate"] = exc.auth_header
        if getattr(exc, "wait", None):
            headers["Retry-After"] = "%d" % exc.wait

    return Response(response.data, status=response.status_code, headers=headers)


def _handle_validation_error(exc, context, response):
    """
        Handling of an Validation Error. We need to take care, that there are three types of Validation Errors
        1. DjangoValidationError (happening at the Model level, does not provide an HTTP response
        2. RestFrameworkValidationError (pimped up version by drf)
        3. ObjectValidationError (object-level Validation error)
    """

    response.status_code = status.HTTP_400_BAD_REQUEST

    if hasattr(response, "data"):
        response.data = {"errors": response.data}

    if isinstance(exc, DjangoValidationError):
        if "__all__" in dict(exc):
            response.data = {"errors": dict(exc)}
        else:
            response.data = {"errors": dict(exc)}

    if isinstance(exc, RestFrameworkValidationError):

        error_dict = serializers.as_serializer_error(exc)

        if "error" in error_dict:
            error_dict["__all__"] = error_dict.pop("error")

            response.data = {"errors": error_dict}

    logger.warning("STarting general handling !!!!!")

    return _handle_generic_error(exc, context, response)


def _handle_improperly_configured_error(exc, context, response):
    """
        Handling of an Validation Error
        Could be from the Model:
            {'__all__': ['Contract start/end dates overlap with another Contract.']}
    """

    response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

    response.data = {"errors": {"__all__": str(exc)}}

    return _handle_generic_error(exc, context, response)


def _handle_not_authenticated(exc, context, response):
    response.data = {"errors": {"Not authenticated": "Use your login and password to log in"}}
    return _handle_generic_error(exc, context, response)


def _handle_not_found_error(exc, context, response):

    view = context.get("view", None)

    pk_message = ""

    if "kwargs" in context and "user_pk" in context["kwargs"]:
        pk_message = f"for '{context['kwargs']['user_pk']}'"
    elif "kwargs" in context and "pk" in context["kwargs"]:
        pk_message = f"for '{context['kwargs']['pk']}'"

    error_message = f"No objects found."

    if issubclass(view.__class__, MeURLMixin):
        # Lets have a little nicer message for the Users

        if pk_message:
            error_message = f"No user found {pk_message}. You must use 'me' or an (correct) 'uuid'"
        else:
            error_message = f"No users found"

    else:

        if pk_message:
            error_message = f"No object found {pk_message}. You must use an (correct) 'uuid'"

    response.data = {"errors": {"Not found": error_message}}

    return _handle_generic_error(exc, context, response)