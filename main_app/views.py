from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Card

# Create your views here.

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def cards_index(request):
  cards = Card.objects.all()
  return render(request, 'cards/index.html', { 'cards': cards })

def cards_detail(request, card_id):
  card = Card.objects.get(id=card_id)
  return render(request, 'cards/detail.html', { 'card': card })

class CardCreate(CreateView):
  model = Card
  fields = '__all__'

class CardUpdate(UpdateView):
  model = Card
  fields = ['type', 'value', 'pack']

class CardDelete(DeleteView):
  model = Card
  success_url = '/cards/'