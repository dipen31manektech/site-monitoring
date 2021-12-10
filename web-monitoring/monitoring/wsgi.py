"""
WSGI config for monitoring project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

from sitemonitor.models import monitorDetails, monitorCountDetails
from sitemonitor.views import monitoring, SSLMonitoring
from performance.views import PerformanceMonitor
from datetime import datetime
# import mtmonitor
from sitemonitor.utils import scheduler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monitoring.settings')

# When application starts need to auto start the existing monitoring domain.
# mtmonitor.initError()
monitorData = monitorDetails.objects.all()

for data in monitorData:
    monitorCount_Details = monitorCountDetails()
    monitorCount_Details.monitorDetailsId = data
    monitorCount_Details.startTime = data.startDate
    monitorCount_Details.endTime = data.endDate
    if data.upTime != 0:
        monitorCount_Details.type = 'up'
    else:
        monitorCount_Details.type = 'down'
    monitorCount_Details.save()

    # Reset te monitor details for next monitoring.
    data.startDate = datetime.now()
    data.endDate = datetime.now()
    data.upTime = 0
    data.downTime = 0
    data.save()
    job_id = str(data.id)

    scheduler.add_job(monitoring, 'interval', seconds=data.interval, args=[data.domainName, data.interval, data.email],
                      id=job_id)

    if data.SSLEnable:
        job_id = job_id + '_SSL'
        scheduler.add_job(SSLMonitoring, 'interval', hours=data.SSLInterval, args=[data.domainName, data.email],
                          id=job_id)

    if data.isperfomance:
        job_id = job_id + '_Performance'
        scheduler.add_job(PerformanceMonitor, 'interval', hours=data.perfomanceinterval,
                          args=[data.domainName, data.email], id=job_id)

application = get_wsgi_application()
