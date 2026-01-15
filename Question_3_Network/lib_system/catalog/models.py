from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# 1. 書籍模型
class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="書名")
    author = models.CharField(max_length=100, verbose_name="作者")
    isbn = models.CharField(max_length=13, unique=True, verbose_name="ISBN")
    total_copies = models.IntegerField(default=1, verbose_name="總館藏數")
    available_copies = models.IntegerField(default=1, verbose_name="目前可借數")
    
    def __str__(self):
        return self.title

# 2. 借閱紀錄模型
class BorrowingRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="借閱人")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="書籍")
    borrow_date = models.DateTimeField(auto_now_add=True, verbose_name="借出時間")
    due_date = models.DateTimeField(verbose_name="應還時間")
    return_date = models.DateTimeField(null=True, blank=True, verbose_name="歸還時間")

    # 儲存時自動計算到期日 (預設 14 天)
    def save(self, *args, **kwargs):
        if not self.id and not self.due_date:
            self.due_date = timezone.now() + timedelta(days=14)
        super().save(*args, **kwargs)

    # 判斷是否逾期
    @property
    def is_overdue(self):
        if self.return_date:
            return False # 已還書就不算逾期
        return timezone.now() > self.due_date

    def __str__(self):
        return f"{self.user.username} 借閱 {self.book.title}"