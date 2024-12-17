from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
import requests
from bs4 import BeautifulSoup
from scrape_site.models import Link
from .serializers import LinkSerializer
# Create your views here.


class ScrapeApiView(APIView):
    def post(self, request):
        site = request.data.get('site', '')
        if not site:
            return Response({'error': 'Site URL is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            page = requests.get(site)
            soup = BeautifulSoup(page.text, 'html.parser')

            # lets clear old links bfore scraping new or updated links
            Link.objects.all().delete()

            # scraping saved links
            for link in soup.find_all('a'):
                link_address = link.get('href')
                link_text = link.string if link.string else 'no text available'
                Link.objects.create(address=link_address, name=link_text)

            return Response({
                'message': 'scraping completed successfully!',
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_links(request):
    links = Link.objects.all()
    serializer = LinkSerializer(links, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
def delete_links(request):
    Link.objects.all().delete()
    return Response({
        'message': 'Links deleted successfully!'
    }, status=status.HTTP_204_NO_CONTENT)
