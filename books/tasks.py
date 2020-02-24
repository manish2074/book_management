from celery import shared_task
from django.core.mail import send_mail
from .models import Book
import os

#When these task are called,update_book sends message 
#to the author of the book informing him about the 
# change in the book and create_book sends message when 
# the user creates the book

@shared_task
def update_book(pk):
    order = Book.objects.get(pk=pk)
    subject = 'Changes in Book'
    message = f'Dear,{order.author.username},There have been some changes in your book,{order.name}'
    mail_sent = send_mail(subject,message,os.getenv('EMAIL_USER'),[order.author])
    return mail_sent

@shared_task
def create_book(pk):
    order = Book.objects.get(pk=pk)
    subject = 'Creatation of book'
    message = f'Dear,{order.author.username},your book {order.name} has been created.Thank you!'
    mail = send_mail(subject,message,os.getenv('EMAIL_USER'),[order.author])
    return mail