from django import forms
from .models import Taches
from .models import Utilisateur
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserCreationForm
from datetime import date


class TachesForm(forms.ModelForm):
    class Meta:
        model = Taches
        fields = ['titre', 'date']

def clean_date(self):
        date = self.cleaned_data.get('date')
        if date < date.today():
            raise forms.ValidationError("La date ne peut pas être inférieure à la date d'aujourd'hui.")
        return date
       

       
class TachesFormModification(forms.ModelForm):
    class Meta:
        model = Taches
        fields = ['titre', 'date','statut']

        


class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(
        label="Mot de passe",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    confirm_password = forms.CharField(
        label="Confirmation du mot de passe",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )

    class Meta:
        model = Utilisateur
        fields = ('nom', 'password')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned_data

    def save(self, commit=True):
        utilisateur = super().save(commit=False)
        utilisateur.password = make_password(self.cleaned_data["password"])  # Utilisation de make_password pour hasher le mot de passe
        if commit:
            utilisateur.save()
        return utilisateur