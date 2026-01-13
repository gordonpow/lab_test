import cv2
import numpy as np

def main():
    # 1. 開啟相機 (0 為預設鏡頭)
    cap = cv2.VideoCapture(0)
    

    print("正在啟動 OpenCV 硬幣偵測... 按 'q' 鍵退出")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # --- 影像預處理 ---
        # 轉成灰階
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 中值濾波 (減少雜訊，對圓形偵測很重要)
        blurred = cv2.medianBlur(gray, 7)

        # --- 霍夫圓變換 (Hough Circle Transform) ---
        # dp: 累加器解析度與影像解析度的反比 (1.2 是常用的值)
        # minDist: 兩個圓心之間的最短距離 (避免同一個硬幣偵測到多個圓)
        # param1: Canny 邊緣檢測的高門檻
        # param2: 圓心檢測門檻 (越小越靈敏，但也越多雜訊)
        circles = cv2.HoughCircles(
            blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=60,
            param1=60, param2=50, minRadius=25, maxRadius=120
        )

        total_sum = 0

        if circles is not None:
            # 將座標與半徑轉為整數
            circles = np.uint16(np.around(circles[0, :]))
            
            for (x, y, r) in circles:
                # --- 根據半徑判定面額 (這是你需要根據實際相機高度調整的地方) ---
                # 提示：你可以先印出 r 的值，看看 50 元在鏡頭下半徑是多少
                if r > 110:
                    value, color = 50, (0, 215, 255)  # 金色/黃色
                elif r > 100:
                    value, color = 10, (255, 0, 0)    # 藍色
                elif r > 91:
                    value, color = 5, (0, 255, 0)     # 綠色
                else:
                    value, color = 1, (0, 0, 255)     # 紅色
                
                total_sum += value

                # 畫出硬幣圓緣
                cv2.circle(frame, (x, y), r, color, 3)
                # 畫出圓心
                cv2.circle(frame, (x, y), 2, (0, 0, 255), 3)
                # 顯示單枚金額
                cv2.putText(frame, f"${value}", (x - 15, y - 5), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                cv2.putText(frame, f"r:{r}", (x - 15, y - 35), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        # --- 顯示總金額 ---
        cv2.rectangle(frame, (10, 10), (280, 60), (0, 0, 0), -1)
        cv2.putText(frame, f"Total Amount: ${total_sum}", (20, 45), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)

        # 顯示畫面
        cv2.imshow('OpenCV Coin Counter (Real-time)', frame)

        # 按 'q' 退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()