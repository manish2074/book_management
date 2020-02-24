from django.shortcuts import render,redirect
from .models import Book,Language
from .tasks import create_book,update_book
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CreateBooksForm,UpdateBooksForm
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView,UpdateView,DeleteView,CreateView
from django.urls import reverse_lazy
# Create your views here.

# This is the view to create the book.The user has to 
# be logged_in to create the book.If not the user is redirected 
# to login.If the form is not-valid , user has to fill again.
#From line 35 to 37 , The form takes in the list of language
# and in db it is saved in lowercase .The user just have to give 
# space for next language to add . 

class CreateBooksView(LoginRequiredMixin,CreateView):
    login_url = "/books/login"
    form_class = CreateBooksForm
    template_name = "books/create.html"
    success_url = reverse_lazy('home')


    def form_valid(self,form):
        tag_list=[]
        books = form.save(commit=False)
        books.author = self.request.user
        languages = form.cleaned_data['languages']
        books.save() # must be save before adding m2m
        tag_list=[Language.objects.get_or_create(name=tag)[0] for tag in languages.lower().split()]
        for tag in tag_list:
            a = books.language.add(tag)
        books.language.set = a      
        books.save()
        create_book.delay(books.pk)
        return super(CreateBooksView,self).form_valid(form)


    def form_invalid(self,form):
        print (form.errors)
        return super(CreateBooksView,self).form_invalid(form) 

#This is a list of books which has been paginated
# A page contains 4 books

def book_list(request,tag_slug=None):
    object_list=Book.objects.all()
    paginator = Paginator(object_list,4)
    page = request.GET.get('page')
    try :
        books = paginator.page(page)
    except PageNotAnInteger as e:
        books = paginator.page(1)

    except EmptyPage:
        books = paginator.page(paginator.num_pages)

        
    return render(request,'books/index.html',{'books':books})
    
#This is a simple class based detail view.

class BookDetail(DetailView):
    model = Book
    template_name='books/detail.html'
    context_object_name = 'books'

#This is a update view for the book
# after the book is updated, the message is being 
# sent to user to notify the changes

@login_required
def post_update(request,pk):
    update = get_object_or_404(Book,pk=pk)
    form = UpdateBooksForm(request.POST or None ,request.FILES or None,instance=update)

    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.save() 
            messages.success(request,'Updated successfully!')
            update_book.delay(post.pk)
    context ={
        'form':form
    }      
        
    return render(request,'books/update.html',context)

#This is a delete view for the book.
# The user is notified after his book
# has been deleted.

@login_required
def post_delete(request,pk):
    post = get_object_or_404(Book,pk=pk)
    post.delete()
    return redirect('home')