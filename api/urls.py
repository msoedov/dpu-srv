from django.conf.urls import url

from api import views

urlpatterns = [
    # ...
    url(r"events/(?P<spc>[^/]+)$$", views.EventsView.as_view()),
]
