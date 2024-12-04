from django.urls import path
from . import views

urlpatterns = [
  path('',views.all_properties, name='properties'), 
  path('add/', views.AddProperty.as_view(), name='add_property'),  
  path('<int:pk>/', views.PropertyDetailView.as_view(), name='property_detail'),
  path('<int:pk>/edit/',views.PropertyUpdateView.as_view(), name="edit_property"),
  path('<int:pk>/delete/', views.PropertyDeleteView.as_view(), name='delete_property')
]