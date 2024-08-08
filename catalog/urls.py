from django.urls import path
from catalog import views

urlpatterns = [
    path('', views.index, name='index'),
    # /catalog/books
    path('books/', views.BookListView.as_view(), name='books'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    # path('book/<int:pk>',views.book_detail_view, name='book-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path("loanedbooks/", views.LoanedBooks.as_view(), name="all-borrowed"),
]