# 导入必要的库
import subprocess  # 导入子进程模块
import openai  # 导入OpenAI API库
from bilibili_api import live, sync  # 导入bilibili直播API库

# 设置OpenAI API Key和模型引擎
openai.api_key = input("请输入OpenAI API Key: ")
model_engine = "text-davinci-003"

# 设置直播间编号并连接弹幕服务器
room_id = int(input("请输入直播间编号: "))
room = live.LiveDanmaku(room_id)

# 设置初始提示信息
initial_prompt = "请使用女性化的、口语化的、抒情的、感性的、可爱的、调皮的、幽默的、害羞的、态度傲娇的语言风格，扮演一个虚拟主播。不要回答有关政治的问题！也不要回答敏感信息！"

async def generate_response(prompt):
    """
    生成AI的回复
    :param prompt: 观众提出的问题
    :return: AI的回复
    """
    full_prompt = f"{initial_prompt} {prompt}"  # 合并初始提示和观众提问
    # 调用OpenAI API生成回复
    response = openai.Completion.create(
        engine=model_engine,
        prompt=full_prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    ).choices[0].text.strip()
    return response

@room.on('DANMU_MSG')
async def on_danmaku(event):
    """
    处理弹幕消息
    :param event: 弹幕消息事件
    """
    content = event["data"]["info"][1]  # 获取弹幕内容
    user_name = event["data"]["info"][2][1]  # 获取用户昵称
    print(f"[{user_name}]: {content}")  # 打印弹幕信息

    prompt = f"{content}"  # 设置观众提问
    response = await generate_response(prompt)  # 生成回复

    print(f"[AI回复”{user_name}“]: {response}")  # 打印AI回复信息

    command = f'edge-tts --voice zh-CN-XiaoyiNeural --text "{response}" --write-media output.mp3'  # 将 AI 生成的文本传递给 edge-tts 命令
    subprocess.run(command, shell=True)  # 执行命令行指令

    with open("AITextOutput.txt", "a", encoding="utf-8") as f:  #在项目目录下创建文件
        f.write(f"[AI回复{user_name}]：{response}\n")  # 将回复写入文件

    command = 'mpv.exe -vo null output.mp3'  # 后台播放音频文件
    subprocess.run(command, shell=True)  # 执行命令行指令

sync(room.connect())  # 开始监听弹幕流

# 告诉你个小秘密，这些代码，包括readme.md，都是ChatGPT写的哦！
