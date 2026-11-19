from django.urls import path
from . import views

app_name = "immobilier"

urlpatterns = [
    path("biens/", views.liste_biens, name="liste_biens"),
    path("biens/<int:pk>/", views.detail_bien, name="detail_bien"),

    path("acheteurs/", views.liste_acheteurs, name="liste_acheteurs"),
    path("acheteurs/<int:pk>/", views.detail_acheteur, name="detail_acheteur"),

    path("vendeurs/", views.liste_vendeurs, name="liste_vendeurs"),
    path("vendeurs/<int:pk>/", views.detail_vendeur, name="detail_vendeur"),

    path("agents/", views.liste_agents, name="liste_agents"),
    path("agents/<int:pk>/", views.detail_agent, name="detail_agent"),
]