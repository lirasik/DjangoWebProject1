"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from .forms  import AnketaForm, BlogForm 
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from .models import Blog
from .models import Comment
from .forms import CommentForm

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Страница с нашими контактами.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Сведения о нас.',
            'year':datetime.now().year,
        }
    )

def links(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title':'Полезные ресурсы',
            
            'year':datetime.now().year,
        }
    )

def anketa(request):
    assert isinstance(request, HttpRequest)
    data = None
    gender = {'1': 'Мужcкой', '2': 'Женский'}
    car = {'1': 'Да', '2': 'Нет'}
    if request.method == 'POST':
        form = AnketaForm(request.POST)
        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['city'] = form.cleaned_data['city']
            data['gender'] = gender[ form.cleaned_data['gender']]
            data['car'] = car[ form.cleaned_data['car']]
            data['email'] = form.cleaned_data['email']
            if (form.cleaned_data['notice'] == True):
                data['notice'] = 'Да'
            else:
                data['notice'] = 'Нет'
            data['message'] = form.cleaned_data['message']
            form = None
    else:
        form = AnketaForm()
    return render(
        request,
        'app/anketa.html',
        {
            'form':form,
            'data':data
        }
    )

def registration(request):
    """Renders the registration page."""

    if request.method == "POST":
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_staff = False
            reg_f.is_active = True
            reg_f.is_superuser = False
            reg_f.date_joined = datetime.now()
            reg_f.last_login = datetime.now()

            reg_f.save()

            return redirect('home') 
    else:
        regform = UserCreationForm() 
    assert isinstance(request, HttpRequest) 
    return render(
        request,
        'app/registration.html',
        {
            
            'regform':regform,
            
            'year':datetime.now().year,
        }
    )

def blog(request):
     posts = Blog.objects.all()

     assert isinstance(request, HttpRequest)
     return render(
         request,
         'app/blog.html',
         {
             'title': 'Блог',
             'posts': posts,
             'year':datetime.now().year,
         }
     )

def blogpost(request, parametr):

       """Renders the blogpost page."""
       assert isinstance(request, HttpRequest)
       post_1 = Blog.objects.get(id=parametr) 
       comments = Comment.objects.filter(post=parametr)

       if request.method == "POST":
           form = CommentForm(request.POST)
           if form.is_valid():
               comment_f = form.save(commit=False)
               comment_f.author = request.user
               comment_f.date = datetime.now()
               comment_f.post = Blog.objects.get(id=parametr)
               comment_f.save()
               return redirect('blogpost', parametr=post_1.id)
       else:
           form = CommentForm()
       return render(
          request,
          'app/blogpost.html',
          {
             'post_1': post_1, 
             'comments': comments,
             'form': form,
             'year':datetime.now().year,
          }

        )

def newpost(request):
    """Renders the newpost page."""
    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()
            blog_f.author = request.user
            blog_f.save()

            return redirect('blog')
    else:
        blogform = BlogForm()

    return render(
        request,
        'app/newpost.html',
        {
            'blogform': blogform,
            'title':'Добавить статью блога',
            
            'year':datetime.now().year,
        }
        
        
    )
def videopost(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'title':'Наши видео',
            
            'year':datetime.now().year,
        }
    )