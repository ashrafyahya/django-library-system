from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render

from .models import Book, Booking


def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('book_list')
    return redirect('login')


@login_required
def book_list(request):
    books = Book.objects.select_related('category').all()
    return render(request, 'library/book_list.html', {'books': books})


@login_required
def my_bookings(request):
    bookings = Booking.objects.select_related('book').filter(student=request.user)
    return render(request, 'library/my_bookings.html', {'bookings': bookings})


@login_required
def create_booking(request, book_id):
    if request.method != 'POST':
        return redirect('book_list')

    book = get_object_or_404(Book, pk=book_id)
    try:
        Booking.create_booking(student=request.user, book=book)
        messages.success(request, 'Buchung erfolgreich erstellt.')
    except ValidationError as exc:
        messages.error(request, exc.message)

    return redirect('book_list')


@login_required
def cancel_booking(request, booking_id):
    if request.method != 'POST':
        return redirect('my_bookings')

    booking = get_object_or_404(Booking, pk=booking_id, student=request.user)
    try:
        booking.cancel_by_student()
        messages.success(request, 'Buchung wurde storniert.')
    except ValidationError as exc:
        messages.error(request, exc.message)

    return redirect('my_bookings')
