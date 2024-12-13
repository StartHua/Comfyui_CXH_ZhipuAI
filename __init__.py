
from .ZhipuAI_GPT import ZhipuAI_batch_trigger
from .zhipuAi import CXH_ZhiPuAi_Vision,CXH_ZhiPuAi_TX,CXH_ZhiPuAi_Cogview,CXH_ZhiPuAi_Retrieve_Video,CXH_ZhiPuAi_TX_Video,CXH_ZhiPuAi_Img_Video
# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "ZhipuAI_batch_trigger":ZhipuAI_batch_trigger,
    "CXH_ZhiPuAi_Vision":CXH_ZhiPuAi_Vision,
    "CXH_ZhiPuAi_TX":CXH_ZhiPuAi_TX,
    "CXH_ZhiPuAi_Cogview":CXH_ZhiPuAi_Cogview,
    "CXH_ZhiPuAi_TX_Video":CXH_ZhiPuAi_TX_Video,
    "CXH_ZhiPuAi_Retrieve_Video":CXH_ZhiPuAi_Retrieve_Video,
    "CXH_ZhiPuAi_Img_Video":CXH_ZhiPuAi_Img_Video
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "CXH_ZhiPuAi_Vision":"CXH_ZhiPuAi_Vision",
    "CXH_ZhiPuAi_TX":"CXH_ZhiPuAi_TX",
    "ZhipuAI_batch_trigger":"ZhipuAI_batch_trigger",
    "CXH_ZhiPuAi_Cogview":"CXH_ZhiPuAi_Cogview",
    "CXH_ZhiPuAi_TX_Video":"CXH_ZhiPuAi_TX_Video",
    "CXH_ZhiPuAi_Retrieve_Video":"CXH_ZhiPuAi_Retrieve_Video",
    "CXH_ZhiPuAi_Img_Video":"CXH_ZhiPuAi_Img_Video"
}
