from django.urls import path
from .views import ScrapeApiView, get_links, delete_links
from .import views

urlpatterns = [
    path('scrape/', ScrapeApiView.as_view(), name='api_scrape'),
    path('links/', get_links, name='get_links'),
    path('delete/', delete_links, name='delete_links')

]
