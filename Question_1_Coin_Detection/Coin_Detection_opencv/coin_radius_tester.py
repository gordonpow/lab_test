import cv2
import numpy as np

def main():
    cap = cv2.VideoCapture(0)
    # 固定解析度，確保半徑數值穩定
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    print("--- 硬幣半徑校準模式 ---")
    print("請將不同面額的硬幣依序放入鏡頭，並記錄畫面上顯示的 r 值。")
    print("按 'q' 鍵退出")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break

        # 預處理：灰階 + 模糊
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.medianBlur(gray, 7)

        # 偵測圓形 (放寬 param2 讓你比較好抓到圓)
        circles = cv2.HoughCircles(
            blurred, 
            cv2.HOUGH_GRADIENT, dp=1.2, minDist=60,
            param1=70, param2=60, minRadius=20, maxRadius=120
        )

        if circles is not None:
            circles = np.uint16(np.around(circles[0, :]))
            for (x, y, r) in circles:
                # 畫出圓形邊界
                cv2.circle(frame, (x, y), r, (0, 255, 0), 2)
                # 畫出中心點
                cv2.circle(frame, (x, y), 2, (0, 0, 255), 3)
                
                # 重要：在畫面上顯示該圓形的半徑值 r
                cv2.putText(frame, f"r={r}", (x + 10, y + 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

        cv2.imshow('Radius Tester', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()