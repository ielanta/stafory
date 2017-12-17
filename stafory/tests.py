from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Child, Journal
from .serializers import ChildSerializer


class ChildListTest(APITestCase):
    def setUp(self):
        Child.objects.create(name='Катя', gender='F', birth_date='1990-08-08', is_studying=False)

    def test_get_child_list(self):
        url = reverse('child-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual('Катя', response.data[0]['name'])


class CreateChildTest(APITestCase):
    def setUp(self):
        self.data = {'name': 'Катя', 'gender': 'F', 'birth_date': '1990-08-08', 'is_studying': False}

    def test_create_child(self):
        url = reverse('child-list')
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Child.objects.count(), 1)


class UpdateChildTest(APITestCase):
    def setUp(self):
        self.child = Child.objects.create(name='Катя', gender='F', birth_date='1990-08-08', is_studying=False)
        self.data = ChildSerializer(self.child).data
        self.data.update({'is_studying': True})

    def test_update_child(self):
        url = reverse('child-detail', args=[self.child.id])
        response = self.client.put(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_studying'], True)


class JournalListTest(APITestCase):
    def setUp(self):
        ch_not_studying = Child.objects.create(name='Катя', gender='F', birth_date='1990-08-08', is_studying=False)
        ch_studying = Child.objects.create(name='Вера', gender='F', birth_date='1990-08-08', is_studying=True)
        Journal.objects.create(child=ch_not_studying, trustee_name='Светлана')
        Journal.objects.create(child=ch_studying, trustee_name='Светлана')

    def test_get_journal_list(self):
        url = reverse('journal-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # because work only with is_studing=True


class CreateJournalTest(APITestCase):
    def setUp(self):
        ch_not_studying = Child.objects.create(name='Катя', gender='F', birth_date='1990-08-08', is_studying=False)
        ch_studying = Child.objects.create(name='Вера', gender='F', birth_date='1990-08-08', is_studying=True)
        self.data1 = {'child': ch_not_studying.id, 'trustee_name': 'Светлана'}
        self.data2 = {'child': ch_studying.id, 'trustee_name': 'Светлана'}

    def test_create_journal(self):
        url = reverse('journal-list')
        response = self.client.post(url, self.data1, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(url, self.data2, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
