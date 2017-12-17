from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from .models import Child, Journal
from .serializers import ChildSerializer, JournalSerializer


class ChildViewSet(viewsets.ModelViewSet):
    queryset = Child.objects.all()
    serializer_class = ChildSerializer


class JournalViewSet(viewsets.ModelViewSet):
    queryset = Journal.objects.filter(child__is_studying=True).all()
    serializer_class = JournalSerializer
    filter_backends = [OrderingFilter]
    ordering = ['-date']
