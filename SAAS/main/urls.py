from django.conf.urls import url

from main import views

urlpatterns = [
    url(r'^test/',views.test),
    url(r'^change_time/',views.change_time),
    url(r'^upload/',views.upload),
    url(r'^translate/',views.translate),
    url(r'^download/',views.download),
    url(r'',views.main),
]