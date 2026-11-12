from django.urls import path
from . import views

app_name = "immobilier"

urlpatterns = [
    path("", views.liste_biens, name="liste_biens"),
    path("<int:pk>/", views.detail_bien, name="detail_bien"),
]