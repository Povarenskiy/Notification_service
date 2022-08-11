from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from mailing_app.views import MailingView, ClientView, MessageView

router = routers.DefaultRouter()

router.register('mailing', MailingView)
router.register('client', ClientView)
router.register('message', MessageView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls))
    ]