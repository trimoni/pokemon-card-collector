from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

VALUE = (
  ('SUPER RARE', 'Super Rare'),
  ('RARE', 'Rare'),
  ('UNCOMMON', 'Uncommon'),
  ('COMMON', 'Common')
)

CONDITION = (
  ('Near Mint', 'Near Mint'),
  ('Lightly Played', 'Lightly Played'),
  ('Moderately Played', 'Moderately Played'),
  ('Heavily Played', 'Heavily Played'),
  ('Damaged', 'Damaged')
)

class DropOff(models.Model):
  name = models.CharField(max_length=100)
  address = models.CharField(max_length=100)
  datetime = models.DateTimeField()

  def __str__(self):
      return self.name
    
  def get_absolute_url(self):
      return reverse("dropoff_detail", kwargs={"pk": self.id})

class Card(models.Model):
  name = models.CharField(max_length=100)
  type = models.CharField(max_length=100)
  value = models.CharField(max_length=100, choices=VALUE, default='COMMON')
  pack =  models.CharField(max_length=100)
  dropoff = models.ManyToManyField(DropOff)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
      return reverse("cards_detail", kwargs={'card_id': self.id})

class Price(models.Model):
  condition = models.CharField(max_length=100, choices=CONDITION, default=CONDITION[0][0])
  money = models.IntegerField()

  card= models.ForeignKey(Card, on_delete=models.CASCADE)

  def __str__(self):
    return f"This {self.get_condition_display()} card is worth {self.money} dollars"

class Photo(models.Model):
  url = models.CharField(max_length=250)
  card = models.OneToOneField(Card, on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for card_id: {self.card_id} @{self.url}"

  
  