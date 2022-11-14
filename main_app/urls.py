from django.urls import path
from . import views

urlpatterns = [
  path('', views.Home.as_view(), name='home'),
  path('about/', views.about, name='about'),
  path('cards/', views.cards_index, name='cards_index'),
  path('cards/<int:card_id>/', views.cards_detail, name='cards_detail'),
  path('cards/create/', views.CardCreate.as_view(), name='cards_create'),
  path('cards/<int:pk>/update', views.CardUpdate.as_view(), name='cards_update'),
  path('cards/<int:pk>/delete', views.CardDelete.as_view(), name='cards_delete'),
  path('cards/<int:card_id>/add_price/', views.add_price, name='add_price'),
  path('dropoff/create/', views.DropOffCreate.as_view(), name='dropoff_create'),
  path('dropoff/<int:pk>/', views.DropOffDetail.as_view(), name='dropoff_detail'),
  path('dropoff/', views.DropOffList.as_view(), name='dropoff_index'),
  path('dropoff/<int:pk>/update/', views.DropOffUpdate.as_view(), name='dropoff_update'),
  path('dropoff/<int:pk>/delete/', views.DropOffDelete.as_view(), name='dropoff_delete'),
  path('cards/<int:card_id>/assoc_dropoff/<int:dropoff_id>/', views.assoc_dropoff, name='assoc_dropoff'),
  path('accounts/signup/', views.signup, name='signup'),
  path('cards/<int:card_id>/add_photo/', views.add_photo, name='add_photo'),
]
