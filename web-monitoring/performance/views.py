from django.shortcuts import render
from sitemonitor.models import monitorDetails
from . models import performanceCountDetails
from datetime import datetime
import requests

# Create your views here.
key = 'AIzaSyBwGhLAa1rpoqGnvekPgVggCigvk-tIBzY'


def performance(request):
    return render(request, "performance/performance.html", {})


def PerformanceMonitor(url, email):
    monitorData = monitorDetails.objects.get(domainName=url)
    perf_cnt_details = performanceCountDetails()
    perf_cnt_details.monitor_details_id = monitorData
    perf_cnt_details.performance_checktime = datetime.now()
    try:
        url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=%s&key=%s" % (url, key)
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        perf_cnt_details.is_performance = True
        perf_cnt_details.performance_data = response.text
        perf_cnt_details.save()
    except Exception as e:
        perf_cnt_details.is_performance = False
        perf_cnt_details.save()
