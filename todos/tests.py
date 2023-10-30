from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import Todo


class TestListCreateTodos(APITestCase):
    def authenticate(self):
        self.client.post(reverse('register'), {'username':'username', 'email':'email@gmail.com', 'password':'password'})
        response = self.client.post(reverse('login'), {"email":"email@gmail.com", "password":"password"})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['token']}")

    def test_should_not_create_todo_with_no_user_authentication(self):
        sample_todos = {
            'title':'test',
            'description': 'hello world'
        }
        response = self.client.post(reverse('todos'),sample_todos)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_should_create_todo(self):
        previous_todo_count = Todo.objects.all().count()
        self.authenticate()
        sample_todos = {
            'title':'test',
            'description': 'hello world'
        }
        response = self.client.post(reverse('todos'),sample_todos)
        self.assertEqual(Todo.objects.all().count(), previous_todo_count+1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'test')
        self.assertEqual(response.data['description'], 'hello world')

    
    def test_retrieves_all_todos(self):
        self.authenticate()
        response = self.client.get(reverse('todos'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data['results'], list)

        sample_todos = {
            'title':'test',
            'description': 'hello world'
        }
        self.client.post(reverse('todos'), sample_todos)

        res = self.client.get(reverse('todos'))
        self.assertIsInstance(res.data['count'], int)
        self.assertEqual(res.data['count'], 1)
