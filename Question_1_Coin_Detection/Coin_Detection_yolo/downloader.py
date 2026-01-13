from icrawler.builtin import GoogleImageCrawler, BingImageCrawler

def download_images(keyword, max_num=100, save_dir='dataset'):
    """
    keyword: 搜尋關鍵字 (例如: "Taiwan 50 dollar coin")
    max_num: 預計下載數量
    save_dir: 儲存目錄
    """
    # 建議使用 Bing，因為 Google 的爬蟲限制較多且容易失敗
    crawler = BingImageCrawler(storage={'root_dir': f'{save_dir}/{keyword}'})
    
    print(f"正在搜尋並下載: {keyword}...")
    crawler.crawl(keyword=keyword, max_num=max_num)
    print(f"下載完成！存放在: {save_dir}/{keyword}")

if __name__ == "__main__":
    # 範例：下載各類硬幣
    # coin_types = ["Taiwan 50 dollar coin", "Taiwan 10 dollar coin", "Taiwan 1 dollar coin"]
    coin_types = ["Taiwan 5 dollar coin"]
    for coin in coin_types:
        download_images(coin, max_num=50)