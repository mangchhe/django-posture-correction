from django.shortcuts import render, redirect
from .models import UsersDB
from django.contrib import auth

# Create your views here.

def signup(request):

    if request.method == "POST":
        print(UsersDB.objects.all().filter(username=request.POST["username"]))
        if UsersDB.objects.all().filter(username=request.POST["username"]).exists():
            return render(request, 'signup.html', {'error2':'실패'})
        if request.POST["password1"] == request.POST["password2"]:
            user = UsersDB.objects.create_user(
            username=request.POST["username"], password=request.POST["password1"])
            auth.login(request, user)
            return redirect('main')
            
        return render(request,'signup.html', {'error1':'실패'})
    return render(request,'signup.html')

def login(request):
    
    if request.method == "POST":
        username = request.POST['loginId']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('main')
        else:
            return render(request, 'login.html',{'error':'실패'})
    else:
        return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('main')