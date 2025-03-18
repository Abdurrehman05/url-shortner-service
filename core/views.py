from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404
from .models import URL
from .serializers import URLSerializer
import string
import random

def redirect_url(request, short_url):
    """Redirect to the original URL from a short URL"""
    try:
        url = URL.objects.get(short_url=short_url, is_active=True)
        url.increment_access_count()
        return redirect(url.long_url)
    except URL.DoesNotExist:
        raise Http404("Short URL not found or inactive")

class URLViewSet(viewsets.ModelViewSet):
    queryset = URL.objects.all()
    serializer_class = URLSerializer
    lookup_field = 'short_url'

    def generate_short_url(self):
        """Generate a unique short URL"""
        chars = string.ascii_letters + string.digits
        while True:
            short_url = ''.join(random.choices(chars, k=6))
            if not URL.objects.filter(short_url=short_url).exists():
                return short_url

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(short_url=self.generate_short_url())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        url = self.get_object()
        url.increment_access_count()
        serializer = self.get_serializer(url)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def deactivate(self, request, short_url=None):
        """Deactivate a URL"""
        url = self.get_object()
        url.is_active = False
        url.save()
        return Response({'status': 'URL deactivated'})
