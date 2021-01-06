from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

gender_choice = (
    ('M', 'Male'),
    ('F', 'Female'),
)

blood_choices = (
    ('a+', 'A RhD positive (A+)'),
    ('a-', 'A RhD negative (A-)'),
    ('b+', 'B RhD positive (B+)'),
    ('b-', 'B RhD negative (B-)'),
    ('o+', 'O RhD positive (O+)'),
    ('o-', 'O RhD negative (O-)'),
    ('ab+', 'AB RhD positive (AB+)'),
    ('ab-', 'AB RhD negative (AB-)'),
)

class MyDonorManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email")
        if not username:
            raise ValueError("Users must have an username")

        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True

        user.set_password(password)
        user.save(using=self._db)
        return user

class DonorSignup(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyDonorManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

class Profile(models.Model):
    name = models.CharField(max_length=60)
    email = models.EmailField(max_length=60)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=6, choices=gender_choice, default='Male')
    phone = models.CharField(max_length=20)
    blood_group = models.CharField(max_length=21, choices=blood_choices)
    info = models.TextField(max_length=400, blank=True)
    donor = models.ForeignKey(DonorSignup, on_delete=models.CASCADE)

class Messages(models.Model):
    email_from = models.EmailField(max_length=60)
    email_to = models.EmailField(max_length=60)
    message = models.TextField(max_length=400)
