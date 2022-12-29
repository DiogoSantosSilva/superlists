from django.conf.urls import url
from accounts import views
from django.contrib.auth.views import logout

urlpatterns = [
    url('^send_login_email$', views.send_login_email, name="send_login_email"),
    url('^login$', views.login, name="login"),
    url('^logout$', logout, {'next_page': '/'},  name="logout"),
]
