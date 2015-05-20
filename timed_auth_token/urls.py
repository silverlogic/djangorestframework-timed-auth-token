from django.conf.urls import url

from .views import TimedAuthTokenCreateView


urlpatterns = [
    url(r'^login/', TimedAuthTokenCreateView.as_view(), name='login')
]
