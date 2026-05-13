from django import forms
from .models import Review, Order

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Votre avis...'
            }),
        }
        labels = {
            'rating': 'Note',
            'comment': 'Commentaire',
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address', 'phone']
        widgets = {
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Votre adresse de livraison...'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+212 6 00 00 00 00'
            }),
        }
        labels = {
            'address': 'Adresse de livraison',
            'phone': 'Numéro de téléphone',
        }