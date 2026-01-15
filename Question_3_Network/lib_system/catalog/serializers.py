from rest_framework import serializers
from .models import Book, BorrowingRecord

# 1. 書籍序列化 (讓 API 吐出書籍資料)
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

# 2. 借閱紀錄序列化
class BorrowingRecordSerializer(serializers.ModelSerializer):
    book_title = serializers.ReadOnlyField(source='book.title') # 方便前端直接看書名

    class Meta:
        model = BorrowingRecord
        fields = ['id', 'user', 'book', 'book_title', 'borrow_date', 'due_date', 'return_date', 'is_overdue']
        read_only_fields = ['user', 'borrow_date', 'due_date', 'return_date'] 
        # 這些欄位由系統自動填寫，使用者不能改