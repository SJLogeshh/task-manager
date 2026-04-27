from django.test import TestCase
from django.contrib.auth.models import User
from .models import Task

class TaskTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass"
        )

    def test_create_task(self):
        task = Task.objects.create(
            title="Test Task",
            user=self.user
        )
        self.assertEqual(task.title, "Test Task")

    def test_user_login(self):
        login = self.client.login(
            username="testuser",
            password="testpass"
        )
        self.assertTrue(login)