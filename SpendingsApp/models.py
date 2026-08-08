

from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='categories')

    def __str__(self) -> str:
        return self.name

class Spending(models.Model):
    entryDate = models.DateTimeField(auto_now_add=True)
    spendingDate = models.DateField()
    description = models.CharField(max_length=100)
    amount = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='spendings')

    def __str__(self) -> str:
        date = self.spendingDate.strftime('%d.%m.%y')
        return f'{date}: {self.description} {self.amount}'
