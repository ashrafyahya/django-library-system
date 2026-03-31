from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models, transaction


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=120)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='books')
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']

    def clean(self):
        if self.available_copies > self.total_copies:
            raise ValidationError('Available copies cannot be greater than total copies.')

    def __str__(self):
        return f'{self.title} - {self.author}'


class Booking(models.Model):
    class Status(models.TextChoices):
        BOOKED = 'booked', 'Booked'
        CANCELLED = 'cancelled', 'Cancelled'
        BORROWED = 'borrowed', 'Borrowed'
        RETURNED = 'returned', 'Returned'

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='bookings')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.BOOKED)
    booked_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-booked_at']

    def __str__(self):
        return f'{self.student.username} - {self.book.title} ({self.status})'

    @classmethod
    def create_booking(cls, student, book):
        with transaction.atomic():
            locked_book = Book.objects.select_for_update().get(pk=book.pk)
            if locked_book.available_copies < 1:
                raise ValidationError('No copies are currently available.')

            has_active_booking = cls.objects.filter(
                student=student,
                book=locked_book,
                status__in=[cls.Status.BOOKED, cls.Status.BORROWED],
            ).exists()
            if has_active_booking:
                raise ValidationError('You already have an active booking for this book.')

            locked_book.available_copies -= 1
            locked_book.save(update_fields=['available_copies'])
            return cls.objects.create(student=student, book=locked_book, status=cls.Status.BOOKED)

    def cancel_by_student(self):
        if self.status != self.Status.BOOKED:
            raise ValidationError('Only booked items can be cancelled by students.')
        self._cancel_and_restore_inventory()

    def cancel_by_admin(self):
        if self.status != self.Status.BOOKED:
            raise ValidationError('Only booked items can be cancelled.')
        self._cancel_and_restore_inventory()

    def mark_as_borrowed(self):
        if self.status != self.Status.BOOKED:
            raise ValidationError('Only booked items can be marked as borrowed.')
        self.status = self.Status.BORROWED
        self.save(update_fields=['status', 'updated_at'])

    def mark_as_returned(self):
        if self.status != self.Status.BORROWED:
            raise ValidationError('Only borrowed items can be marked as returned.')

        with transaction.atomic():
            locked_book = Book.objects.select_for_update().get(pk=self.book.pk)
            locked_book.available_copies += 1
            if locked_book.available_copies > locked_book.total_copies:
                locked_book.available_copies = locked_book.total_copies
            locked_book.save(update_fields=['available_copies'])

            self.status = self.Status.RETURNED
            self.save(update_fields=['status', 'updated_at'])

    def _cancel_and_restore_inventory(self):
        with transaction.atomic():
            locked_book = Book.objects.select_for_update().get(pk=self.book.pk)
            locked_book.available_copies += 1
            if locked_book.available_copies > locked_book.total_copies:
                locked_book.available_copies = locked_book.total_copies
            locked_book.save(update_fields=['available_copies'])

            self.status = self.Status.CANCELLED
            self.save(update_fields=['status', 'updated_at'])
