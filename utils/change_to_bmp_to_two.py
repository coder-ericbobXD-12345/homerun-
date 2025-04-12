from PIL import Image
from datetime import datetime

def bmp_two(photo_path):
    # 讀取原始圖片
    input_path = photo_path
    output_path = f"static/bmp_{datetime.now().timestamp()}"

    # 打開圖片
    img = Image.open(input_path)

    # 轉換為灰階並裁剪（如果需要）
    # 這裡根據圖片內容選擇適合的範圍來裁剪，只保留波形部分
    cropped_img = img.crop((50, 50, 1150, 550))  # 調整範圍來適配波形

    # 調整大小為 128x64 來適應 SSD1306
    resized_img = cropped_img.resize((128, 64)).convert("1")  # 轉換為 1-bit 單色

    # 儲存為 BMP 格式（1-bit 單色）
    resized_img.save(output_path, format="BMP")

    return output_path