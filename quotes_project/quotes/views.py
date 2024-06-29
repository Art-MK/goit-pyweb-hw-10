from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .models import Quote, Author
from .forms import QuoteForm, AuthorForm
import subprocess
from django.http import JsonResponse


def index(request):
    quotes = Quote.objects.all()
    login_form = AuthenticationForm()
    if request.method == 'POST':
        if 'login' in request.POST:
            login_form = AuthenticationForm(data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect('index')
        elif 'logout' in request.POST:
            logout(request)
            return redirect('index')

    context = {
        'quotes': quotes,
        'login_form': login_form,
    }
    return render(request, 'quotes/index.html', context)

def author_detail(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    quotes = Quote.objects.filter(author=author)
    return render(request, 'quotes/author_detail.html', {'author': author, 'quotes': quotes})

@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.user = request.user
            quote.save()
            return redirect('index')
    else:
        form = QuoteForm()
    return render(request, 'quotes/add_quote.html', {'form': form})

@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = AuthorForm()
    return render(request, 'quotes/add_author.html', {'form': form})

@csrf_exempt
def scrape_data(request):
    if request.method == "POST":
        subprocess.run(["python", "scraper.py"])
        return redirect('index')

def index(request):
    quotes = Quote.objects.all()
    paginator = Paginator(quotes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    tags = Quote.objects.values_list('tags', flat=True).distinct()

    context = {
        'quotes': page_obj,
        'top_ten_tags': top_ten_tags(),
        'tags': tags,
    }
    return render(request, 'quotes/index.html', context)

def quotes_by_tag(request, tag):
    quotes = Quote.objects.filter(tags__icontains=tag)
    paginator = Paginator(quotes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'quotes': page_obj,
        'tag': tag,
    }
    return render(request, 'quotes/quotes_by_tag.html', context)

def top_ten_tags():
    tags = Quote.objects.values_list('tags', flat=True)
    tag_count = {}
    for tag_list in tags:
        if tag_list:
            for tag in tag_list:
                if tag in tag_count:
                    tag_count[tag] += 1
                else:
                    tag_count[tag] = 1
    sorted_tags = sorted(tag_count.items(), key=lambda x: x[1], reverse=True)[:10]
    return [tag for tag, count in sorted_tags]

def search_quotes(request):
    query = request.GET.get('query', '').lower()
    quotes = Quote.objects.filter(tags__icontains=query)
    results = [
        {
            'text': quote.text,
            'author': quote.author.fullname,
            'tags': list(quote.tags),
        }
        for quote in quotes
    ]
    return JsonResponse(results, safe=False)