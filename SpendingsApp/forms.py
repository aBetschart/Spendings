from django import forms
from .models import Category, Spending


class SpendingForm(forms.ModelForm):
    spendingDate = forms.DateField(label="Spent on")
    class Meta:
        model = Spending
        exclude = ['entryDate']
        widgets = {
            "spendingDate": forms.DateInput()
        }
       
class CategoryForm(forms.ModelForm):
    class Meta:
        fields="__all__"
        model = Category

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

class MonthlySpendingOverview(forms.Form):
    month = forms.ChoiceField(choices=MONTH_CHOICES)
    year = forms.IntegerField()
    