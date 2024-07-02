from django import forms
from .models import Category, Spending


class EnterSpendingForm(forms.ModelForm):
    spendingDate = forms.DateField(input_formats=["%d.%m.%y"], label="Spent on")
    class Meta:
        model = Spending
        exclude = ['entryDate']
        widgets = {
            "spendingDate": forms.DateInput(format=("%d/%m/%y"))
        }
       
class NewCategoryForm(forms.ModelForm):
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
    month = forms.ChoiceField(choices=MONTH_CHOICES, initial="JULY")
    year = forms.IntegerField(initial=2024)