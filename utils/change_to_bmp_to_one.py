from PIL import Image
from datetime import datetime

def bmp_one(photo_path):
    # 讀取原始圖片
    input_path = photo_path
    output_path = f"static/bmp_{datetime.now().timestamp()}"

    # 打開圖片
    img = Image.open(input_path)

    # 裁剪圖片 (只保留波形)
    # 根據圖片比例，去除標題、標籤，保留主要的波形區域
    cropped_img = img.crop((50, 100, 950, 350))  # 調整這些數值來適應波形

    # 調整大小為 128x64 適配 SSD1306
    resized_img = cropped_img.resize((128, 64)).convert("1")  # 轉換為單色

    # 儲存為 BMP 格式（1-bit 單色）
    resized_img.save(output_path, format="BMP")

    return output_path