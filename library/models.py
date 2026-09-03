from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Author(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    biography = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20, unique=True)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books'
    )
    publisher = models.CharField(max_length=150, blank=True)
    publication_year = models.PositiveIntegerField(null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    available_quantity = models.PositiveIntegerField(default=1)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_available(self):
        return self.available_quantity > 0

    @property
    def status(self):
        if self.available_quantity > 0:
            return "Available"
        return "Issued"

    def __str__(self):
        return self.title


class Member(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='member_profile'
    )
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    joined_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Issue(models.Model):

    STATUS_CHOICES = [
        ('issued', 'Issued'),
        ('returned', 'Returned'),
    ]

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='issues'
    )

    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name='issues'
    )

    issue_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='issued'
    )

    fine = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_fine(self):

        end_date = self.return_date or timezone.now().date()

        if end_date > self.due_date:
            late_days = (end_date - self.due_date).days
            return late_days * 10

        return 0

    def __str__(self):
        return f"{self.book.title} - {self.member}"