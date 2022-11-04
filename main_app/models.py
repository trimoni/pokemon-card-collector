from django.db import models
from django.urls import reverse

# Create your models here.

VALUE = (
  ('SUPER RARE', 'Super Rare'),
  ('RARE', 'Rare'),
  ('UNCOMMON', 'Uncommon'),
  ('COMMON', 'Common')
)

class Card(models.Model):
  name = models.CharField(max_length=100)
  type = models.CharField(max_length=100)
  value = models.CharField(max_length=100, choices=VALUE, default='COMMON')
  pack =  models.CharField(max_length=100)

  def __str__(self):
    return self.name

def get_absolute_url(self):
    return reverse("cards_detail", kwargs={'card_id': self.id})
