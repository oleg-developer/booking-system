from django.conf.urls import url

from apps.dashboard.views import email_confirm, recover_password

urlpatterns = [
    url(r'^email_confirm/(?P<user>\d+)/(?P<token>.*)', email_confirm,
        name='email_confirm'),
    url(r'^recover_password/(?P<user>\d+)/(?P<token>.*)', recover_password,
        name='recover_password')
]
