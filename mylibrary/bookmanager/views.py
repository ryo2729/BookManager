from django.shortcuts import render, redirect
from .forms import ISBNForm
from .models import Book
import requests
import re

# 情報を登録する部分
def validate_isbn(isbn):
    pattern = r"^(?:ISBN(?:-10)?:? )?(?=[0-9X]{10}$|(?=(?:[0-9]+[- ]){3})[- 0-9X]{13}$|97[89][0-9]{10}$|(?=(?:[0-9]+[- ]){4})[- 0-9]{17}$)(?:97[89][- ]?)?[0-9]{1,5}[- ]?[0-9]+[- ]?[0-9]+[- ]?[0-9X]$"  
    return bool(re.match(pattern, isbn))

def get_book_info(isbn):
    URL = f"https://api.openbd.jp/v1/get?isbn={isbn}&pretty"
    r = requests.get(URL)
    data = r.json()
    if data and data[0]:
        title = data[0]["summary"]["title"]
        author = data[0]["summary"]["author"]
        publisher = data[0]["summary"]["publisher"]
        return title, author, publisher
    return None, None, None

def index(request):
    if request.method == 'POST':
        form = ISBNForm(request.POST)
        if form.is_valid():
            isbn = form.cleaned_data['isbn']
            if validate_isbn(isbn):
                title, author, publisher = get_book_info(isbn)
                if title:
                    Book.objects.create(isbn=isbn, title=title, author=author, publisher=publisher)
                    return redirect('success')
                else:
                    return render(request, 'index.html', {'form': form, 'error': 'このISBNに該当する本はありませんでした。'})
            else:
                return render(request, 'index.html', {'form': form, 'error': 'このISBNは正しい形式ではありません。'})
    else:
        form = ISBNForm()
    return render(request, 'index.html', {'form': form})

def success(request):
    return render(request, 'success.html')


# 情報を閲覧する部分
def book_list(request):
    keyword = request.GET.get('keyword')
    if keyword:
        books = Book.objects.filter(title__icontains=keyword) | Book.objects.filter(author__icontains=keyword)
    else:
        books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

#　情報を削除する部分
def delete_book(request, book_id):
    book = Book.objects.get(pk=book_id)
    book.delete()
    return redirect('book_list')







# Create your views here.
