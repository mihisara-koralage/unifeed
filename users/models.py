from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# 1. Define the Custom Manager first
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')  # Set default role to admin for superusers

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


# 2. Your updated CustomUser Model
class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = 'student', 'Student'
        PAGE    = 'page',    'Page / Organisation'
        ADMIN   = 'admin',   'Admin'

    # Remove username — we log in with email instead
    username = None
    email    = models.EmailField(unique=True)

    role     = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT)
    bio      = models.TextField(blank=True)
    avatar   = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)  # for Page accounts awaiting admin approval

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = []  # email is already required by USERNAME_FIELD

    # Tell Django to use your custom manager!
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    # Convenience properties
    @property
    def is_student(self):
        return self.role == self.Role.STUDENT

    @property
    def is_page(self):
        return self.role == self.Role.PAGE

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN