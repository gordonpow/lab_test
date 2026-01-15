# 智慧圖書館管理系統 (AI Library System)

這是一個基於 Django REST Framework 開發的圖書館管理系統，並整合了 Ollama AI 模型 (Qwen2) 來提供智慧書籍推薦服務。

---



## 功能特色 (Features)

### 1. 圖書管理 (Catalog)
- **書籍模型 (Book)**: 紀錄書名、作者、ISBN、總庫存與可借閱數量。
- **借閱紀錄 (BorrowingRecord)**: 自動計算到期日 (14天)，並支援還書功能。
- **庫存控制**: 借書時自動扣庫存，還書時自動加回；防止庫存錯誤。

### 2. 借閱 API
- **借書**: `POST /api/books/{id}/borrow/`
- **還書**: `POST /api/my-borrow/{id}/return_book/`
- **查詢個人借閱**: 只顯示當前登入使用者的紀錄。

### 3. AI 智慧圖書館員
- **整合 Ollama**: 透過本地運行的 Ollama 服務連接 `qwen2` 模型。
- **智慧推薦**:
    - 系統會將目前館藏書籍清單注入給 AI。
    - AI 根據使用者詢問 (例如：「我想學程式設計」) 推薦適合的書籍。
    - **結構化回應**: 後端會解析 AI 回覆中的 `[BOOK_ID]` 標記，並直接回傳書籍詳細資料 (JSON) 給前端。

---

## 系統架構流程圖

```mermaid
graph TD
    User[使用者/前端] -->|HTTP Request| Django[Django Backend]
    Django -->|CRUD| DB[(SQLite Database)]
    Django -->|Chat Prompt| AI["Ollama AI (Local)"]
    AI -->|Recommendation| Django
    Django -->|JSON Response| User
```

---

## 檔案功能與輸入輸出說明 (File Functions & I/O)

下表將各檔案功能與上方流程圖中的關鍵字 (**Django**, **DB**, **AI**, **User**) 對應，方便理解資料流向。

| 檔案 (File)          | 對應流程圖節點 (Flowchart Node) | 功能說明 (Function)                                                                       | 輸入 (Input)                                               | 輸出 (Output)                                                   |
| :------------------- | :------------------------------ | :---------------------------------------------------------------------------------------- | :--------------------------------------------------------- | :-------------------------------------------------------------- |
| **`views.py`**       | **Django**, **AI**              | **API 核心大腦**。<br>接收前端請求，判斷是否需要呼叫 `AI` 進行推薦，並執行資料庫 `CRUD`。 | **HTTP Request**<br>(e.g., POST `{"message": "學Python"}`) | **JSON Response**<br>(e.g., `{'reply': '...', 'books': [...]}`) |
| **`models.py`**      | **DB**                          | **資料庫藍圖**。<br>定義 `Book` 與 `BorrowingRecord` 的結構，對應實際的 SQLite 資料表。   | Django ORM 操作                                            | **SQLite Database** Table<br>(儲存書籍與借閱狀態)               |
| **`serializers.py`** | **Django**                      | **資料翻譯官**。<br>將複雜的 Python 物件轉換為 JSON 格式，方便傳回給 **User**。           | Python Model Objects                                       | JSON Data Dict                                                  |
| **`urls.py`**        | **Django**, **User**            | **門牌導引**。<br>將 **User** 的網址請求 (`/api/...`) 導向對應的 `views.py` 函式。        | URL Paths                                                  | View Functions                                                  |
| **`test_ai.py`**     | **AI**                          | **AI 連線測試**。<br>獨立測試 Django Server 與本地 **Ollama AI** 的連線狀況。             | 無 (內建字串 "hi")                                         | Console Prints<br>(顯示 AI 回覆內容)                            |
| **`manage.py`**      | **Django**                      | **系統管理員**。<br>啟動 Server 或更新 **DB** 架構。                                      | Terminal Commands                                          | System Actions                                                  |





## 成果展示 (Results Showcase)

### 1. 使用者介面

* **使用者初始介面** :使用者最一開始看到的界面。

    ![使用者初始介面](./img/使用者初始介面.png)
    ![使用者初始介面](./gif/使用者介面.gif)


### 2.搜尋功能

* **搜尋功能** :使用者可以輸入關鍵字或是ISBN來搜尋書籍。

    ![搜尋功能](./gif/搜尋功能.gif)

### 3. AI聊天機器人

* **AI聊天機器人** :使用者可以輸入自己想要看的領域或想要學習的主題，AI會回覆推薦的書籍。且可以直接顯示借閱書籍的按鈕。

    ![AI聊天機器人](./gif/機器人回答.gif)

### 4. 借閱功能

* **借閱功能** :使用者可以借閱書籍，借閱後會顯示借閱紀錄，且可以顯示借閱的書籍。

    ![借閱功能](./gif/借書功能.gif)

### 5. 借閱紀錄

* **借閱紀錄** :使用者可以查看自己的借閱紀錄，且顯示借閱的書籍、借閱日期、借閱到期日、借閱狀態。
  
  ![借閱紀錄](./gif/借閱紀錄.gif)

### 6. 還書功能

* **還書功能** :使用者可以在期限內還書，還書後該比資料會從借書紀錄消失，且庫存會加回。
  ![還書功能](./gif/還書功能.gif)

### 7. 深淺色模式

* **深淺色模式** :使用者可以切換深淺色模式，且可以儲存使用者的設定。

  ![深淺色模式](./gif/深淺模式切換.gif)