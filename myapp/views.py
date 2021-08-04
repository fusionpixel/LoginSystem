from django.contrib.auth.forms import AuthenticationForm
from .forms import CreateUserForm
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "index.html")


def signup(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CreateUserForm()

    context = {"form": form}

    return render(request, "signup.html", context)


def loginPage(request):
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"form": form})


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("login")


@login_required
def home(request):
    return render(request, "home.html")
