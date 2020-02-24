from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _

# This is a User model that which inherits from AbstractUser
# Here the email is login_field and should be unique so that 
# when there has been some change to the book the rightful owner 
# gets the notice.

# Create your models here.
def upload_image(instance,filename):
    return f"{instance.author}/{filename}"

class User(AbstractUser):
    email = models.EmailField(_('email address'),unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username","first_name","last_name")

# As per the condition, Book has a ManyToManyField relation with
# Language.The ordering of the book is according to latest book
# uploaded. author has on_delete=models.PROTECT because even though
# the author account is_active = False or deleted the book should not

class Language(models.Model):
    name= models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    name=models.CharField(max_length=200) 
    about =models.TextField()
    image = models.ImageField(upload_to=upload_image)  
    language = models.ManyToManyField(Language,related_name='book') 
    author = models.ForeignKey(User,on_delete=models.PROTECT,related_name='bauthor')
    def __str__(self):
        return self.name  

         
    class Meta:
        ordering = ('-pk',)


    def get_absolute_url(self):
        return reverse("book_detail", kwargs={"pk": self.pk})
             
