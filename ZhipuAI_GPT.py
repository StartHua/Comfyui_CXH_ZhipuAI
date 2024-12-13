import os
import base64
import numpy as np
from PIL import Image,ImageOps, ImageFilter

import io
from zhipuai import ZhipuAI

import folder_paths

from openpyxl import Workbook
from openpyxl.drawing.image import Image as ExcelImage

from .tool import *


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
        
        content = get_key()
        self.index = 0
        self.keys = [key.strip() for key in content.split('\n') if key.strip()]
        if self.client == None:
            self.client = ZhipuAI(api_key=self.keys[0])


        start_tags(inputDir,self.client,prompt,saveExcel )
        return(inputDir,)
