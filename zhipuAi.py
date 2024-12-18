from .tool import *
import time
import base64
# 文字
class CXH_ZhiPuAi_TX:

    def __init__(self):
        content = get_key()
        self.index = 0
        self.keys = [key.strip() for key in content.split('\n') if key.strip()]

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": (["glm-4-flash","glm-4-plus","glm-4", "glm-4-0520","glm-4-air","glm-4-flashx","glm-4-long","glm-4-airx"],),
                "system":("STRING", {"multiline": True, "default": "你是一个乐于解答各种问题的助手，你的任务是为用户提供专业、准确、有见地的建议。"},),
                "prompt":("STRING", {"multiline": True, "default": ""},), 
            }
        }

    RETURN_TYPES = ("STRING",) 
    RETURN_NAMES = ("out",)
    FUNCTION = "gen"
    OUTPUT_NODE = False 
    CATEGORY = "CXH/gemini"

    def gen(self,model,system,prompt):
        if len(self.keys) ==0 :
            print("请注册zhipuAi: https://www.bigmodel.cn/invite?icode=00e53ccPBd3LlcbyEEU8TkjPr3uHog9F4g5tjuOUqno%3D")

        #key
        if self.index >= len(self.keys):
            self.index = 0
        apikey = self.keys[self.index]
        client = ZhipuAI(api_key=apikey)
        self.index = self.index + 1

        response = client.chat.completions.create(
            model=model,  # 填写需要调用的模型编码
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ],
        )
        print(response)
        # 将结果列表中的张量连接在一起
        return (response.choices[0].message.content,)

# 单个图片反推
class CXH_ZhiPuAi_Vision:
    def __init__(self):
        content = get_key()
        self.index = 0
        self.keys = [key.strip() for key in content.split('\n') if key.strip()]
        # self.client = ZhipuAI(api_key=self.api_key)

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "model": (["glm-4v-flash","glm-4v-plus", "glm-4v"],),
                "prompt":   ("STRING", {"multiline": True, "default": "请用英文详细描述这张图像，不要使用任何中文。英文输出。"},),
                "type": (["video","image"],{'default': 'text'}),
                "video_path": ("STRING", {
                    "multiline": False,
                    "default": None
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("out",)
    FUNCTION = "gen"
    OUTPUT_NODE = False
    CATEGORY = "CXH"

    def gen(self, image,model,prompt:str, type:str, video_path=None):

        pil_image = tensor2pil(image)
        
        image_base64 = pilTobase64(pil_image)

        if len(self.keys) ==0 :
            print("请注册zhipuAi: https://www.bigmodel.cn/invite?icode=00e53ccPBd3LlcbyEEU8TkjPr3uHog9F4g5tjuOUqno%3D")

        #key
        if self.index >= len(self.keys):
            self.index = 0
        apikey = self.keys[self.index]
        client = ZhipuAI(api_key=apikey)
        self.index = self.index + 1
        if type=="image":
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
                ]
        if type=="video":
            if prompt == "":
                return ("请输入prompt",)
            with open(video_path, 'rb') as video_file:
                    video_base = base64.b64encode(video_file.read()).decode('utf-8')
            messages=[
            {
                "role": "user",
                "content": [
                {
                    "type": "video_url",
                    "video_url": {
                        "url" : video_base
                    }
                },
                {
                    "type": "text",
                    "text": prompt
                }
                ]
            }
            ]
        response = client.chat.completions.create(
            model=model,  # 填写需要调用的模型名称
            messages=messages
        )
        
        content = response.choices[0].message.content
        return(content,)
    
class CXH_ZhiPuAi_Cogview:
    def __init__(self):
        content = get_key()
        self.index = 0
        self.keys = [key.strip() for key in content.split('\n') if key.strip()]

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": (["cogview-3-plus","cogview-3"],),
                "prompt":   ("STRING", {"multiline": True, "default": "a girl"},),
                "size":(["1024x1024","768x1344","864x1152","1344x768","1152x864","1440x720","720x1440"],),
                "seed": ("INT", {"default": 656545, "min": 0, "max": 1000000}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("out",)
    FUNCTION = "gen"
    OUTPUT_NODE = False
    CATEGORY = "CXH"

    def gen(self, model,prompt:str,size,seed):

        if len(self.keys) ==0 :
            print("请注册zhipuAi: https://www.bigmodel.cn/invite?icode=00e53ccPBd3LlcbyEEU8TkjPr3uHog9F4g5tjuOUqno%3D")

        #key
        if self.index >= len(self.keys):
            self.index = 0
        apikey = self.keys[self.index]
        client = ZhipuAI(api_key=apikey)
        self.index = self.index + 1

        response = client.images.generations(
            model=model, #填写需要调用的模型编码
            prompt=prompt,
            size=size
        )

        url = response.data[0].url

        image2 = img_from_url(url)
        image2 = pil2tensor(image2) 

        return(image2,)
    
# 视频
class CXH_ZhiPuAi_TX_Video:
    def __init__(self):
        content = get_key()
        self.index = 0
        self.keys = [key.strip() for key in content.split('\n') if key.strip()]

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": (["cogvideox"],),
                "prompt":   ("STRING", {"multiline": True, "default": "比得兔开小汽车，游走在马路上，脸上的表情充满开心喜悦。"},),
                "quality": (["quality","speed"],),
                "with_audio": ("BOOLEAN", {"default": True}),
                "seed": ("INT", {"default": 656545, "min": 0, "max": 1000000}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("out",)
    FUNCTION = "gen"
    OUTPUT_NODE = False
    CATEGORY = "CXH"

    def gen(self, model,prompt,quality,with_audio,seed):

        if len(self.keys) ==0 :
            print("请注册zhipuAi: https://www.bigmodel.cn/invite?icode=00e53ccPBd3LlcbyEEU8TkjPr3uHog9F4g5tjuOUqno%3D")

        #key
        if self.index >= len(self.keys):
            self.index = 0
        apikey = self.keys[self.index]
        client = ZhipuAI(api_key=apikey)
        self.index = self.index + 1

        response = client.videos.generations(
            model=model,
            prompt=prompt,
            quality = quality,
            with_audio=with_audio
        )
        id = response.id
        print(id)
        return(id,)

class CXH_ZhiPuAi_Img_Video:
    def __init__(self):
        content = get_key()
        self.index = 0
        self.keys = [key.strip() for key in content.split('\n') if key.strip()]

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "model": (["cogvideox"],),
                "prompt":   ("STRING", {"multiline": True, "default": "让画面动起来"},),
                "size":(["720x480","1024x1024","1280x960","960x1280","1920x1080","1080x1920","2048x1080","3840x2160"],),
                "quality": (["quality","speed"],),
                "with_audio": ("BOOLEAN", {"default": True}),
                "duration": ("INT", {"default": 5, "min": 1, "max": 1024}),
                "fps": ("INT", {"default": 30, "min": 1, "max": 120}),
                
                "seed": ("INT", {"default": 656545, "min": 0, "max": 1000000}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("out",)
    FUNCTION = "gen"
    OUTPUT_NODE = False
    CATEGORY = "CXH"

    def gen(self, image,model,prompt,size,quality,with_audio,duration,fps,seed):
        
        if len(self.keys) ==0 :
            print("请注册zhipuAi: https://www.bigmodel.cn/invite?icode=00e53ccPBd3LlcbyEEU8TkjPr3uHog9F4g5tjuOUqno%3D")

       
        #key
        if self.index >= len(self.keys):
            self.index = 0
        apikey = self.keys[self.index]
        client = ZhipuAI(api_key=apikey)
        self.index = self.index + 1

        pil_image = tensor2pil(image)
        
        image_base64 = pilTobase64(pil_image)
        

       # 调用视频生成接口
        response = client.videos.generations(
            model=model,  # 使用的视频生成模型
            image_url=image_base64,  # 提供的图片URL地址或者 Base64 编码
            prompt=prompt,  
            quality=quality,  # 输出模式，"quality"为质量优先，"speed"为速度优先
            with_audio=with_audio,
            size=size,  # 视频分辨率，支持最高4K（如: "3840x2160"）
            duration=duration,  # 视频时长，可选5秒或10秒
            fps=fps,  # 帧率，可选为30或60
        )

        id = response.id
        print(id)
        return(id,)



class CXH_ZhiPuAi_Retrieve_Video:
    def __init__(self):
        content = get_key()
        self.index = 0
        self.keys = [key.strip() for key in content.split('\n') if key.strip()]

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "id":   ("STRING", {"multiline": False, "default": "","forceInput": True},),
                "delay":("INT", {"default": 10}),
                "second":("INT", {"default": 5}),
                "repeat":("INT", {"default": 40}),
                "seed": ("INT", {"default": 656545, "min": 0, "max": 1000000}),
            }
        }

    RETURN_TYPES = ("IMAGE","STRING")
    RETURN_NAMES = ("image","video_url")
    FUNCTION = "gen"
    OUTPUT_NODE = False
    CATEGORY = "CXH"

    def gen(self, id,delay,second,repeat,seed):

        if len(self.keys) ==0 :
            print("请注册zhipuAi: https://www.bigmodel.cn/invite?icode=00e53ccPBd3LlcbyEEU8TkjPr3uHog9F4g5tjuOUqno%3D")

        #key
        if self.index >= len(self.keys):
            self.index = 0
        apikey = self.keys[self.index]
        client = ZhipuAI(api_key=apikey)
        self.index = self.index + 1

        print("任务id:" + id)
        print("等待执行任务......")
        time.sleep(delay) 
        #轮询
        wait_req = True
        repeat_temp = repeat
        image_url = None
        video_url = None
        while wait_req: 
            response = client.videos.retrieve_videos_result(
                id=id
            )
            print(response)
            # 检查请求是否成功  
            task_status = response.task_status
            if task_status != "SUCCESS":
                time.sleep(second)  # 阻塞等待 
                repeat_temp = repeat_temp - 1
                if repeat_temp <= 0 :
                    wait_req = False 
                print("轮询:" + str(repeat_temp))
            else:
                first_result = response.video_result[0]  # 获取列表的第一个元素
                video_url  = first_result.url
                image_url = first_result.cover_image_url 
                wait_req = False 

        if image_url == None or video_url == None:
            print("没有获取到数据！")

        source_img = img_from_url(image_url)
        source_img = pil2tensor(source_img)
        
        return(source_img,video_url,)