from django.db import models
from sitemonitor.models import monitorDetails


# Create your models here.
class performanceCountDetails(models.Model):
    is_performance = models.BooleanField(default=True)
    monitor_details_id = models.ForeignKey(monitorDetails, on_delete=models.CASCADE)
    performance_checktime = models.DateTimeField(blank=True, null=True)
    performance_data = models.TextField()
