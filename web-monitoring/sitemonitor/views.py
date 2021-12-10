from django.db.models import Sum, Count, Max, Min, F
from django.shortcuts import render, redirect
import urllib
from django.http import HttpResponse

from rest_framework import generics, status
from rest_framework.response import Response

from .models import monitorDetails, monitorCountDetails, sslCountDetails
from performance.models import performanceCountDetails
from datetime import datetime
from django.core.mail import send_mail
from .utils import timeCalculation, getMinutesBySeconds, scheduler
from urllib.request import ssl, socket
from urllib.parse import urlparse
import json
from performance.views import PerformanceMonitor


# Create your views here.

def monitor(request):
    url = request.POST.get('selected_domain')
    email = request.POST.get('selected_email')

    if url and not email:
        monitorData = monitorDetails.objects.filter(domainName=url)
    elif email and not url:
        monitorData = monitorDetails.objects.filter(email=email)
    elif email and url:
        monitorData = monitorDetails.objects.filter(
            email=email, domainName=url)
    else:
        monitorData = monitorDetails.objects.all()

    domain_list = monitorDetails.objects.order_by().values(
        'domainName').distinct()
    email_list = monitorDetails.objects.order_by().values('email').distinct()
    context = {
        'monitorData': monitorData,
        'domain_list': domain_list,
        'email_list': email_list,
        'selected_url': url,
        'selected_email': email,
    }
    return render(request, "sitemonitor/monitor.html", context)


def addmonitor(request):
    return render(request, "sitemonitor/index.html", {})


class dashboard_performance(generics.GenericAPIView):
    def post(self, request):
        global_data = []
        monitor_record = monitorDetails.objects.filter(
            domainName=request.POST['data']).values_list('id', flat=True)
        perforamce_record = performanceCountDetails.objects.filter(
            monitor_details_id=monitor_record[0]).last()
        performance_detail = json.loads(perforamce_record.performance_data)
        if 'lighthouseResult' in performance_detail:
            if performance_detail.get('lighthouseResult').get(
                    'audits'
                    ).get('first-contentful-paint'):
                performance_dict = {}
                performance_dict.update(
                    {
                        'title': performance_detail.get(
                                'lighthouseResult').get('audits').get(
                                'first-contentful-paint').get('title'),
                        'numericValue': performance_detail.get(
                                'lighthouseResult').get('audits').get(
                                'first-contentful-paint').get(
                                'numericValue'),
                        'description': performance_detail.get(
                                'lighthouseResult').get('audits').get(
                                'first-contentful-paint').get(
                                'description'),
                        'numericUnit': performance_detail.get(
                                'lighthouseResult').get('audits').get(
                                'first-contentful-paint').get(
                                'numericUnit')
                    }
                )
                global_data.append(performance_dict)
            if performance_detail.get('lighthouseResult').get(
                    'audits'
                    ).get('speed-index'):
                    performance_dict = {}
                    performance_dict.update(
                        {
                            'title': performance_detail.get(
                                    'lighthouseResult').get('audits').get(
                                    'speed-index').get('title'),
                            'numericValue': performance_detail.get(
                                    'lighthouseResult').get('audits').get(
                                    'speed-index').get('numericValue'),
                            'description': performance_detail.get(
                                    'lighthouseResult').get('audits').get(
                                    'speed-index').get('description'),
                            'numericUnit': performance_detail.get(
                                    'lighthouseResult').get('audits').get(
                                    'speed-index').get('numericUnit')
                        }
                    )
                    global_data.append(performance_dict)
            if performance_detail.get('lighthouseResult').get(
                        'audits'
                        ).get('largest-contentful-paint'):
                    performance_dict = {}
                    performance_dict.update(
                        {
                            'title': performance_detail.get(
                                    'lighthouseResult').get('audits').get(
                                    'largest-contentful-paint').get('title'),
                            'numericValue': performance_detail.get(
                                    'lighthouseResult').get('audits').get(
                                    'largest-contentful-paint').get('numericValue'),
                            'description': performance_detail.get(
                                    'lighthouseResult').get('audits').get(
                                    'largest-contentful-paint').get('description'),
                            'numericUnit': performance_detail.get(
                                    'lighthouseResult').get('audits').get(
                                    'largest-contentful-paint').get('numericUnit')
                        }
                    )
                    global_data.append(performance_dict)
            if performance_detail.get('lighthouseResult').get(
                    'audits'
                    ).get('interactive'):
                performance_dict = {}
                performance_dict.update(
                    {
                        'title': performance_detail.get(
                                'lighthouseResult').get('audits').get(
                                'interactive').get('title'),
                        'numericValue': performance_detail.get(
                                'lighthouseResult').get('audits').get(
                                'interactive').get('numericValue'),
                        'description': performance_detail.get(
                                'lighthouseResult').get('audits').get(
                                'interactive').get('description'),
                        'numericUnit': performance_detail.get(
                                'lighthouseResult').get('audits').get(
                                'interactive').get('numericUnit')
                    }
                )
                global_data.append(performance_dict)
            if performance_detail.get('lighthouseResult').get(
                    'audits'
                    ).get('total-blocking-time'):
                performance_dict = {}
                performance_dict.update(
                    {
                        'title': performance_detail.get(
                                'lighthouseResult').get('audits').get(
                                'total-blocking-time').get('title'),
                        'numericValue': performance_detail.get(
                                'lighthouseResult').get('audits').get(
                                'total-blocking-time').get('numericValue'),
                        'description': performance_detail.get(
                                'lighthouseResult').get('audits').get(
                                'total-blocking-time').get('description'),
                        'numericUnit': performance_detail.get(
                                'lighthouseResult').get('audits').get(
                                'total-blocking-time').get('numericUnit')
                    }
                )
                global_data.append(performance_dict)
            if performance_detail.get('lighthouseResult').get(
                    'audits'
                    ).get('cumulative-layout-shift'):
                performance_dict = {}
                performance_dict.update(
                    {
                        'title': performance_detail.get(
                                'lighthouseResult').get('audits').get(
                                'cumulative-layout-shift').get('title'),
                        'numericValue': performance_detail.get(
                                'lighthouseResult').get('audits').get(
                                'cumulative-layout-shift').get('numericValue'),
                        'description': performance_detail.get(
                                'lighthouseResult').get('audits').get(
                                'cumulative-layout-shift').get('description'),
                        'numericUnit': performance_detail.get(
                                'lighthouseResult').get('audits').get(
                                'cumulative-layout-shift').get('numericUnit')
                    }
                )
                global_data.append(performance_dict)
        context = {
            'global_datas': global_data,
        }
        print("\n\n\n\n context", context)
        return HttpResponse(json.dumps(context))


class ChartDetailsViewSet(generics.GenericAPIView):

    def get(self, request):
        try:
            context = {}
            totalUpTime = 0
            totalDownTime = 0
            downTimeList = []
            upTimeList = []
            totalTimeList = []
            domain_list = []
            totalTime = 0
            id_list = monitorDetails.objects.values_list(
                'id', 'domainName').annotate(dcount=Count('domainName'))
            for idx, data in enumerate(id_list):
                domain_list.insert(idx, data[1])
                totalCountDetails = monitorCountDetails.objects.filter(
                    monitorDetailsId=data[0])
                countUpDetails = monitorCountDetails.objects.filter(
                    monitorDetailsId=data[0], type='up')
                countDownDetails = monitorCountDetails.objects.filter(
                    monitorDetailsId=data[0], type='down')
                upTime = 0
                downTime = 0
                currentData = monitorDetails.objects.get(pk=data[0])
                if totalCountDetails and (countUpDetails or countDownDetails):
                    for monitorCount in countUpDetails:
                        if monitorCount.endTime and monitorCount.startTime:
                            upTime += (
                                monitorCount.endTime - monitorCount.startTime
                            ).seconds / 60

                    for monitorCount in countDownDetails:
                        if monitorCount.endTime and monitorCount.startTime:
                            downTime += (
                                monitorCount.endTime - monitorCount.startTime
                            ).seconds / 60
                    totalTime = upTime+downTime

                totalTime += (
                        currentData.endDate - currentData.startDate
                        ).seconds / 60

                upTime += currentData.upTime / 60
                downTime += currentData.downTime / 60

                upTimeList.insert(idx, int(upTime))
                downTimeList.insert(idx, int(downTime))
                totalTimeList.insert(idx, int(totalTime))

                totalUpTime = sum(upTimeList)
                totalDownTime = sum(downTimeList)

                context = {
                    'exceptionData': domain_list,
                    'upTimeList': upTimeList,
                    'downTimeList': downTimeList,
                    'totalTimeList': totalTimeList,
                    'totalDownTime': totalDownTime,
                    'totalUpTime': totalUpTime
                }
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(
                "Error Occured.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def dashboard(request):
    # global_data = []
    totalURLs = monitorDetails.objects.order_by().values(
        'domainName').distinct().count()
    SSLURLs = monitorDetails.objects.filter(SSLEnable=True).count()
    performanceURLs = monitorDetails.objects.filter(isperfomance=True).count()
    # performance_detail = json.loads(
    #     performanceCountDetails.objects.all().last().performance_data)
    domain_list = monitorDetails.objects.filter(isperfomance=True)
    # if 'lighthouseResult' in performance_detail:
    #     if performance_detail.get('lighthouseResult').get(
    #             'audits'
    #             ).get('first-contentful-paint'):
    #         performance_dict = {}
    #         performance_dict.update(
    #             {
    #                 'title': performance_detail.get(
    #                         'lighthouseResult').get('audits').get(
    #                         'first-contentful-paint').get('title'),
    #                 'numericValue': performance_detail.get(
    #                         'lighthouseResult').get('audits').get(
    #                         'first-contentful-paint').get('numericValue'),
    #                 'description': performance_detail.get(
    #                         'lighthouseResult').get('audits').get(
    #                         'first-contentful-paint').get('description'),
    #                 'numericUnit': performance_detail.get(
    #                         'lighthouseResult').get('audits').get(
    #                         'first-contentful-paint').get('numericUnit')

    #             }
    #         )
    #         global_data.append(performance_dict)
    #     if performance_detail.get('lighthouseResult').get(
    #             'audits'
    #             ).get('speed-index'):
    #         performance_dict = {}
    #         performance_dict.update(
    #             {
    #                 'title': performance_detail.get(
    #                         'lighthouseResult').get('audits').get(
    #                         'speed-index').get('title'),
    #                 'numericValue': performance_detail.get(
    #                         'lighthouseResult').get('audits').get(
    #                         'speed-index').get('numericValue'),
    #                 'description': performance_detail.get(
    #                         'lighthouseResult').get('audits').get(
    #                         'speed-index').get('description'),
    #                 'numericUnit': performance_detail.get(
    #                         'lighthouseResult').get('audits').get(
    #                         'speed-index').get('numericUnit')
    #             }
    #         )
    #         global_data.append(performance_dict)
    #     if performance_detail.get('lighthouseResult').get(
    #             'audits'
    #             ).get('largest-contentful-paint'):
    #         performance_dict = {}
    #         performance_dict.update(
    #             {
    #                 'title': performance_detail.get(
    #                         'lighthouseResult').get('audits').get(
    #                         'largest-contentful-paint').get('title'),
    #                 'numericValue': performance_detail.get(
    #                         'lighthouseResult').get('audits').get(
    #                         'largest-contentful-paint').get('numericValue'),
    #                 'description': performance_detail.get(
    #                         'lighthouseResult').get('audits').get(
    #                         'largest-contentful-paint').get('description'),
    #                 'numericUnit': performance_detail.get(
    #                         'lighthouseResult').get('audits').get(
    #                         'largest-contentful-paint').get('numericUnit')
    #             }
    #         )
    #         global_data.append(performance_dict)
    #     if performance_detail.get('lighthouseResult').get(
    #             'audits'
    #             ).get('interactive'):
    #         performance_dict = {}
    #         performance_dict.update(
    #             {
    #                 'title': performance_detail.get(
    #                         'lighthouseResult').get('audits').get(
    #                         'interactive').get('title'),
    #                 'numericValue': performance_detail.get(
    #                         'lighthouseResult').get('audits').get(
    #                         'interactive').get('numericValue'),
    #                 'description': performance_detail.get(
    #                         'lighthouseResult').get('audits').get(
    #                         'interactive').get('description'),
    #                 'numericUnit': performance_detail.get(
    #                         'lighthouseResult').get('audits').get(
    #                         'interactive').get('numericUnit')
    #             }
    #         )
    #         global_data.append(performance_dict)
    #     if performance_detail.get('lighthouseResult').get(
    #             'audits'
    #             ).get('total-blocking-time'):
    #         performance_dict = {}
    #         performance_dict.update(
    #             {
    #                 'title': performance_detail.get(
    #                         'lighthouseResult').get('audits').get(
    #                         'total-blocking-time').get('title'),
    #                 'numericValue': performance_detail.get(
    #                         'lighthouseResult').get('audits').get(
    #                         'total-blocking-time').get('numericValue'),
    #                 'description': performance_detail.get(
    #                         'lighthouseResult').get('audits').get(
    #                         'total-blocking-time').get('description'),
    #                 'numericUnit': performance_detail.get(
    #                         'lighthouseResult').get('audits').get(
    #                         'total-blocking-time').get('numericUnit')
    #             }
    #         )
    #         global_data.append(performance_dict)
    #     if performance_detail.get('lighthouseResult').get(
    #             'audits'
    #             ).get('cumulative-layout-shift'):
    #         performance_dict = {}
    #         performance_dict.update(
    #             {
    #                 'title': performance_detail.get(
    #                         'lighthouseResult').get('audits').get(
    #                         'cumulative-layout-shift').get('title'),
    #                 'numericValue': performance_detail.get(
    #                         'lighthouseResult').get('audits').get(
    #                         'cumulative-layout-shift').get('numericValue'),
    #                 'description': performance_detail.get(
    #                         'lighthouseResult').get('audits').get(
    #                         'cumulative-layout-shift').get('description'),
    #                 'numericUnit': performance_detail.get(
    #                         'lighthouseResult').get('audits').get(
    #                         'cumulative-layout-shift').get('numericUnit')
    #             }
    #         )
    #         global_data.append(performance_dict)
    context = {
        'totalURLs': totalURLs,
        'activeURLs': totalURLs,
        'SSLURLs': SSLURLs,
        'performanceURLs': performanceURLs,
        'active_performanceURLs': performanceURLs,
        'active_SSLURLs': SSLURLs,
        # 'global_datas': global_data,
        'domain_list': domain_list
    }
    return render(request, "dashboard/dashboard.html", context)


def removemonitor(request, pk):
    monitorRecord = monitorDetails.objects.get(pk=pk)
    job_id = str(pk)
    monitorRecord.delete()
    jobs = scheduler.get_job(job_id)
    if jobs:
        scheduler.remove_job(job_id)
    if monitorRecord.SSLEnable:
        job_id = str(pk) + '_SSL'
        sslJobs = scheduler.get_job(job_id)
        if sslJobs:
            scheduler.remove_job(job_id)
    if monitorRecord.isperfomance:
        job_id = str(pk) + '_Performance'
        performanceJobs = scheduler.get_job(job_id)
        if performanceJobs:
            scheduler.remove_job(job_id)

    return redirect('/monitor')


def editmonitor(request, pk):
    monitorRecord = monitorDetails.objects.get(pk=pk)
    context = {
        'monitorData': monitorRecord,
    }
    return render(request, "sitemonitor/index.html", context)


def startmonitor(request):
    url = request.POST.get('domainName')
    interval = int(request.POST.get('interval'))
    email = request.POST.get('email')
    notificationInterval = int(request.POST.get('notificationInterval'))
    performanceEnable = request.POST.get('isperfomance')
    SSLEnable = request.POST.get('SSLEnable')
    if SSLEnable == 'on':
        SSLEnable = True
    else:
        SSLEnable = False

    if performanceEnable == 'on':
        performanceEnable = True
    else:
        performanceEnable = False

    monitorData = monitorDetails.objects.get(domainName=url)
    if monitorData and monitorData.startDate:
        monitorCount_Details = monitorCountDetails()
        monitorCount_Details.monitorDetailsId = monitorData
        monitorCount_Details.startTime = monitorData.startDate
        monitorCount_Details.endTime = monitorData.endDate
        if monitorData.upTime != 0:
            monitorCount_Details.type = 'up'
        else:
            monitorCount_Details.type = 'down'
        monitorCount_Details.save()

    if not monitorData.startDate:
        monitorData.startDate = datetime.now()
    if not monitorData.endDate:
        monitorData.endDate = datetime.now()
    monitorData.email = email
    monitorData.interval = interval
    monitorData.notificationInterval = notificationInterval
    monitorData.upTime = 0
    monitorData.downTime = 0
    monitorData.SSLEnable = SSLEnable
    monitorData.isperfomance = performanceEnable
    if SSLEnable:
        monitorData.SSLInterval = int(request.POST.get('SSLInterval'))

    if performanceEnable and request.POST.get(
            'perfomanceinterval'):
        print("\n\n\n\nDDDDDDDDD ", request.POST.get(
            'perfomanceinterval'))
        monitorData.perfomanceinterval = int(request.POST.get(
            'perfomanceinterval'))

    monitorData.save()
    job = scheduler.get_job(str(monitorData.id))
    if job:
        scheduler.reschedule_job(job.id)
    else:
        scheduler.add_job(monitoring, 'interval', seconds=interval, args=[
            url, interval, email],
                          id=str(monitorData.id))

    if SSLEnable:
        job = scheduler.get_job(str(monitorData.id) + '_SSL')
        if job:
            scheduler.reschedule_job(job.id)
        else:
            scheduler.add_job(SSLMonitoring, 'interval',
                              hours=monitorData.SSLInterval, args=[url, email],
                              id=str(monitorData.id) + '_SSL')

    if monitorData.isperfomance:
        job = scheduler.get_job(str(monitorData.id) + '_Performance')
        if job:
            scheduler.reschedule_job(job.id)
        else:
            scheduler.add_job(PerformanceMonitor, 'interval',
                              minutes=monitorData.perfomanceinterval,
                              args=[url, email],
                              id=str(monitorData.id) + '_Performance')

    return redirect('/monitor')


def monitoring(url, interval, email):
    monitorData = monitorDetails.objects.get(domainName=url)
    try:
        user_agent = 'Mozilla/5.0'
        headers = {'User-Agent': user_agent}
        request = urllib.request.Request(url=url, headers=headers)
        status_code = urllib.request.urlopen(request).getcode()
        website_is_up = status_code == 200
        monitorData.domainName = url
        if not monitorData.startDate:
            monitorData.startDate = datetime.now()
        monitorData.endDate = datetime.now()
        if website_is_up:
            monitorData.upTime += interval
        monitorData.save()
    except:
        if monitorData:
            monitorData.downTime += interval
            monitorData.domainName = url
            monitorData.interval = interval
            if not monitorData.startDate:
                monitorData.startDate = datetime.now()
            monitorData.endDate = datetime.now()
        lastNotificationTime = monitorData.lastNotificationTime
        notificationInterval = monitorData.notificationInterval

        if lastNotificationTime and monitorData.downTime != interval:
            date_time_obj = datetime.strptime(str(
                lastNotificationTime), '%Y-%m-%d %H:%M:%S.%f')
        else:
            monitorData.lastNotificationTime = datetime.now()
            date_time_obj = datetime.now()

        if monitorData.isNotification and (
                getMinutesBySeconds(
                    datetime.now().timestamp() - date_time_obj.timestamp()
                    ) > notificationInterval):
            days, hours, minutes, seconds = timeCalculation(monitorData.downTime)
            Subject = 'Error found for {}'.format(url)
            message = '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/></head><body ' \
                      'class="bg-white"><div class="d-flex flex-column flex-root"><div ' \
                      'style="font-family:Arial,Helvetica,sans-serif; line-height: 1.5; font-weight: normal; ' \
                      'font-size: 15px; color: #2F3044; ' \
                      '"><table align="left" border="0" ' \
                      'style="border-collapse:collapse;margin:0 auto; padding:0; ' \
                      '"><tbody><tr><td' \
                      '"><tr><td align="left" valign="left"><div style="text-align:left; margin: 0 ' \
                      '0; padding: 40px; background-color:#ffffff; border-radius: 6px"><div style="padding-bottom: ' \
                      '30px; font-size: 17px;"><strong>Error found for: {}</strong></div><div style="padding-bottom: ' \
                      '30px">We found {} to be down since last <strong>{} days {} hour {} minutes {} ' \
                      'seconds.</strong><br><br><br> ' \
                      '<div ' \
                      'style="padding-bottom: 10px">Kind regards,<br>Site Monitoring ' \
                      'Team.</br></div></div></td></tr></img></a></td></tr></tbody></table></div></div></body></html' \
                      '>'.format(
                url, url, days, hours, minutes, seconds)
            send_mail(
                Subject,
                message,
                'testineed@gmail.com',
                [email],
                fail_silently=False,
                html_message=message,
            )
            monitorData.lastNotificationTime = datetime.now()
        monitorData.save()


def SSLMonitoring(url, email):
    monitorData = monitorDetails.objects.get(domainName=url)
    sslDetails = sslCountDetails()
    sslDetails.monitorDetailsId = monitorData
    sslDetails.SSLCheckTime = datetime.now()

    # get only host name
    parsed_uri = urlparse(url)
    host = '{uri.netloc}'.format(uri=parsed_uri)
    try:
        context = ssl.create_default_context()
        with socket.create_connection((host, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                data = json.dumps(ssock.getpeercert())

        sslDetails.isSSL = True
        sslDetails.SSLDetails = data
        sslDetails.save()

        data = json.loads(data)
        expiryDate = data.get('notAfter')
        expiryDate = datetime.strptime(expiryDate, '%b %d %H:%M:%S %Y %Z')
        currentDateTime = datetime.now()

        if expiryDate < currentDateTime:
            Subject = 'SSL Error found for {}'.format(url)
            message = '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/></head><body ' \
                      'class="bg-white"><div class="d-flex flex-column flex-root"><div ' \
                      'style="font-family:Arial,Helvetica,sans-serif; line-height: 1.5; font-weight: normal; ' \
                      'font-size: 15px; color: #2F3044; ' \
                      '"><table align="left" border="0" ' \
                      'style="border-collapse:collapse;margin:0 auto; padding:0; ' \
                      '"><tbody><tr><td' \
                      '"><tr><td align="left" valign="left"><div style="text-align:left; margin: 0 ' \
                      '0; padding: 40px; background-color:#ffffff; border-radius: 6px"><div style="padding-bottom: ' \
                      '30px; font-size: 17px;"><strong>SSL Error found for: {}</strong></div><div ' \
                      'style="padding-bottom: ' \
                      '30px">We found {} not to be secure, SSL certificate is expired. ' \
                      '<div ' \
                      'style="padding-bottom: 10px">Kind regards,<br>Site Monitoring ' \
                      'Team.</br></div></div></td></tr></img></a></td></tr></tbody></table></div></div></body></html' \
                      '>'.format(url, url, url)
            send_mail(
                Subject,
                message,
                'testineed@gmail.com',
                [email],
                fail_silently=False,
                html_message=message,
            )

    except Exception as e:
        sslDetails.isSSL = False
        print(e)
        sslDetails.save()

        Subject = 'SSL Error found for {}'.format(url)
        message = '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/></head><body ' \
                  'class="bg-white"><div class="d-flex flex-column flex-root"><div ' \
                  'style="font-family:Arial,Helvetica,sans-serif; line-height: 1.5; font-weight: normal; ' \
                  'font-size: 15px; color: #2F3044; ' \
                  '"><table align="left" border="0" ' \
                  'style="border-collapse:collapse;margin:0 auto; padding:0; ' \
                  '"><tbody><tr><td' \
                  '"><tr><td align="left" valign="left"><div style="text-align:left; margin: 0 ' \
                  '0; padding: 40px; background-color:#ffffff; border-radius: 6px"><div style="padding-bottom: ' \
                  '30px; font-size: 17px;"><strong>SSL Error found for: {}</strong></div><div style="padding-bottom: ' \
                  '30px">We found {} not to be secure, SSL certificate verification is failed. ' \
                  '<div ' \
                  'style="padding-bottom: 10px">Kind regards,<br>Site Monitoring ' \
                  'Team.</br></div></div></td></tr></img></a></td></tr></tbody></table></div></div></body></html' \
                  '>'.format(url, url, url)
        send_mail(
            Subject,
            message,
            'testineed@gmail.com',
            [email],
            fail_silently=False,
            html_message=message,
        )
