# (15) tests.py - Pruebas unitarias y de integración para usuarios y autenticación

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User

class UserTests(APITestCase):
    def setUp(self):
        """
        Configuración inicial para las pruebas. Se crea un usuario de prueba
        que será utilizado en las pruebas.
        """
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'password123'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_create_user(self):
        """
        Prueba para crear un nuevo usuario.
        """
        url = reverse('user-list')
        new_user_data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'newpassword123'
        }
        response = self.client.post(url, new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)  # Verifica que se haya creado un nuevo usuario

    def test_login_user(self):
        """
        Prueba para iniciar sesión con credenciales válidas.
        """
        url = reverse('login')
        data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_protected_route(self):
        """
        Prueba para acceder a una ruta protegida.
        """
        # Iniciar sesión para obtener el token
        url_login = reverse('login')
        login_response = self.client.post(url_login, {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }, format='json')
        
        token = login_response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)  # Agrega el token a la cabecera

        url = reverse('user-detail', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user_invalid_email(self):
        """
        Prueba para asegurar que no se puede crear un usuario con un email inválido.
        """
        url = reverse('user-list')
        invalid_user_data = {
            'email': 'invalid-email',
            'username': 'invaliduser',
            'password': 'newpassword123'
        }
        response = self.client.post(url, invalid_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user_invalid_credentials(self):
        """
        Prueba para intentar iniciar sesión con credenciales inválidas.
        """
        url = reverse('login')
        data = {
            'email': self.user_data['email'],
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

    def test_user_detail_not_found(self):
        """
        Prueba para acceder a un usuario que no existe.
        """
        url = reverse('user-detail', args=[999])  # ID que no existe
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_user(self):
        """
        Prueba para actualizar un usuario.
        """
        url_login = reverse('login')
        login_response = self.client.post(url_login, {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }, format='json')

        token = login_response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        url = reverse('user-detail', args=[self.user.id])
        update_data = {
            'username': 'updateduser',
            'email': 'updated@example.com'
        }
        response = self.client.put(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.email, 'updated@example.com')

    def test_delete_user(self):
        """
        Prueba para eliminar (desactivar) un usuario.
        """
        url_login = reverse('login')
        login_response = self.client.post(url_login, {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }, format='json')

        token = login_response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        url = reverse('user-detail', args=[self.user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.user.id, is_active=True).exists())  # Verifica que el usuario esté desactivado

    def test_permission_denied_on_unauthenticated_user(self):
        """
        Prueba para asegurar que un usuario no autenticado no puede acceder a rutas protegidas.
        """
        url = reverse('user-detail', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
