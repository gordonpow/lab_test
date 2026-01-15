# catalog/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# 自動產生網址
router = DefaultRouter()
router.register(r'books', views.BookViewSet)
router.register(r'my-records', views.BorrowingRecordViewSet, basename='my-records')

urlpatterns = [ 
    path('', views.index, name='index'),
    path('my-books/', views.my_books, name='my_books'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('', include(router.urls)),
   
]