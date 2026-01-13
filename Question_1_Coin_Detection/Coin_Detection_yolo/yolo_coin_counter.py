import cv2
from ultralytics import YOLO

def main():
    # --- 1. 載入你訓練好的 YOLOv11 模型 ---
    # 請將 'your_model_path/best.pt' 替換為你實際的 best.pt 檔案路徑
    # 範例: model = YOLO(r"C:\AI_program\coin_1\coin_1\runs\coin_project\coin_yolo11\weights\best.pt")
    model = YOLO(r"runs\detect\runs\coin_project\coin_yolo112\weights\best.pt") # 假設 best.pt 在專案根目錄下的相對路徑

    # --- 2. 開啟相機 ---
    cap = cv2.VideoCapture(0) # 0 代表預設的網路攝影機
    if not cap.isOpened():
        print("錯誤: 無法開啟相機。請檢查相機是否連接正常或被其他程式占用。")
        return

    # --- 3. 定義硬幣面額對應表 ---
    # 請確保這個順序與你在 Roboflow 標註時的類別 (class) 順序一致
    # 範例: 如果你的 Roboflow class 0 是 1元, 1 是 5元, 2 是 10元, 3 是 50元
    coin_values = {
        0: 1,  # 假設 class 0 是 1元
        1: 10,  # 假設 class 1 是 5元
        2: 5, # 假設 class 2 是 10元
        3: 50  # 假設 class 3 是 50元
    }

    print("YOLOv11 硬幣辨識已啟動。按 'q' 鍵退出。")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("無法從相機讀取畫面。")
            break

        # --- 4. 執行 YOLO 辨識 ---
        # conf=0.5 表示只顯示信心值 (confidence) 高於 50% 的硬幣
        # imgsz=640 表示將輸入影像調整為 640x640 像素 (與訓練時尺寸一致)
        results = model(frame, conf=0.5, imgsz=640, verbose=False) # verbose=False 不顯示每次推論的日誌

        total_sum = 0
        
        # --- 5. 處理辨識結果並繪圖 ---
        for r in results: # r 包含了每個硬幣的資訊
            boxes = r.boxes # 取得所有偵測到的物件框
            for box in boxes:
                cls_id = int(box.cls[0]) # 硬幣的類別 ID (0, 1, 2, 3...)
                confidence = float(box.conf[0]) # 信心值
                x1, y1, x2, y2 = map(int, box.xyxy[0]) # 偵測框的座標

                # 根據類別 ID 取得面額
                value = coin_values.get(cls_id, 0)
                total_sum += value

                # 繪製辨識框和文字
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2) # 綠色框
                label = f"${value} ({confidence:.2f})"
                cv2.putText(frame, label, (x1, y1 - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # --- 6. 顯示總金額 ---
        cv2.rectangle(frame, (10, 10), (320, 60), (0, 0, 0), -1) # 黑色背景框
        cv2.putText(frame, f"TOTAL: ${total_sum}", (20, 45), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3) # 黃色文字

        # 顯示畫面
        cv2.imshow("YOLOv11 Coin Counter", frame)

        # 按 'q' 鍵退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # --- 7. 釋放資源 ---
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()