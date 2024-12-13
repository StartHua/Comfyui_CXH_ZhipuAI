from zhipuai import ZhipuAI

import folder_paths
import os
import base64

from PIL import Image,ImageOps, ImageFilter
import numpy as np
import io
import requests
from io import BytesIO
import torch

current_folder = os.path.dirname(os.path.abspath(__file__))
apiKeyFile = os.path.join(current_folder,"apiKey.txt")

def get_key():
    try:
        config_path = os.path.join(current_folder, 'apikey.txt')
        # 读取整个文件内容
        with open(config_path, 'r', encoding='utf-8') as file:
            content = file.read().strip()
            return content
    except:
        print("Error: Gemini API key is required")
        return ""

def tensor2pil(t_image: torch.Tensor)  -> Image:
    return Image.fromarray(np.clip(255.0 * t_image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

def pil2tensor(image:Image) -> torch.Tensor:
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

# 获取网络图片
def img_from_url(url):
    # 发送HTTP请求获取图片  
    response = requests.get(url)  
    response.raise_for_status()  # 如果请求失败，这会抛出异常
    # 将响应内容作为BytesIO对象打开，以便PIL可以读取它  
    image = Image.open(BytesIO(response.content))
    return image

# 获取所有图片文件路径
def get_all_image_paths(directory):
    image_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_paths.append(os.path.join(root, file))
    return image_paths

# 将图片转换为Base64编码
def image_to_base64(image_path):
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# 保存分析结果到txt文件
def save_to_txt(file_name, content):
    txt_file_path = os.path.splitext(file_name)[0] + '.txt'
    with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(content)
    print(f"文件 {txt_file_path} 已保存。")

def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

# pil转64
def pilTobase64(pil_image):

    byte_arr = io.BytesIO()
    pil_image.save(byte_arr, format='PNG')  
    byte_arr = byte_arr.getvalue() 

    image_base64 = base64.b64encode(byte_arr).decode('utf-8') 
    return image_base64