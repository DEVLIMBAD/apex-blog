from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLES = (
        ('auther', 'Author'),
        ('user', 'regular user'),
    )
    role = models.CharField(max_length=10, choices=ROLES, default='user')
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)


    def __str__(self):
        return self.username

    def is_admin(self):
        return self.role == 'admin'
    
    def is_author(self):
        return self.role == 'author'



