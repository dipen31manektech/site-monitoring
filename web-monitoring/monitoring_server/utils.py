from django.core.handlers.wsgi import WSGIHandler
from bs4 import BeautifulSoup
import requests
from datetime import datetime


def initError():
    WSGIHandler.__call__ = errorHandling


def errorHandling(self, environ, start_response):
    request = self.request_class(environ)
    response = self.get_response(request)
    status = '%d %s' % (response.status_code, response.reason_phrase)
    response_headers = [
        *response.items(),
        *(('Set-Cookie', c.output(header='')) for c in response.cookies.values()),
    ]
    start_response(status, response_headers)
    if response.status_code >= 400:
        try:
            exceptionDetails = {}
            soup = BeautifulSoup(response.content, "html")
            gdp_table = soup.find("table", attrs={"class": "meta"})
            gdp_table_data = gdp_table.find_all("tr")
            for tableData in gdp_table_data:
                key = tableData.th.text.strip(":").replace(" ", "_")
                if "Server_time" != key:
                    exceptionDetails[key] = tableData.td.text
                else:
                    date = tableData.td.text
                    date_time_obj = datetime.strptime(str(date), '%a, %d %b %Y %H:%M:%S %z')
                    exceptionDetails[key] = date_time_obj
            url = "http://127.0.0.1:8000/api/client/create-exception/"
            requests.post(url, data=exceptionDetails)
        except Exception as e:
            print("Internal Error: {}".format(e))
    return response
