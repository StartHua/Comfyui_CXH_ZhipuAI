import os
import base64
import numpy as np
from PIL import Image,ImageOps, ImageFilter

import io
from zhipuai import ZhipuAI

import folder_paths

from openpyxl import Workbook
from openpyxl.drawing.image import Image as ExcelImage

comfy_path = os.path.dirname(folder_paths.__file__)
custom_nodes_path = os.path.join(comfy_path, "custom_nodes")
apiKeyFile = os.path.join(custom_nodes_path,"Comfyui_CXH_ZhipuAI","apiKey.txt")

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

# 打标并保存结果
def start_tags(file_dir,client,prompt,saveExcel = False):
    image_paths = get_all_image_paths(file_dir)
    for image_path in image_paths:
        # 检查对应的txt文件是否已存在，如果存在则跳过打标
        txt_file_path = os.path.splitext(image_path)[0] + '.txt'
        if os.path.exists(txt_file_path):
            print(f"文件 {txt_file_path} 已存在，跳过打标。")
            continue

        print(image_path, '开始打标')
        image_base64 = image_to_base64(image_path)
        response = client.chat.completions.create(
            model="glm-4v",  # 填写需要调用的模型名称
            messages=[
                {"role": "user",
                 "content": [
                     {
                         "type": "text",
                         "text": prompt
                     },
                     {
                         "type": "image_url",
                         "image_url": {
                             "url": image_base64
                         }
                     }
                 ]
                 },
            ],
        )
        print(image_path, '打标结束')
        content = response.choices[0].message.content
        print(content)
        save_to_txt(image_path, content)
    if saveExcel ==True:
        # 属性:name image prompt
        # 创建新的Excel工作簿和工作表
        wbname = "prompts"
        wb = Workbook()
        ws = wb.active
        ws.title = wbname
        # 写入表头
        ws.append(["name", "image", "prompt"])
        width_row = 30
        # 设置列宽
        ws.column_dimensions['A'].width = width_row  
        ws.column_dimensions['B'].width = width_row +10 
        ws.column_dimensions['C'].width = 100  
         # 初始化行号，从2开始因为表头占据了第一行  
        row_number = 2
        # 获取所有文件
        files = os.listdir(file_dir)

        # 筛选出图片和对应的文本文件
        images = [f for f in files if f.endswith(('.png', '.jpg', '.jpeg'))]
        for image_name in images:
             # 构建对应的文本文件名
            txt_name = os.path.splitext(image_name)[0] + '.txt'
            txt_path = os.path.join(file_dir, txt_name)
            image_path = os.path.join(file_dir, image_name)
            # 读取文本文件内容
            prompt = ""
            if os.path.exists(txt_path):
                with open(txt_path, 'r', encoding='utf-8') as file:
                    prompt = file.read()

            # 添加行到Excel
            ws.append([image_name, "", prompt])
            # 将图片也插入到Excel中
            img = ExcelImage(image_path)
            img.anchor = f'B{row_number}'  # 设置图片插入的位置

            # 设置图片缩放
            original_img_height = Image.open(image_path).height
            scale_factor = 128 / original_img_height
            img.height = 128  # 设置图片高度为128像素
            img.width = int(Image.open(image_path).width * scale_factor)  # 调整宽度以保持比例
           
            ws.add_image(img)

            # 设置行高适配图片高度，Excel中的行高单位是点
            ws.row_dimensions[row_number].height = img.height * 0.75

            # 更新行号  
            row_number += 1
        # 保存工作簿
        print("保存成功！")
        savepath = os.path.join(file_dir,wbname+".xlsx")
        wb.save(savepath)

def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

# pil转64
def pilTobase64(pil_image):

    byte_arr = io.BytesIO()
    pil_image.save(byte_arr, format='PNG')  
    byte_arr = byte_arr.getvalue() 

    image_base64 = base64.b64encode(byte_arr).decode('utf-8') 
    return image_base64

# 单个图片反推
class ZhipuAI_single_trigger:
    def __init__(self):
        self.client = None

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "prompt":   ("STRING", {"multiline": True, "default": "请用英文详细描述这张图像，不要使用任何中文。英文输出。"},),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("out",)
    FUNCTION = "gen"
    OUTPUT_NODE = False
    CATEGORY = "CXH"

    def gen(self, image,prompt:str):
        
        with open(apiKeyFile, "r",encoding="utf-8") as file:
            content = file.read()
        if len(content) <=0:
            return ""
        if self.client == None:
            self.client = ZhipuAI(api_key=content)

        pil_image = tensor2pil(image)
        
        image_base64 = pilTobase64(pil_image)
        response = self.client.chat.completions.create(
            model="glm-4v",  # 填写需要调用的模型名称
            messages=[
                {"role": "user",
                 "content": [
                     {
                         "type": "text",
                         "text": prompt
                     },
                     {
                         "type": "image_url",
                         "image_url": {
                             "url": image_base64
                         }
                     }
                 ]
                 },
            ],
        )
        content = response.choices[0].message.content
        return(content,)

# 文件夹反推
class ZhipuAI_batch_trigger:
 
    def __init__(self):
        self.client = None

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "inputDir": ("STRING", {"multiline": False, "default": ""},),
                "prompt":   ("STRING", {"multiline": True, "default": "请用英文详细描述这张图像，不要使用任何中文。"},),
                "saveExcel": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("out",)
    FUNCTION = "gen"
    OUTPUT_NODE = False
    CATEGORY = "CXH"

    def gen(self, inputDir:str,prompt:str,saveExcel:bool):
        
        with open(apiKeyFile, "r",encoding="utf-8") as file:
            content = file.read()
        if len(content) <=0:
            return ""
        if self.client == None:
            self.client = ZhipuAI(api_key=content)


        start_tags(inputDir,self.client,prompt,saveExcel )
        return(inputDir,)
