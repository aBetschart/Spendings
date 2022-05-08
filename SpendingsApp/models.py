from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name

class Spending(models.Model):
    entryDate = models.DateTimeField(auto_now_add=True)
    spendingDate = models.DateField()
    description = models.CharField(max_length=100)
    amount = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
