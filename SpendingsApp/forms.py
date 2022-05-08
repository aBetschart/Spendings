from django import forms
from .models import Category, Spending

class EnterSpendingForm(forms.ModelForm):
    spendingDate = forms.DateField(input_formats=["%d/%m/%y"], label="Spent on")
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