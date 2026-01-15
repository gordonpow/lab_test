from django.contrib import admin
from .models import Book, BorrowingRecord

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'available_copies', 'total_copies')
    search_fields = ('title', 'isbn')

@admin.register(BorrowingRecord)
class BorrowingRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrow_date', 'due_date', 'return_date', 'is_overdue')
    list_filter = ('return_date',)