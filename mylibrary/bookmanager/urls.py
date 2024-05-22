from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('success/', views.success, name='success'),
    path('books/', views.book_list, name='book_list'),
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),
]
