from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Card, DropOff, Photo
from .forms import PriceForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3
S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'pokemon-card-collector'

# Create your views here.

class Home(LoginView):
  template_name = 'home.html'

def about(request):
  return render(request, 'about.html')

@login_required
def cards_index(request):
  cards = Card.objects.filter(user=request.user)
  return render(request, 'cards/index.html', { 'cards': cards })

@login_required
def cards_detail(request, card_id):
  card = Card.objects.get(id=card_id)
  dropoff_card_doesnt_have = DropOff.objects.exclude(id__in = card.dropoff.all().values_list('id'))
  price_form = PriceForm()
  return render(request, 'cards/detail.html', { 'card': card, 'price_form': price_form, 'dropoff': dropoff_card_doesnt_have })

class CardCreate(LoginRequiredMixin, CreateView):
  model = Card
  fields = ['name', 'type', 'value', 'pack']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class CardUpdate(LoginRequiredMixin, UpdateView):
  model = Card
  fields = ['type', 'value', 'pack']

class CardDelete(LoginRequiredMixin, DeleteView):
  model = Card
  success_url = '/cards/'

@login_required
def add_price(request, card_id):
  form = PriceForm(request.POST)
  if form.is_valid():
    new_price = form.save(commit=False)
    new_price.card_id = card_id
    new_price.save()
  return redirect('cards_detail', card_id=card_id)

class DropOffCreate(LoginRequiredMixin, CreateView):
  model = DropOff
  fields = '__all__'

class DropOffList(LoginRequiredMixin, ListView):
  model = DropOff

class DropOffDetail(LoginRequiredMixin, DetailView):
  model = DropOff

class DropOffUpdate(LoginRequiredMixin, UpdateView):
  model = DropOff
  fields = ['name', 'address', 'datetime']

class DropOffDelete(LoginRequiredMixin, DeleteView):
  model = DropOff
  success_url = '/dropoff/'

@login_required
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

def add_photo(request, card_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex + photo_file.name[photo_file.name.rfind('.'):]
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      photo = Photo(url=url, card_id=card_id)
      card_photo = Photo.objects.filter(card_id=card_id)
      if card_photo.first():
        card_photo.first().delete()
      photo.save()
    except Exception as err:
      print('An error occurred uploading file to S3: %s' % err)
  return redirect('cards_detail', card_id=card_id)