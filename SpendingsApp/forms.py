from django import forms
from .models import Category, Spending


class SpendingForm(forms.ModelForm):
    class Meta:
        model = Spending
        exclude = ['entryDate']
        widgets = {
            "spendingDate": forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Spent on'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
       
class CategoryForm(forms.ModelForm):
    class Meta:
        fields="__all__"
        model = Category

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
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
    