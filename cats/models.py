from django.contrib.auth import get_user_model
from django.db import models

from .choices import BREED_CHOICES, HAIRINESS_CHOICES

User = get_user_model()

class Cat(models.Model):
    name = models.CharField(max_length=35)
    breeder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cats', default=User)
    breed = models.CharField(max_length=40, choices=BREED_CHOICES, default='Абиссинская')
    age = models.PositiveBigIntegerField(null=False, blank=False, default=1)
    hairiness = models.CharField(max_length=20, choices=HAIRINESS_CHOICES, default='Безволосая')

    def __str__(self):
        return f"({self.id}) {self.name}"


    class Meta:
        verbose_name = 'Кот'
        verbose_name_plural = 'Коты'
