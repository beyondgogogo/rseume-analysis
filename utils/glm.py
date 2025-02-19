from zhipuai import ZhipuAI

def chat_with_ai(role, message):
# def chat_with_ai(role, message):
    """
    Function to interact with ZhipuAI chat model.

    Args:
        role (str): The role of the message sender (e.g., 'user').
        message (str): The content of the message to send.

    Returns:
        str: The AI's response message.
    """
    client = ZhipuAI(api_key="98b61ac3fe74307b7549915437425356.xmyraauKeGEOTaZP")
    response = client.chat.completions.create(
        model="glm-4-flash",
        messages=[
            {"role": role, "content": message},
        ],
    )
    return response.choices[0].message.content

def chat_with_ai2(role, message):
# def chat_with_ai(role, message):
    """
    Function to interact with ZhipuAI chat model.

    Args:
        role (str): The role of the message sender (e.g., 'user').
        message (str): The content of the message to send.

    Returns:
        str: The AI's response message.
    """
    client = ZhipuAI(api_key="649899d0531f4658960a3f5e2b0baf58.MoQilyeyilv2FuHA")
    response = client.chat.completions.create(
        model="glm-4-flash",
        messages=[
            {"role": role, "content": message},
        ],
    )
    return response.choices[0].message.content

# # Example usage:
# role = "user"
# message = ("你好")
# response_message = chat_with_ai(role, message)
# print(response_message)
