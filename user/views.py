from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm

def signup(request):

    if request.user.is_authenticated:
        return redirect('/bilti/user/')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/bilti/user/')
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

def signin(request):
    nextURL = request.GET.get("next")
    if(nextURL== None):
        nextURL = '/bilti/user/'
    print(nextURL)
    if request.user.is_authenticated:
        print(request.user)
        return redirect(request, nextURL)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(nextURL)
        else:
            form = AuthenticationForm(request.POST)
            return render(request, 'signin.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'signin.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth import logout

def signout(request):
    logout(request)
    return redirect('/bilti/')

