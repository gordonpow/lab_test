import cv2
import os

def process_all_videos(base_video_dir, base_output_dir, frame_interval=10):
    """
    掃描 base_video_dir 下的所有子資料夾，並將影片拆解成圖片
    """
    # 支援的影片格式
    valid_extensions = ('.mp4', '.avi', '.mov', '.mkv')

    # 走訪 video 資料夾 (例如: video/1, video/5...)
    for subdir in os.listdir(base_video_dir):
        video_subdir_path = os.path.join(base_video_dir, subdir)
        
        # 確保它是資料夾（例如 1, 5, 10, 50）
        if os.path.isdir(video_subdir_path):
            # 建立對應的輸出資料夾 (例如: dataset/1, dataset/5...)
            output_subdir_path = os.path.join(base_output_dir, subdir)
            if not os.path.exists(output_subdir_path):
                os.makedirs(output_subdir_path)
            
            # 處理該資料夾下的所有影片檔案
            for file in os.listdir(video_subdir_path):
                if file.lower().endswith(valid_extensions):
                    video_path = os.path.join(video_subdir_path, file)
                    extract_frames(video_path, output_subdir_path, subdir, file, frame_interval)

def extract_frames(video_path, output_folder, label, video_name, frame_interval):
    cap = cv2.VideoCapture(video_path)
    count = 0
    saved_count = 0
    
    # 取得影片純檔名，避免存檔衝突
    pure_name = os.path.splitext(video_name)[0]
    
    print(f"正在處理: {label}元影片 -> {video_name}")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        if count % frame_interval == 0:
            # 檔名加入影片原名，確保唯一性
            file_name = f"{pure_name}_f{saved_count:04d}.jpg"
            save_path = os.path.join(output_folder, file_name)
            cv2.imwrite(save_path, frame)
            saved_count += 1
            
        count += 1
    
    cap.release()
    print(f"  └─ 完成！儲存了 {saved_count} 張圖片。")

if __name__ == "__main__":
    # 設定你的影片路徑與輸出路徑
    VIDEO_DIR = "video_mix"      # 你的影片根目錄
    OUTPUT_DIR = "dataset"   # 圖片儲存根目錄
    
    process_all_videos(VIDEO_DIR, OUTPUT_DIR, frame_interval=10)