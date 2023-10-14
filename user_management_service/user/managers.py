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
        user.is_staff = True

        CustomUser = apps.get_model('user', 'CustomUser')
        user.user_type = CustomUser.UserTypeChoices.ADMIN

        user.save(using=self._db)

        return user

    def is_admin(self, user):
        return user.is_superuser
    
    def is_coach(self, user):
        ## check if user is connected to coach model (related_name='coach')
        return hasattr(user, 'coach')
    
    def is_facility_owner(self, user):
        ## check if user is connected to facility_owner model (related_name='facility_owner')
        return hasattr(user, 'facility_owner')
    
    def is_partner(self, user):
        ## check if user is connected to partner model (related_name='partner')
        return hasattr(user, 'partner')
    
    def is_counselor(self, user):
        ## check if user is connected to counselor model (related_name='counselor')
        return hasattr(user, 'counselor')
