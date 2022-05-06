from django.db import models

class Category(models.Model):
    name: models.CharField(max_length=50)

class Spending(models.Model):
    description: models.CharField(max_length=100)
    amount: models.FloatField()
    spendingDate: models.DateTimeField()
    entryDate: models.DateTimeField()

class SpendingCategories(models.Model):
    spending: models.ForeignKey(Spending, on_delete=models.CASCADE, unique=True)
    category: models.ForeignKey(Category, on_delete=models.CASCADE)