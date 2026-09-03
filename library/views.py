from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Book, Author, Category, Member, Issue
from .forms import BookForm, AuthorForm, CategoryForm, MemberForm


@login_required
def dashboard(request):

    total_books = Book.objects.count()
    total_authors = Author.objects.count()
    total_categories = Category.objects.count()
    total_members = Member.objects.count()

    issued_books = Issue.objects.filter(status='issued').count()
    available_books = Book.objects.filter(
        available_quantity__gt=0
    ).count()

    overdue_books = Issue.objects.filter(
        status='issued',
        due_date__lt=timezone.now().date()
    ).count()

    return render(
        request,
        'library/dashboard.html',
        {
            'total_books': total_books,
            'total_authors': total_authors,
            'total_categories': total_categories,
            'total_members': total_members,
            'issued_books': issued_books,
            'available_books': available_books,
            'overdue_books': overdue_books,
        }
    )


# =========================
# BOOK CRUD
# =========================

@login_required
def book_list(request):

    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    status = request.GET.get('status', '')

    books = Book.objects.select_related(
        'author',
        'category'
    ).all()

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(isbn__icontains=query) |
            Q(author__name__icontains=query)
        )

    if category:
        books = books.filter(category_id=category)

    if status == 'available':
        books = books.filter(available_quantity__gt=0)

    elif status == 'issued':
        books = books.filter(available_quantity=0)

    paginator = Paginator(books, 5)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(
        request,
        'library/book_list.html',
        {
            'page_obj': page_obj,
            'categories': categories,
            'query': query,
            'selected_category': category,
            'selected_status': status,
        }
    )


@login_required
def book_create(request):

    if request.method == 'POST':

        form = BookForm(request.POST)

        if form.is_valid():

            book = form.save()

            book.available_quantity = book.quantity
            book.save()

            messages.success(
                request,
                'Book added successfully.'
            )

            return redirect('book_list')

    else:
        form = BookForm()

    return render(
        request,
        'library/book_form.html',
        {'form': form}
    )


@login_required
def book_update(request, pk):

    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':

        form = BookForm(request.POST, instance=book)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Book updated successfully.'
            )

            return redirect('book_list')

    else:
        form = BookForm(instance=book)

    return render(
        request,
        'library/book_form.html',
        {
            'form': form,
            'book': book
        }
    )


@login_required
def book_delete(request, pk):

    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':

        book.delete()

        messages.success(
            request,
            'Book deleted successfully.'
        )

        return redirect('book_list')

    return render(
        request,
        'library/book_confirm_delete.html',
        {'book': book}
    )


# =========================
# AUTHOR
# =========================

@login_required
def author_list(request):

    authors = Author.objects.all()

    return render(
        request,
        'library/author_list.html',
        {'authors': authors}
    )


@login_required
def author_create(request):

    if request.method == 'POST':

        form = AuthorForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Author added.')
            return redirect('author_list')

    else:
        form = AuthorForm()

    return render(
        request,
        'library/author_form.html',
        {'form': form}
    )


@login_required
def author_delete(request, pk):

    author = get_object_or_404(Author, pk=pk)

    if request.method == 'POST':
        author.delete()
        messages.success(request, 'Author deleted.')

    return redirect('author_list')


# =========================
# CATEGORY
# =========================

@login_required
def category_list(request):

    categories = Category.objects.all()

    return render(
        request,
        'library/category_list.html',
        {'categories': categories}
    )


@login_required
def category_create(request):

    if request.method == 'POST':

        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Category added.')
            return redirect('category_list')

    else:
        form = CategoryForm()

    return render(
        request,
        'library/category_form.html',
        {'form': form}
    )


@login_required
def category_delete(request, pk):

    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted.')

    return redirect('category_list')


# =========================
# MEMBER
# =========================

@login_required
def member_list(request):

    members = Member.objects.select_related('user').all()

    return render(
        request,
        'library/member_list.html',
        {'members': members}
    )


@login_required
def member_create(request):

    if request.method == 'POST':

        form = MemberForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Member added successfully.'
            )

            return redirect('member_list')

    else:
        form = MemberForm()

    return render(
        request,
        'library/member_form.html',
        {'form': form}
    )


@login_required
def member_delete(request, pk):

    member = get_object_or_404(Member, pk=pk)

    if request.method == 'POST':

        member.delete()

        messages.success(
            request,
            'Member deleted successfully.'
        )

    return redirect('member_list')


# =========================
# ISSUE BOOK
# =========================

@login_required
def issue_book(request):

    if request.method == 'POST':

        book_id = request.POST.get('book')
        member_id = request.POST.get('member')

        book = get_object_or_404(Book, id=book_id)
        member = get_object_or_404(Member, id=member_id)

        if book.available_quantity <= 0:

            messages.error(
                request,
                'This book is not available.'
            )

            return redirect('issue_book')

        existing_issue = Issue.objects.filter(
            book=book,
            member=member,
            status='issued'
        ).exists()

        if existing_issue:

            messages.error(
                request,
                'This member already has this book.'
            )

            return redirect('issue_book')

        issue_date = timezone.now().date()
        due_date = issue_date + timedelta(days=14)

        Issue.objects.create(
            book=book,
            member=member,
            issue_date=issue_date,
            due_date=due_date
        )

        book.available_quantity -= 1
        book.save()

        messages.success(
            request,
            f'{book.title} issued successfully.'
        )

        return redirect('issue_list')

    books = Book.objects.filter(
        available_quantity__gt=0
    )

    members = Member.objects.select_related('user').all()

    return render(
        request,
        'library/issue_book.html',
        {
            'books': books,
            'members': members
        }
    )


# =========================
# ISSUE LIST
# =========================

@login_required
def issue_list(request):

    issues = Issue.objects.select_related(
        'book',
        'member',
        'member__user'
    ).all()

    paginator = Paginator(issues, 10)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'library/issue_list.html',
        {
            'page_obj': page_obj,
            'today': timezone.localdate(),
            'current_datetime': timezone.localtime()
        },
    )


# =========================
# RETURN BOOK
# =========================

@login_required
def return_book(request, pk):

    issue = get_object_or_404(
        Issue,
        pk=pk
    )

    if issue.status == 'returned':

        messages.warning(
            request,
            'Book already returned.'
        )

        return redirect('issue_list')

    issue.return_date = timezone.now().date()

    issue.fine = issue.calculate_fine()

    issue.status = 'returned'

    issue.save()

    issue.book.available_quantity += 1
    issue.book.save()

    messages.success(
        request,
        f'Book returned. Fine: Rs. {issue.fine}'
    )

    return redirect('issue_list')