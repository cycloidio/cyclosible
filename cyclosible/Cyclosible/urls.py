"""Cyclosible URL Configuration
"""
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.authtoken import views as authtoken_views
from .views import (GroupViewSet, UserViewSet)
from .routers import main_router
from cyclosible.playbook import urls as playbook_urls
assert playbook_urls

main_router.register(r'groups', GroupViewSet)
main_router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/', include(main_router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', authtoken_views.obtain_auth_token),
    url(r'^docs/', include('rest_framework_swagger.urls')),
]
