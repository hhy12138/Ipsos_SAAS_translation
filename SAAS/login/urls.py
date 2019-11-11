from django.conf.urls import url

from login import views

urlpatterns = [
    url(r'^forgetpassword',views.forgetpassword),
    url(r'^changepassword',views.changepassword),
    url(r'',views.login),
]