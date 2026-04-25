from django.test import TestCase

from accounts.models import CustomUser


class AccountsBaseTestcase(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="testuser1@example.com",
            password="password123",
        )
        self.admin = CustomUser.objects.create_superuser(
            email="admin@example.com",
            password="password123",
        )
        self.vendor = CustomUser.objects.create_user(
            email="vendor@example.com",
            password="password123",
            role=CustomUser.Role.VENDOR,
            is_vendor=True
        )
