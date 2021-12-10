"""monitoring URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
import sitemonitor.urls
import performance.urls
import monitoring_server.urls

urlpatterns = [
    path('monitor/', include(sitemonitor.urls, namespace="monitor")),
    path('performance/', include(performance.urls, namespace="performance")),
    path('api/client/', include(monitoring_server.urls, namespace="monitoring_server")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
