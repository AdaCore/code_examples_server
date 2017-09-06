"""compile_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from rest_framework import routers

from compile_server.app import views, checker

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),

    # Check one program
    url(r'^check_program/', checker.check_program),

    # Get a list of the examples
    url(r'^examples/', views.examples),

    # Get the details on one example
    url(r'^example/([^\/]+)$', views.example),

    # HTML urls

    # Get the code viewer on one example
    url(r'^code_page/([^\/]+)$', views.code_page),

    # Get a list of all the examples
    url(r'^examples_list/', views.examples_list),

    # The landing page
    url(r'', views.examples_list),
]
