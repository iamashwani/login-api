from django.db import models
import uuid
from cart.models import User
# Create your models here.
status = (
    ("PENDING", "Pending"),
    ("CLOSED", "Closed"),
)

def create_ticket_id():
    return str(uuid.uuid4()).split("-")[-1]

class Ticket(models.Model):
    ticket_id = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    status1 = models.CharField(choices=status, max_length=155, default='pending')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    # Magic method to return format
    def __str__(self):
        return "{} = {}".format(self.title, self.ticket_id)

    def save(self, *args, **kwargs):
        if len(self.ticket_id.strip(" "))==0:
            self.ticket_id = create_ticket_id()

        super(Ticket, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-created_date"]