import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from catalog.models import Book
import random
import time

class Command(BaseCommand):
    help = '從博客來搜尋並抓取書籍資料 (進階版)'

    def add_arguments(self, parser):
        parser.add_argument('keyword', type=str, help='要搜尋的書籍關鍵字')

    def handle(self, *args, **options):
        keyword = options['keyword']
        self.stdout.write(f'正在搜尋關鍵字: {keyword} ...')

        # 1. 修正網址：使用博客來目前的搜尋格式
        url = f"https://search.books.com.tw/search/query/key/{keyword}/cat/all"
        
        # 2. 更換成更完整的 Header (模擬真實瀏覽器行為)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Referer': 'https://www.books.com.tw/',
        }

        try:
            # 休息 1 秒再發請求，避免太快被擋
            time.sleep(1)
            response = requests.get(url, headers=headers)
            
            # 檢查連線狀態
            if response.status_code != 200:
                self.stdout.write(self.style.ERROR(f'連線被拒絕，狀態碼: {response.status_code}'))
                return

            soup = BeautifulSoup(response.text, 'html.parser')

            # --- 除錯區塊 ---
            # 將抓到的內容存檔，方便檢查 (會在專案根目錄產生一個 debug_books.html)
            with open('debug_books.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            self.stdout.write(f'已將網頁內容存為 debug_books.html，若無資料請檢查此檔案。')
            # ----------------

            # 3. 嘗試多種不同的 HTML 結構 (因為博客來搜尋頁有時是列表，有時是表格)
            # 策略 A: 找搜尋結果的標題 (通常是 h3 或 h4)
            # 博客來目前的結構通常是 h4 > a
            book_titles = soup.select('h4 a') # 這是 CSS Selector 写法
            
            # 如果策略 A 找不到，嘗試策略 B (找 class="box_1")
            if not book_titles:
                self.stdout.write('策略 A (h4 a) 找不到，嘗試策略 B...')
                book_titles = soup.select('.box_1 a')

            count = 0
            for link in book_titles:
                if count >= 10:
                    break
                
                # 取得書名
                title = link.text.strip()
                # 排除空標題或太短的雜訊
                if not title or len(title) < 2:
                    continue

                # 嘗試找作者 (往上找父元素，再找同層級的作者區塊)
                # 這邊簡化處理：如果找不到就填 "未知作者"
                author = "未知作者"
                try:
                    # 往上找兩層回到 item container
                    item_container = link.find_parent('div', class_='box_1') or link.find_parent('tr')
                    if item_container:
                        # 嘗試找作者連結
                        author_link = item_container.select_one('a[rel="go_author"]')
                        if author_link:
                            author = author_link.text.strip()
                except:
                    pass

                fake_isbn = f"978{random.randint(1000000000, 9999999999)}"

                book, created = Book.objects.get_or_create(
                    title=title,
                    defaults={
                        'author': author,
                        'isbn': fake_isbn,
                        'total_copies': 3,
                        'available_copies': 3
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f'成功新增: {title} (作者: {author})'))
                    count += 1
                else:
                    self.stdout.write(f'書籍已存在: {title}')

            if count == 0:
                self.stdout.write(self.style.WARNING('仍然找不到書籍。請打開 debug_books.html 檢查是否出現驗證碼或被擋。'))
            else:
                self.stdout.write(self.style.SUCCESS(f'爬蟲結束，共新增 {count} 本書。'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'發生錯誤: {e}'))