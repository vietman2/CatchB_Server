from django.apps import apps
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, password=None, **extra_fields):
        user = self.model(
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, password=None, **extra_fields):
        user = self.create_user(
            password=password,
            **extra_fields
        )
        user.is_superuser = True

        user.save(using=self._db)

        return user

    def delete_user(self, user):
        user.is_active = False
        user.save(using=self._db)

        return user
