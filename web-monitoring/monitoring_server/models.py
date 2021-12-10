from django.db import models


# Create your models here.
class exceptionDetails(models.Model):
    Request_URL = models.CharField(max_length=200, blank=False, null=False, verbose_name="Request URL",
                                   db_column="serverUrl")
    Exception_Location = models.TextField(db_column="exceptionLocation")
    Server_time = models.DateTimeField(blank=True, null=True, db_column="exceptionTime")
    Exception_Type = models.CharField(max_length=200, blank=False, null=False, db_column="errorType")
