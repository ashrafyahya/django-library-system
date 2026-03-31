from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Book, Booking, Category


class BookingWorkflowTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='student1', password='test12345')
        self.category = Category.objects.create(name='Programming')
        self.book = Book.objects.create(
            title='Django Basics',
            author='Team Tutorial',
            category=self.category,
            total_copies=3,
            available_copies=3,
        )

    def test_create_booking_reduces_available_copies(self):
        Booking.create_booking(self.user, self.book)
        self.book.refresh_from_db()
        self.assertEqual(self.book.available_copies, 2)

    def test_cancel_booking_increases_available_copies(self):
        booking = Booking.create_booking(self.user, self.book)
        booking.cancel_by_student()
        self.book.refresh_from_db()
        booking.refresh_from_db()
        self.assertEqual(self.book.available_copies, 3)
        self.assertEqual(booking.status, Booking.Status.CANCELLED)

    def test_returned_booking_restores_inventory(self):
        booking = Booking.create_booking(self.user, self.book)
        booking.mark_as_borrowed()
        booking.mark_as_returned()
        self.book.refresh_from_db()
        self.assertEqual(self.book.available_copies, 3)

    def test_cannot_book_unavailable_book(self):
        self.book.available_copies = 0
        self.book.save(update_fields=['available_copies'])
        with self.assertRaises(ValidationError):
            Booking.create_booking(self.user, self.book)
