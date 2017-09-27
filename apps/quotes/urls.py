from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'process$', views.process),
    url(r'success$', views.success),
    url(r'login$', views.login),
    url(r'add_quote$', views.add_quote),
    url(r'user/(?P<user_id>\d+)$', views.user),
    url(r'favorite/(?P<quote_id>\d+)$', views.favorite),
    url(r'remove/(?P<quote_id>\d+)$', views.remove),
    url(r'logout$', views.logout),

]
