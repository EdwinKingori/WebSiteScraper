from django.urls import path
from . import views

urlpatterns = [
    path('', views.scrape, name='results'),
    path('delete/', views.delete, name='delete')
]
