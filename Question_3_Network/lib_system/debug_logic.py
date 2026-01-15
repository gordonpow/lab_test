import os
import django
import sys
import re

# Add project root to path
sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lib_system.settings')
django.setup()

from catalog.models import Book

print("--- Testing Book Retrieval Logic ---")

# 1. Check if we have books
count = Book.objects.count()
print(f"Total books in DB: {count}")

if count < 2:
    print("Not enough books to test multiple recommendation. Creating dummy books.")
    if not Book.objects.filter(id=1).exists():
        Book.objects.create(id=1, title="Test Book 1", author="Author 1", isbn="111")
    if not Book.objects.filter(id=2).exists():
        Book.objects.create(id=2, title="Test Book 2", author="Author 2", isbn="222")

# 2. Simulate AI response with multiple books
ai_replies = [
    "推薦這本書 [BOOK_ID: 1] 和那本書 [BOOK_ID: 2]",
    "推薦:\n1. 書一 [BOOK_ID: 1]\n2. 書二 [BOOK_ID: 2]",
    "Book A [BOOK_ID: 1]. Book B [BOOK_ID: 2].",
]

for i, reply in enumerate(ai_replies):
    print(f"\nTest Case {i+1}:")
    print(f"Input: {reply}")
    
    match_ids = re.findall(r'\[BOOK_ID:\s*(\d+)\]', reply)
    print(f"Regex Matches: {match_ids}")
    
    unique_ids = list(set(match_ids))
    print(f"Unique IDs: {unique_ids}")
    
    if unique_ids:
        # Check if DB query works with strings
        books_query = Book.objects.filter(id__in=unique_ids)
        found_ids = [b.id for b in books_query]
        print(f"DB Found IDs: {found_ids}")
        
        if len(found_ids) == len(unique_ids):
            print("✅ SUCCESS: All IDs found.")
        else:
            print("❌ FAILURE: Missing books from DB.")
    else:
        print("❌ FAILURE: No IDs matched.")
