from django import forms
from django.forms import ModelForm
from .models import Vehicle

#create a Vehicle form
class VehicleForm(ModelForm):
    class Meta:
        model = Vehicle
        fields = ('CarID', 'year', 'make', 'model', 'miles', 'color', 'location', 'status')
        labels={
            'CarID': '',
            'year': '',
            'make': '',
            'model': '',
            'miles': '',
            'color': '',
            'location': '',
        }

        widgets={
            'CarID': forms.TextInput(attrs={'class':'form-control', 'placeholder':'CarID'}),
            'year': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Year'}),
            'make': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Make'}),
            'model': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Model'}),
            'miles': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Miles'}),
            'color': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Color'}),
            'location': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Location'}),
        }