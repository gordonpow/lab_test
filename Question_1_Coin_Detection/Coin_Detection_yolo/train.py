from ultralytics import YOLO
import os

def start_training():
    # 1. 指定你的 data.yaml 路徑 (請根據你解壓縮後的實際路徑修改)
    yaml_path = os.path.abspath("dataset/data.yaml")
    
    # 2. 載入 YOLOv11 預訓練模型 (n 代表 nano，速度最快)
    model = YOLO("yolo11m.pt") 

    # 3. 開始訓練
    print("開始訓練 YOLOv11 模型...")
    model.train(
        data=yaml_path,
        epochs=100,       # 訓練 100 輪，效果會比較穩
        imgsz=640,        # 使用我們建議的 640 尺寸
        device="0",     # 如果你有 NVIDIA 顯卡，可以改用 0
        project="runs/coin_project", 
        name="coin_yolo11",
        plots=True        # 產出訓練結果圖表
    )
    print("訓練完成！最佳模型儲存在：runs/coin_project/coin_yolo11/weights/best.pt")

if __name__ == "__main__":
    start_training()