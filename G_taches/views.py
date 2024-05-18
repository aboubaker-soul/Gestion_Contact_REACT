from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Utilisateur
from .forms import TachesForm
from .models import Taches
from .forms import TachesFormModification
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm 
from .forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.urls import reverse



def custom_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        utilisateur_id = request.session.get('utilisateur_id')
        if utilisateur_id is None:
            # Utilisateur non connecté, rediriger vers la page de connexion
            return redirect(reverse('connexion'))
        return view_func(request, *args, **kwargs)
    return wrapper

    



def acceuil(request):
    return render(request, 'acceuil.html')



from datetime import date

def Ajoute(request):
    if request.method == 'POST':
        form = TachesForm(request.POST)
        if form.is_valid():
            # Vérification de la date
            date_input = form.cleaned_data.get('date')
            if date_input < date.today():
                form.add_error('date', "La date ne peut pas être inférieure à la date d'aujourd'hui.")
            else:
                # Récupérer l'ID de l'utilisateur connecté depuis la session
                utilisateur_id = request.session.get('utilisateur_id')
                
                # Assurez-vous que l'ID de l'utilisateur est présent dans la session
                if utilisateur_id:
                    # Enregistrez l'utilisateur connecté comme créateur de la tâche
                    form.instance.utilisateur_id = utilisateur_id
                    
                    # Enregistrez la tâche
                    form.save()
                    
                    # Redirigez l'utilisateur vers une autre vue ou une autre page après avoir ajouté la tâche
                    return redirect('liste_taches')
                else:
                    # Gérer le cas où l'ID de l'utilisateur n'est pas présent dans la session
                    messages.error(request, "Veuillez vous connecter pour ajouter une tâche.")
    else:
        form = TachesForm()
    
    return render(request, 'ajout.html', {'form': form})






#def liste_utilisateurs(request):
 # utilisateurs = Utilisateur.objects.all()
  #  return render(request, 'liste_utilisateurs.html', {'utilisateurs': utilisateurs})
@custom_login_required
def liste_taches(request):
    # Récupérer l'ID de l'utilisateur connecté
    utilisateur_id = request.session.get('utilisateur_id')
    
    # S'assurer que l'ID de l'utilisateur est présent dans la session
    if utilisateur_id:
        # Filtrer les tâches en fonction de l'utilisateur connecté
        taches = Taches.objects.filter(utilisateur_id=utilisateur_id)
        return render(request, 'index.html', {'taches': taches})
    else:
        # Gérer le cas où l'ID de l'utilisateur n'est pas présent dans la session
        messages.error(request, "Veuillez vous connecter pour voir vos tâches.")
        return redirect('connexion')

@custom_login_required
def modifier_tache(request):
    if request.method == 'POST':
        tache_id = request.POST.get('tache_id')
        tache = get_object_or_404(Taches, id_taches=tache_id)
        if tache:
            form = TachesFormModification(request.POST, instance=tache)
        else:
            form = TachesFormInsertion(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_taches')
        else:
            print("Le formulaire est invalide :", form.errors)  # Débogage
    else:
        print("La méthode de la requête n'est pas POST.")  # Débogage
    return redirect('liste_taches')  # Redirection par défaut


def inscription(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            if password != confirm_password:
                # Gérer l'erreur si les mots de passe ne correspondent pas
                # Dans cet exemple, je renvoie simplement à la même page avec un message d'erreur
                return render(request, 'inscription.html', {'form': form, 'error_message': "Les mots de passe ne correspondent pas."})
            else:
                # Création de l'utilisateur si les mots de passe correspondent
                user = form.save()
                return redirect('connexion')
    else:
        form = CustomUserCreationForm()
    return render(request, 'inscription.html', {'form': form})

    



def connexion(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        password = request.POST.get('password')
        
        print("Nom d'utilisateur reçu:", nom)  # Débogage
        print("Mot de passe reçu:", password)  # Débogage
        
        # Récupérez l'utilisateur depuis la base de données
        try:
            utilisateur = Utilisateur.objects.get(nom=nom)
            print("Utilisateur trouvé:", utilisateur)
        except Utilisateur.DoesNotExist:
            utilisateur = None
            print("Utilisateur non trouvé.")
        
        # Vérifiez si l'utilisateur existe et si le mot de passe est correct
        if utilisateur is not None and check_password(password, utilisateur.password):
            # Connexion de l'utilisateur
            request.session['utilisateur_id'] = utilisateur.id_utilisateur  # Utilisez id_utilisateur
            return redirect('liste_taches')
        else:
            # Affichage d'un message d'erreur si l'authentification a échoué
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    
    # Rendu de la page de connexion
    return render(request, 'connexion.html')




def deconnexion(request):
    logout(request)
    messages.success(request, "Vous êtes maintenant déconnecté.")
    return redirect('connexion')


