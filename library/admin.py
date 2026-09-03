from django.contrib import admin

from .models import (
    Author,
    Category,
    Book,
    Member,
    Issue
)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'email'
    )

    search_fields = (
        'name',
        'email'
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        'name',
    )

    search_fields = (
        'name',
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'isbn',
        'author',
        'category',
        'quantity',
        'available_quantity',
    )

    list_filter = (
        'category',
        'author',
    )

    search_fields = (
        'title',
        'isbn',
        'author__name',
    )


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'phone',
        'joined_date',
    )

    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name',
    )


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):

    list_display = (
        'book',
        'member',
        'issue_date',
        'due_date',
        'return_date',
        'status',
        'fine',
    )

    list_filter = (
        'status',
        'issue_date',
        'due_date',
    )

    search_fields = (
        'book__title',
        'member__user__username',
    )