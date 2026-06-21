from django import forms

from .models import Category, Spending
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.base_user import AbstractBaseUser

class SpendingForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, user: AbstractBaseUser = None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['category'].queryset = Category.objects.filter(user=user)

    class Meta:
        model = Spending
        exclude = ['entryDate', 'user']
        widgets = {
            "spendingDate": forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Spent on'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}),
        }

class SpendingFilterForm(forms.Form):
    start_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Start date'}))
    end_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'End date'}))
    description = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}))
    min_amount = forms.FloatField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Min amount'}))
    max_amount = forms.FloatField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Max amount'}))
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
       
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields=['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'})
        }

MONTH_CHOICES = (
    ("JANUARY", "January"),
    ("FEBRUARY", "February"),
    ("MARCH", "March"),
    ("APRIL", "April"),
    ("MAY", "May"),
    ("JUNE", "June"),
    ("JULY", "July"),
    ("AUGUST", "August"),
    ("SEPTEMBER", "September"),
    ("OCTOBER", "October"),
    ("NOVEMBER", "November"),
    ("DECEMBER", "December"),
)

class MonthlyOverviewForm(forms.Form):
    month = forms.ChoiceField(choices=MONTH_CHOICES)
    year = forms.IntegerField()

    month.widget.attrs.update({'class': 'form-control'})
    month.label = ""
    year.widget.attrs.update({'class': 'form-control', 'placeholder': 'year'})
    year.label = ""

class YearlyOverviewForm(forms.Form):
    year = forms.IntegerField()
    
    year.widget.attrs.update({'class': 'form-control', 'placeholder': 'year'})
    year.label = ""
    

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'username'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'password'
        })