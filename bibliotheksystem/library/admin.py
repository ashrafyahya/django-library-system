from django.contrib import admin
from django.core.exceptions import ValidationError

from .models import Book, Booking, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'total_copies', 'available_copies')
    list_filter = ('category',)
    search_fields = ('title', 'author')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('student', 'book', 'status', 'booked_at', 'updated_at')
    list_filter = ('status',)
    search_fields = ('student__username', 'book__title')
    actions = ('action_cancel', 'action_mark_borrowed', 'action_mark_returned')

    @admin.action(description='Set selected bookings to cancelled')
    def action_cancel(self, request, queryset):
        updated = 0
        for booking in queryset:
            try:
                booking.cancel_by_admin()
                updated += 1
            except ValidationError:
                continue
        self.message_user(request, f'{updated} booking(s) set to cancelled.')

    @admin.action(description='Set selected bookings to borrowed')
    def action_mark_borrowed(self, request, queryset):
        updated = 0
        for booking in queryset:
            try:
                booking.mark_as_borrowed()
                updated += 1
            except ValidationError:
                continue
        self.message_user(request, f'{updated} booking(s) set to borrowed.')

    @admin.action(description='Set selected bookings to returned')
    def action_mark_returned(self, request, queryset):
        updated = 0
        for booking in queryset:
            try:
                booking.mark_as_returned()
                updated += 1
            except ValidationError:
                continue
        self.message_user(request, f'{updated} booking(s) set to returned.')
