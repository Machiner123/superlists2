from django.conf.urls import url
from accounts import views
from django.contrib.auth.views import logout


urlpatterns = [
    url(r'^login$', views.persona_login, name='persona_login'),
    url(r'^logour$', logout, {'next_page': '/'}, name='logout'),
]
