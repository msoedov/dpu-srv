from django.conf.urls import url
from api import views


urlpatterns = [
    # ...
    url(r"^magic/(?P<mission_id>[^/]+)$", views.VectorView.as_view()),
    url(r"^magic/$", views.VectorView.as_view()),
    url(r"^magic/(?P<pk>[^/]+)$", views.ReadVectorView.as_view()),
]
