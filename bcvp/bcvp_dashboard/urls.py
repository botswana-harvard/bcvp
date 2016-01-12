from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .classes import SubjectDashboard

urlpatterns = []

for pattern in SubjectDashboard.get_urlpatterns():
    urlpatterns.append(
        url(pattern,
            login_required(SubjectDashboard.as_view()),
            name=SubjectDashboard.dashboard_url_name))
