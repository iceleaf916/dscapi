from django.db import models

class UserInformation(models.Model):
    uuid = models.CharField(max_length=200)
    last_date = models.DateTimeField('Send Date', auto_now_add=True)
    ip_address = models.CharField(max_length=200)

    def __unicode__(self):
        return "%s@%s" % (self.uuid, self.ip_address)

