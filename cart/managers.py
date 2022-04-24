from django.db import models
from django.db.models import QuerySet
from django.utils import timezone


# from UserBio.models import UserProfile
# from django.contrib.auth import get_user_model
# User = get_user_model()


class SoftDeletionQuerySet(QuerySet):
    def delete(self):
        # import pdb
        # pdb.set_trace()
        return super(SoftDeletionQuerySet, self).update(deleted_on=timezone.now())

    def hard_delete(self):
        # import pdb
        # pdb.set_trace()
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        return self.filter(deleted_on=None)

    def dead(self):
        return self.exclude(deleted_on=None)

    # def delete(self):
    #     import pdb
    #     pdb.set_trace()
    #     """Delete the records in the current QuerySet."""
    #     assert self.query.can_filter(), \
    #         "Cannot use 'limit' or 'offset' with delete."
    #
    #     if self._fields is not None:
    #         raise TypeError("Cannot call delete() after .values() or .values_list()")
    #
    #     del_query = self._chain()
    #
    #     # The delete is actually 2 queries - one to find related objects,
    #     # and one to delete. Make sure that the discovery of related
    #     # objects is performed on the same database as the deletion.
    #     del_query._for_write = True
    #
    #     # Disable non-supported fields.
    #     del_query.query.select_for_update = False
    #     del_query.query.select_related = False
    #     del_query.query.clear_ordering(force_empty=True)
    #
    #     collector = Collector(using=del_query.db)
    #     collector.collect(del_query)
    #     deleted, _rows_count = collector.delete()
    #
    #     # Clear the result cache, in case this QuerySet gets reused.
    #     self._result_cache = None
    #     return deleted, _rows_count


class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(deleted_on=None)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()
