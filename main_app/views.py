from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Card, DropOff
from .forms import PriceForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def home(request):
  template_name = 'home.html'

def about(request):
  return render(request, 'about.html')

def cards_index(request):
  cards = Card.objects.all()
  return render(request, 'cards/index.html', { 'cards': cards })

def cards_detail(request, card_id):
  card = Card.objects.get(id=card_id)
  dropoff_card_doesnt_have = DropOff.objects.exclude(id__in = card.dropoff.all().values_list('id'))
  price_form = PriceForm()
  return render(request, 'cards/detail.html', { 'card': card, 'price_form': price_form, 'dropoff': dropoff_card_doesnt_have })

class CardCreate(CreateView):
  model = Card
  fields = ['name', 'type', 'value', 'pack']

  def form_valid(self, form):
    form.instance.user = self.requesr.user
    return super().form_valid(form)

class CardUpdate(UpdateView):
  model = Card
  fields = ['type', 'value', 'pack']

class CardDelete(DeleteView):
  model = Card
  success_url = '/cards/'

def add_price(request, card_id):
  form = PriceForm(request.POST)
  if form.is_valid():
    new_price = form.save(commit=False)
    new_price.card_id = card_id
    new_price.save()
  return redirect('cards_detail', card_id=card_id)

class DropOffCreate(CreateView):
  model = DropOff
  fields = '__all__'

class DropOffList(ListView):
  model = DropOff

class DropOffDetail(DetailView):
  model = DropOff

class DropOffUpdate(UpdateView):
  model = DropOff
  fields = ['name', 'address', 'datetime']

class DropOffDelete(DeleteView):
  model = DropOff
  success_url = '/dropoff/'

def assoc_dropoff(request, card_id, dropoff_id):
  Card.objects.get(id=card_id).dropoff.add(dropoff_id)
  return redirect('cards_detail', card_id=card_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('cards_index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)