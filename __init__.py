from .ZhipuAI_GPT import ZhipuAI_single_trigger
from .ZhipuAI_GPT import ZhipuAI_batch_trigger
# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "ZhipuAI_single_trigger":ZhipuAI_single_trigger,
    "ZhipuAI_batch_trigger":ZhipuAI_batch_trigger
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "ZhipuAI_single_trigger":"ZhipuAI_single_trigger",
    "ZhipuAI_batch_trigger":"ZhipuAI_batch_trigger"
}
