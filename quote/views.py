from django.shortcuts import render, redirect
from .models import Quote, Comment, Vote, VoteType
from .forms import QuoteForm, CommentForm, RegisterForm, QuoteSearchForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .utils import generate_quote

def quote_generator(request):
    quote = None
    user_feeling = None 

    if request.method == 'POST':
        user_feeling = request.POST.get('user_feeling')

        if 'save_quote' in request.POST and request.user.is_authenticated:
            quote = request.POST.get('generated_quote')
            Quote.objects.create(
                author='Falcon3-1B-Instruct',
                text=quote,
                category=user_feeling,
                user=request.user
            )
            return redirect('my_quotes')
        else:
            quote = generate_quote(user_feeling)

    return render(request, "quote/quote_generator.html", {
        "quote": quote,
        "user_feeling": user_feeling 
    })

@login_required
def my_quotes(request):
    form = QuoteSearchForm(request.GET)
    quotes = Quote.objects.filter(user=request.user).order_by('-id')

    comments = []
    for quote in quotes:
        comments.append(quote.comments.all())

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
        'search_form': form,
        'comments': comments,
    })
class VoteCounts:
    def __init__(self, quote_id, heart, curious, skull):
        self.quote_id = quote_id
        self.heart = heart
        self.curious = curious
        self.skull = skull

def home(request):
    quotes = Quote.objects.all().order_by('-id')

    comments = []
    for quote in quotes:
        comments.append(quote.comments.all())

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
        'comments': comments,
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
            return redirect('home') #change it to my_quotes?
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

@login_required
def add_comment(request, quote_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        quote = get_object_or_404(Quote, id=quote_id)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.quote = quote
            comment.save()
            return redirect('home')
    else:
        form = CommentForm()
    return render(request, 'quote/add_comment.html', {'form': form})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user != request.user:
        return HttpResponseForbidden("Nie masz uprawnień do usunięcia tego komentarza.")
    if request.method == 'POST':
        comment.delete()
        return redirect('home')
    return render(request, 'quote/delete_comment.html', {'comment': comment})

def get_vote_counts_json(quote):
    heart_count = Vote.objects.filter(quote=quote, typ=VoteType.HEART).count()
    curious_count = Vote.objects.filter(quote=quote, typ=VoteType.CURIOUS).count()
    skull_count = Vote.objects.filter(quote=quote, typ=VoteType.SKULL).count()

    vote_counts = {
        "heart": heart_count,
        "curious": curious_count,
        "skull": skull_count,
    }
    return vote_counts

@login_required
def toggle_vote(request):
    if request.method == 'POST':
        quote_id = request.POST.get('quote_id')
        vote_type = request.POST.get('vote_type')
        if not quote_id or not vote_type:
            return JsonResponse({"error": "Invalid request"}, status=400)
        
        if vote_type not in ["HR", "CR", "SK"]:
            return JsonResponse({"error": "Invalid vote type"}, status=400)
        
        quote = get_object_or_404(Quote, id=quote_id)
        existing_vote = Vote.objects.filter(quote=quote, user=request.user).first()
        is_removing = False
        if existing_vote:
            if existing_vote.typ == vote_type:
                is_removing = True
            existing_vote.delete()
        if is_removing:
            return JsonResponse(get_vote_counts_json(quote))
        
        if vote_type in VoteType.values:
            vote = Vote.objects.create(quote=quote, user=request.user, typ=vote_type)
            vote.save()
            return JsonResponse(get_vote_counts_json(quote))
    return JsonResponse({"error": "Invalid request"}, status=400)

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

