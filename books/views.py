from django.shortcuts import render,redirect
from .models import Book,Language
from .tasks import create_book,update_book
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CreateBooksForm,UpdateBooksForm
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView,UpdateView,DeleteView,CreateView,TemplateView,ListView,View
from django.urls import reverse_lazy
from hitcount.views import HitCountDetailView
from .mixins import ObjectViewMixin
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist


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



class BookTemplateView(TemplateView):
    template_name="books/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book=Book.objects.all()
        
        
        context["latest_book"] = book.order_by("-pk") [:6]
        context["rating_books"] = book.filter(ratings__isnull=False).order_by('-ratings__average')
        context['popular_books'] = book.order_by('-hitcount_count_generic__hits')[:6]
       
        return context
    
#This is a simple class based detail view.It counts how many time user has read about book and then place the book
#as most popular book 

class BookDetail(ObjectViewMixin,HitCountDetailView):
    model = Book
    template_name='books/detail.html'
    context_object_name = 'books'
    count_hit = True
    def get_context_data(self, **kwargs):
        book=Book.objects.all()
        context = super().get_context_data(**kwargs)
        self.object.save()

        return context

#This is the view that seperates the genere of the book
#So, that user can get which book they want

class BookCategoryView(ListView):
    model = Book
    ordering =['-pk']
    context_object_name ='category_list'
    template_name="books/category_book.html"
    paginate_by=6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["genere"] = self.kwargs.get('genere')
        return context

    def get_queryset(self):
        genere = self.kwargs.get("genere")
        genere_key = [item[0] for item in Book.GENERE if item[1] == genere][0]

        return Book.objects.filter(genere=genere_key)

#This is a update view for the book
# after the book is updated, the message is being 
# sent to user to notify the changes

@login_required
def post_update(request,pk):
    update = get_object_or_404(Book,pk=pk)
    form = UpdateBooksForm(request.POST or None ,request.FILES or None,instance=update)
    if request.method == 'POST':
        books = form.save(commit=False)     
        books.save()
        form.save_m2m()
        messages.success(request,'Updated successfully!')
        update_book.delay(books.pk)
    context ={
        'form':form,
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

from .models import History
from django.views.generic.detail import SingleObjectMixin

class HistoryList(ListView):
    def get_queryset(self):
        user_history = History.objects.filter(user=self.request.user)
        return user_history   

class HistoryDelete(SingleObjectMixin,View):
    model = History
    def get(self,request,*args,**kwargs):
        obj = self.get_object()
        if obj is not None:
            obj.delete()
        return redirect('history')