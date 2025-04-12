## 這裡是我們主要的程式碼放置資料夾
### 1. __init__.py
統整下面程式碼的函式，讓我在main.py比較好引用
### 2. transform.py
這就是我們把音檔轉成波型圖和頻譜圖
### 3. compare_photo.py
比較兩個音檔的波型圖與頻譜圖
### 4. compare_math.py
比較兩個音檔的相似程度，方法如下: 
- mfcc (Mel-Frequency Cepstral Coefficients)
- dtw (Dynamic Time Warping)
- cosine similarity
### 5. encode.py
用AES-CBC加密方式加密音檔，並回傳密鑰
### 6. decode.py
接收密鑰，才會解密
### 7. save_file.py
把音檔或圖片存到static資料夾裡面
### 8. change_to_bmp_to_one.py & change_to_bmp_to_one.py
都是把檔案轉成bmp檔，這樣才能在ssd1306上面顯示
