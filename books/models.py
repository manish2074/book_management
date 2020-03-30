from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from hitcount.models import HitCountMixin,HitCount
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation,GenericForeignKey
from star_ratings.models import Rating

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
    GENERE=(("0","Romantic"),("1","Horror"),("2","Comedy"))
    name=models.CharField(max_length=200) 
    about =models.TextField()
    image = models.ImageField(upload_to=upload_image)  
    book_pdf = models.FileField(upload_to=upload_image,validators=[FileExtensionValidator(['pdf'])])
    language = models.ManyToManyField(Language,related_name='book') 
    author = models.ForeignKey(User,on_delete=models.PROTECT,related_name='bauthor')
    genere= models.CharField(choices=GENERE, max_length=2)
    hitcount_count_generic = GenericRelation(HitCount,object_id_field='object_pk',related_query_name='hit_count_generic_relation')
    ratings = GenericRelation(Rating, related_query_name='books')
    def __str__(self):
        return self.name  

         
    class Meta:
        ordering = ('-pk',)


    def get_absolute_url(self):
        return reverse("book_detail", kwargs={"pk": self.pk})
             
class History(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,on_delete=models.SET_NULL,null=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    viewed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content_object.name

    class Meta:
        ordering = ('-pk',)
        verbose_name_plural = 'History'   

from .signals import object_viewed_signal

def object_viewed_receiver(sender,instance,request,*args,**kwargs):
    new_history = History.objects.create(
        user = request.user,
        content_type = ContentType.objects.get_for_model(sender),
        object_id = instance.id,
        
    )

object_viewed_signal.connect(object_viewed_receiver)