from django.urls import path

from . import views


urlpatterns = [

    path('', views.dashboard, name='dashboard'),

    # Books
    path('books/', views.book_list, name='book_list'),
    path('books/add/', views.book_create, name='book_create'),
    path(
        'books/<int:pk>/edit/',
        views.book_update,
        name='book_update'
    ),
    path(
        'books/<int:pk>/delete/',
        views.book_delete,
        name='book_delete'
    ),

    # Authors
    path('authors/', views.author_list, name='author_list'),
    path(
        'authors/add/',
        views.author_create,
        name='author_create'
    ),
    path(
        'authors/<int:pk>/delete/',
        views.author_delete,
        name='author_delete'
    ),

    # Categories
    path(
        'categories/',
        views.category_list,
        name='category_list'
    ),
    path(
        'categories/add/',
        views.category_create,
        name='category_create'
    ),
    path(
        'categories/<int:pk>/delete/',
        views.category_delete,
        name='category_delete'
    ),

    # Members
    path(
        'members/',
        views.member_list,
        name='member_list'
    ),
    path(
        'members/add/',
        views.member_create,
        name='member_create'
    ),
    path(
        'members/<int:pk>/delete/',
        views.member_delete,
        name='member_delete'
    ),

    # Issue / Return
    path(
        'issue/',
        views.issue_book,
        name='issue_book'
    ),
    path(
        'issues/',
        views.issue_list,
        name='issue_list'
    ),
    path(
        'return/<int:pk>/',
        views.return_book,
        name='return_book'
    ),
]