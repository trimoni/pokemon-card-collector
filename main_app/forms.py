from django.forms import ModelForm
from .models import Price

class PriceForm(ModelForm):
  class Meta:
    model = Price
    fields = ['condition', 'money']