"""BoschMCM_API URL Configuration

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
from django.contrib import admin
from django.urls import path
from Webapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/ReadDeviceSettings', views.ReadDeviceSettings().as_view()),
    path('api/changetcpip', views.ConfigIpChange().as_view()),
    path('api/changeedgedeviceproperties', views.ConfigGatewayProperties().as_view()),
    path('api/starttcp', views.StartTcpService().as_view()),
    path('api/stoptcp', views.StopTcpService().as_view()),
    path('api/startppmp', views.StartPpmpService().as_view()),
    path('api/stopppmp', views.StopPpmpService().as_view()),
    path('api/startrtu', views.StartRtuService().as_view()),
    path('api/stoprtu', views.StopRtuService().as_view()),
    # path('api/doLogin', LoginView.LoginViewAPI.as_view())
]
