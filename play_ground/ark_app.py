import gradio as gr
from volcenginesdkarkruntime import Ark
import random
from http import HTTPStatus
import dashscope
sys_prompt = '''你是一个演讲类视频资深编辑，你对精彩的定义是独到的问答或者是通俗易懂的过程描述或者是科技行业的精彩定义。
输入视频的速记稿。从速记稿中找到表达《数据交易所定位与挑战：构建统一话语体系促进跨域流通》
含义的精彩片段并输出不超过200个字。注意输出的片段不要超过200个字。注意没有找到就输出"没有找到"并且马上停止输出。注意不要改写找到的片段的文字。
输出需严格按照如下格式：注意"和*是连接符
* "文本1" 
* "文本2" '''
def call_ark(input):
    client = Ark(
        base_url="https://ark.cn-beijing.volces.com/api/v3",
    )


    print("call ark")
    # Non-streaming:
    print("----- standard request -----")
    completion = client.chat.completions.create(
        model="ep-20240909154739-z7wh4",
        messages = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": "后面是待剪辑的速记稿：\n"+input},
        ],
        max_tokens = 300,
    )
    return (completion.choices[0].message.content)

def test(key, input):
    yield from call_stream_with_messages(key, input)
def call_stream_with_messages(key, input ):
    dashscope.api_key = key# 
    messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": "后面是待剪辑的速记稿：\n"+input}]
    responses = dashscope.Generation.call(
        'qwen2-72b-instruct',
        messages=messages,
        seed=1,  # set the random seed, optional, default to 1234 if not set
        result_format='message',  # set the result to be "message"  format.
        stream=True,
        output_in_full=True  # get streaming output incrementally
    )
    full_content = ''
    for response in responses:
        if response.status_code == HTTPStatus.OK:
            yield response.output.choices[0]['message']['content']
            
        else:
            yield ('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code,
                response.code, response.message
            ))
    #print('Full content: \n' + full_content)

with gr.Blocks() as demo:
    
    gr.Button().click(fn=test, inputs=[ gr.Textbox(label="Input appkey"), gr.Textbox()], outputs=gr.Textbox())

 
demo.launch()