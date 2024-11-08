from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise  ValueError("vous devez avoir une addresse email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('user_type', CustomUser.ADMIN_TYPE)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('user_type')!= CustomUser.ADMIN_TYPE:
            raise ValueError("Le superutilisateur doit avoir un user_type=admin")
        if not email:
            raise ValueError("Le superutilisateur doit avoir une adresse mail")
        return self.create_user(email, password, **extra_fields)





class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = [
        ('client', 'client'),
        ('admin', 'admin')
    ]
    ADMIN_TYPE = 'admin'
    email = models.EmailField(unique=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)


    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []