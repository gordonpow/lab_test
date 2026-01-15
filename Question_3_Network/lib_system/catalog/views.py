from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.utils import timezone
from .models import Book, BorrowingRecord
from .serializers import BookSerializer, BorrowingRecordSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import ollama  # 匯入 Ollama
import re

# 1. 書籍 API (BookViewSet)
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author', 'isbn']

    # 自訂動作：借書
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def borrow(self, request, pk=None):
        book = self.get_object()
        
        # 檢查庫存
        if book.available_copies < 1:
            return Response({'error': '這本書已經被借光了'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 檢查該使用者是否已經借過這本且未還
        if BorrowingRecord.objects.filter(user=request.user, book=book, return_date__isnull=True).exists():
            return Response({'error': '您已經借閱過此書且尚未歸還'}, status=status.HTTP_400_BAD_REQUEST)

        # 建立借閱紀錄
        BorrowingRecord.objects.create(user=request.user, book=book)
        
        # 扣除庫存
        book.available_copies -= 1
        book.save()
        
        return Response({'status': '借閱成功', 'remaining_copies': book.available_copies})

# 2. 借閱紀錄 API (BorrowingRecordViewSet)
class BorrowingRecordViewSet(viewsets.ModelViewSet):
    serializer_class = BorrowingRecordSerializer
    permission_classes = [IsAuthenticated]

    # 只顯示「目前登入使用者」的紀錄
    def get_queryset(self):
        return BorrowingRecord.objects.filter(user=self.request.user).order_by('-borrow_date')

    # 自訂動作：還書
    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        record = self.get_object()
        
        if record.return_date:
            return Response({'error': '這本書已經還過了'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 更新還書時間
        record.return_date = timezone.now()
        record.save()
        
        # 加回庫存
        book = record.book
        book.available_copies += 1
        book.save()
        
        return Response({'status': '歸還成功'})

# 3. 網頁 View：首頁
def index(request):
    return render(request, 'catalog/index.html')

# 4. 網頁 View：我的書房
def my_books(request):
    return render(request, 'catalog/my_books.html')

# 5. 聊天機器人 View (使用本地 Ollama)
# 記得確認檔案最上面有這行匯入： from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def chatbot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')

            # 1. 撈出書籍
            books = Book.objects.all()
            book_list_text = "\n".join([f"- ID:{b.id} 書名:{b.title} (作者: {b.author}, 庫存: {b.available_copies})" for b in books])

            # 2. 設定「多書推薦版」Prompt
            system_prompt = f"""
            你是一個專業的圖書館管理員。

            [你的館藏列表]
            {book_list_text}
            
            [規則]
            1. 語言：必須全程使用「繁體中文」回答。
            2. 推薦策略：
               - 如果有多本適合的書，請「全部列出來」供讀者選擇。
               - 請依序介紹每一本書。
            3. 格式要求 (非常重要)：
               - 在你介紹完「每一本」書之後，緊接著在該段落後面加上 ID 暗號。
               - 格式為：[BOOK_ID: 數字]
               - 例如：推薦了《Python入門》(ID:5) 和 《AI 實戰》(ID:8)，你的回答應該像這樣：
                 「首先推薦《Python入門》，這本書很適合新手。[BOOK_ID: 5] 另外也推薦《AI 實戰》，適合進階學習。[BOOK_ID: 8]」
            """

            # 3. 呼叫 Ollama
            response = ollama.chat(model='qwen2', messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_message},
            ])

            ai_raw_reply = response['message']['content']

            # 4. 解析 AI 回覆，抓取「所有」的 [BOOK_ID: X]
            suggested_books = []
            
            # 使用 re.findall 找出所有的 ID
            # 修改: 忽略大小寫 (flags=re.IGNORECASE) 且允許冒號前後有空白
            match_ids = re.findall(r'\[BOOK_ID\s*:\s*(\d+)\]', ai_raw_reply, flags=re.IGNORECASE)
            
            # Debug: 印出 AI 回覆與抓到的 ID
            print(f"🤖 AI Reply: {ai_raw_reply}")
            print(f"🔍 Found IDs: {match_ids}")
            
            # 去除重複的 ID (避免 AI 重複標記同一本)
            unique_ids = list(set(match_ids))

            if unique_ids:
                # 一次從資料庫撈出這些書
                books_query = Book.objects.filter(id__in=unique_ids)
                
                for book in books_query:
                    suggested_books.append({
                        'id': book.id,
                        'title': book.title,
                        'author': book.author,
                        'available_copies': book.available_copies
                    })
                
                # 把暗號從文字中拿掉，讓畫面乾淨一點
                # 使用 re.sub 把所有 [BOOK_ID: ...] 替換成空字串
                ai_reply = re.sub(r'\[BOOK_ID\s*:\s*\d+\]', '', ai_raw_reply, flags=re.IGNORECASE)
            else:
                ai_reply = ai_raw_reply

            # 回傳 'books' (列表)，不再是單一 'book'
            return JsonResponse({'reply': ai_reply, 'books': suggested_books})

        except Exception as e:
            print("❌ AI 發生錯誤：", e)
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': '只限 POST 請求'}, status=400)