from django.shortcuts import render

# Create your views here.

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

class Card:
  def __init__(self, name, type, value, pack):
    self.name = name
    self.type = type
    self.value = value
    self.pack = pack

cards = [
  Card('Pikachu', 'Electric', 'Common', 'Jungle Pack'),
  Card('Charizard', 'Fire', 'Super Rare', 'Base Pack'),
  Card('Mewtwo', 'Psychic', 'Super Rare', 'Base Pack'),
  Card('Snorlax', 'Normal', 'Rare', 'Jungle Pack')
]

def cards_index(request):
  return render(request, 'cards/index.html', { 'cards': cards })