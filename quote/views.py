from django.shortcuts import render, redirect
from .models import Quote
from .forms import QuoteForm, RegisterForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm

def home(request):
    quotes = Quote.objects.all().order_by('-id')  # najnowsze na górze
    return render(request, 'quote/home.html', {'quotes': quotes})

@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.user = request.user  
            quote.save()
            return redirect('home')
    else:
        form = QuoteForm()
    return render(request, 'quote/add_quote.html', {'form': form})

@login_required
def edit_quote(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)
    if quote.user != request.user:
        return HttpResponseForbidden("Nie masz uprawnień do edycji tego cytatu.")

    if request.method == 'POST':
        form = QuoteForm(request.POST, instance=quote)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = QuoteForm(instance=quote)
    return render(request, 'quote/edit_quote.html', {'form': form})

@login_required
def delete_quote(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)
    if quote.user != request.user:
        return HttpResponseForbidden("Nie masz uprawnień do usunięcia tego cytatu.")
    if request.method == 'POST':
        quote.delete()
        return redirect('home')
    return render(request, 'quote/delete_quote.html', {'quote': quote})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # loguje po rejestracji
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'quote/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'quote/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')

