from django.shortcuts import render, redirect
from .models import Quote
from .forms import QuoteForm, RegisterForm, QuoteSearchForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm

@login_required
def my_quotes(request):
    form = QuoteSearchForm(request.GET)
    quotes = Quote.objects.filter(user=request.user).order_by('-id')

    if form.is_valid():
        text = form.cleaned_data.get('text')
        author = form.cleaned_data.get('author')
        category = form.cleaned_data.get('category')

        if text:
            quotes = quotes.filter(text__icontains=text)
        if author:
            quotes = quotes.filter(author__icontains=author)
        if category:
            quotes = quotes.filter(category__icontains=category)

    return render(request, 'quote/my_quotes.html', {
        'quotes': quotes,
        'search_form': form
    })

def home(request):
    quotes = Quote.objects.all().order_by('-id')

    search_form = QuoteSearchForm(request.GET)
    if search_form.is_valid():
        filter_text = search_form.cleaned_data.get('text', None)
        filter_author = search_form.cleaned_data.get('author', None)
        filter_category = search_form.cleaned_data.get('category', None)
        if filter_text:
            quotes = quotes.filter(text__icontains=filter_text)
        if filter_author:
            quotes = quotes.filter(author__icontains=filter_author)
        if filter_category:
            quotes = quotes.filter(category__icontains=filter_category)
        # najnowsze na górze
    
    paginator = Paginator(quotes, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    context = {
        'quotes': page_obj,
        'search_form': search_form,
    }
    return render(request, 'quote/home.html', context)

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

