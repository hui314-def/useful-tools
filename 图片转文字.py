import cv2,pytesseract

image_path = '2.jpg' # 替换为你的图片路径
if image_path:
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # 转为灰度图像（可选，提升识别率）
    _,binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) # 二值化处理
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' # 指定OCR文件路径，需要自己额外按照
    text = pytesseract.image_to_string(binary, lang = 'chi_sim').replace(' ', '') # 使用pytesseract识别文字 中文用'chi_sim'，英文用'eng'
    print(text)
    with open('output.txt', 'w', encoding='utf-8') as f: # 保存到txt文件
        f.write(text)