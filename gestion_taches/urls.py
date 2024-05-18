from django.urls import path
from G_taches.views import Ajoute, liste_taches, modifier_tache
from G_taches.views import connexion, inscription, deconnexion, acceuil




urlpatterns = [
    path('ajoute/', Ajoute, name='ajoute'),  # URL pour la vue Ajoute
    path('liste', liste_taches, name='liste_taches'),  # URL pour la vue liste_taches
    path('modifier_tache/', modifier_tache, name='modifier_tache'),  # URL pour la vue modifier_tache

    
    path('inscription/', inscription, name='inscription'),
    path('', connexion, name='connexion'),
    
    path('deconnexion/', deconnexion, name='deconnexion'),

     path('acceuil/', acceuil, name='acceuil'),



]
