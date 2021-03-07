from django.shortcuts import render
from brms_app.forms import NewBookForm, SearchForm
from django.http import HttpResponse, HttpResponseRedirect
from brms_app import models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def userLogin(request):
    data={}
    if request.method=='POST':
        username=request.POST['username'];
        password=request.POST['password'];
        user=authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            request.session['username']=username
            return HttpResponseRedirect('/brms_app/view-books')
        else:
            data['error']="Username or Password is incorrect"
            res=render(request,'brms_app/user_login.html',data)
            return res
    else:
        return render(request,'brms_app/user_login.html',data)

def userLogout(request):
    logout(request)
    return HttpResponseRedirect('/brms_app/login')

@login_required(login_url="/brms_app/login")
def searchBook(request):
    form=SearchForm()
    res=render(request,'brms_app/search_book.html',{'form':form})
    return res

@login_required(login_url="/brms_app/login")
def search(request):
    form=SearchForm(request.POST)
    books=models.Book.objects.filter(title=form.data['title'])
    res=render(request,'brms_app/search_book.html',{'form':form,'books':books})
    return res

@login_required(login_url="/brms_app/login")
def deleteBook(request):
    bookid=request.GET['bookid']
    book=models.Book.objects.filter(id=bookid)
    book.delete()
    return HttpResponseRedirect('brms_app/view-books')

@login_required(login_url="/brms_app/login")
def editBook(request):
    book=models.Book.objects.get(id=request.GET['bookid'])
    fields={'title':book.title,'price':book.price,'author':book.author,'publisher':book.publisher}
    form=NewBookForm(initial=fields)
    res=render(request,'brms_app/edit_book.html',{'book':book,'form':form})
    return res

@login_required(login_url="/brms_app/login")
def edit(request):
    if request.method=='POST':
        form=NewBookForm(request.POST)
        book=models.Book()
        book.id=request.POST['bookid']
        book.title=form.data['title']
        book.price=form.data['price']
        book.author=form.data['author']
        book.publisher=form.data['publisher']
        book.save()
    return HttpResponseRedirect('brms_app/view-books')

@login_required(login_url="/brms_app/login")
def viewBooks(request):
    books=models.Book.objects.all()
    username=request.session['username']
    res=render(request,'brms_app/view_books.html',{'books':books,'username':username})
    return res

@login_required(login_url="/brms_app/login")
def newBook(request):
    form=NewBookForm()
    res=render(request,'brms_app/new_book.html',{'form':form})
    return res

@login_required(login_url="/brms_app/login")
def add(request):
    if request.method=='POST':
        form=NewBookForm(request.POST)
        book=models.Book()
        book.title=form.data['title']
        book.price=form.data['price']
        book.author=form.data['author']
        book.publisher=form.data['publisher']
        book.save()
    s="<h1>Record Stored !!</h1><br><a href='/brms_app/view-books'>View All Books</a>"
    return HttpResponse(s)
