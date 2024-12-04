from django.shortcuts import render, redirect
from django.contrib import messages
import requests
from bs4 import BeautifulSoup
from .models import Link
# Create your views here.


def scrape(request):
    if request.method == 'POST':
        site = request.POST.get('site', '')

        page = requests.get(site)
        soup = BeautifulSoup(page.text, 'html.parser')

        for link in soup.find_all('a'):
            link_address = link.get('href')
            link_text = link.string
            Link.objects.create(address=link_address, name=link_text)

        return redirect("/")
    else:
        link_data = Link.objects.all()

    context = {
        'link_data': link_data
    }
    return render(request, 'scrape_site/result.html', context)


def delete(request):
    delete_all = None
    if request.method == "POST":
        delete_all = Link.objects.all().delete()
        messages.success(request, "Successfuly deleted content!")
        return redirect('/')

    context = {
        'delete_all': delete_all
    }

    return render(request, 'scrape_site/delete.html', context)
