from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)

class Spending(models.Model):
    description = models.CharField(max_length=100)
    amount = models.FloatField()
    spendingDate = models.DateField()
    entryDate = models.DateTimeField(auto_now_add=True)

class SpendingCategories(models.Model):
    spending = models.OneToOneField(Spending, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)