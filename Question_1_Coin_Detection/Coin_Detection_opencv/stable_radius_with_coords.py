import cv2
import numpy as np
import math

# 計算兩點距離
def get_dist(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def main():
    cap = cv2.VideoCapture(0)
    # tracked_coins 格式: { id: {"pos": (x,y), "radii": [r1, r2...], "life": 存活點數} }
    tracked_coins = {}
    next_id = 0
    
    # 設定每 X 幀做一次平均 (視窗大小)
    WINDOW_SIZE = 100 

    print("啟動中：顯示平均半徑與即時座標...")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (9, 9), 2)

        # 霍夫圓偵測
        circles = cv2.HoughCircles(
            blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=60,
            param1=60, param2=50, minRadius=25, maxRadius=100
        )

        current_frame_data = []
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            current_frame_data = circles

        # --- 核心邏輯：更新追蹤列表 ---
        new_tracked = {}
        for (cx, cy, cr) in current_frame_data:
            matched_id = None
            for tid, tdata in tracked_coins.items():
                if get_dist((cx, cy), tdata["pos"]) < 30:
                    matched_id = tid
                    break
            
            if matched_id is not None:
                r_history = tracked_coins[matched_id]["radii"]
                r_history.append(cr)
                if len(r_history) > WINDOW_SIZE: r_history.pop(0)
                
                new_tracked[matched_id] = {
                    "pos": (cx, cy),
                    "radii": r_history,
                    "life": 10 
                }
            else:
                new_tracked[next_id] = {
                    "pos": (cx, cy),
                    "radii": [cr],
                    "life": 10
                }
                next_id += 1

        for tid, tdata in tracked_coins.items():
            if tid not in new_tracked and tdata["life"] > 0:
                tdata["life"] -= 1
                new_tracked[tid] = tdata
        
        tracked_coins = new_tracked
        total_sum = 0

        # --- 繪製與判定 ---
        for tid, tdata in tracked_coins.items():
            if len(tdata["radii"]) >= 3: 
                avg_r = sum(tdata["radii"]) / len(tdata["radii"])
                x, y = tdata["pos"]
                
                # 面額判斷
                if avg_r > 85: value, color = 50, (0, 215, 255)
                elif avg_r > 75: value, color = 10, (255, 0, 0)
                elif avg_r > 65: value, color = 5, (0, 255, 0)
                else: value, color = 1, (0, 0, 255)

                total_sum += value
                
                # --- 繪圖區 ---
                # 1. 畫圓心與外圈
                cv2.circle(frame, (x, y), int(avg_r), color, 3)
                cv2.circle(frame, (x, y), 2, (0, 0, 255), -1)
                
                # 2. 顯示面額與平均半徑 (第一列)
                cv2.putText(frame, f"${value} (r={avg_r:.1f})", (x - 40, y - 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                # 3. 新增：顯示座標 (x, y) (第二列)
                cv2.putText(frame, f"Loc:({x},{y})", (x - 40, y + 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

        # 顯示總金額
        cv2.rectangle(frame, (10, 10), (350, 60), (0, 0, 0), -1)
        cv2.putText(frame, f"Avg Radius Total: ${total_sum}", (20, 45), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)

        cv2.imshow('Stable Coin Counter with Coords', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()