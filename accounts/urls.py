from django.conf.urls import url, include

from accounts.views import send_login_email, login, logout


urlpatterns = [
    url(r'^send_login_email$', send_login_email, name='send_login_email'),
    url(r'^login', login, name='login'),
    url(r'^logout$', logout, name='logout'),
]
