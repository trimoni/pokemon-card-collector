from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('cards/', views.cards_index, name='cards_index'),
  path('cards/<int:card_id>/', views.cards_detail, name='cards_detail'),
  path('cards/create/', views.CardCreate.as_view(), name='cards_create'),
  path('cards/<int:pk>/update', views.CardUpdate.as_view(), name='cards_update'),
  path('cards/<int:pk>/delete', views.CardDelete.as_view(), name='cards_delete')
]
