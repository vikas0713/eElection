"""
URL configuration for eElection project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from election import views as election_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("dashboard", election_views.dashboard, name="dashboard"),
    path("details/<int:state_id>", election_views.state_details, name="state_details"),
    path("confirm-identity/<int:election_id>", election_views.confirm_identity, name="confirm_identity"),
    path("validate-identity/<int:election_id>", election_views.validate_identity, name="validate_identity"),
    path("cast-vote/", election_views.cast_vote, name="cast_vote"),


]
