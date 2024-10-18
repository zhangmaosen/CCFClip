
import pysubs2

from ollama import Client, AsyncClient
from rapidfuzz import fuzz
from datetime import datetime
import pytz
import ffmpeg
import re
import os
import shutil
import dashscope
from gradio_streamvideo import StreamVideo
import time
from http import HTTPStatus
import asyncio
from moviepy.editor import *
from pypinyin import lazy_pinyin
def save_video(video, target_path):
    """
    Saves the uploaded video to the specified target path.
    
    :param video: The uploaded video file.
    :param target_path: The directory where the video should be saved.
    :return: Path to the saved video.
    """
    # Ensure the directory exists
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    
    # Save the video
    shutil.move(video.name, target_path)
    return None
def load_srt_file(srt_file):
    with open(srt_file, 'r') as f:
        srt_text = f.read()
    return [srt_text, len(srt_text)]

from langchain_experimental.text_splitter import SemanticChunker
from langchain_ollama import OllamaEmbeddings


from langchain_core.documents import BaseDocumentTransformer, Document
import itertools
def chunk_run_model(system_prompt,docs, model_select,  user_prompt,  temperature=0.1, num_ctx=30000,keep_alive=-1, num_predict=150):
    all = ""
    for doc in docs:

        if len(doc.page_content) <=2:
            continue
        #print(f"doc is <{doc.page_content}>")
        for out in  run_model(system_prompt, doc.page_content, model_select,  user_prompt,  temperature=temperature, num_ctx=num_ctx,keep_alive=keep_alive, num_predict=num_predict):
            yield all+f"{out.strip()}"
        all += f"{out.strip()}" + "\n"
        yield all

def load_d_templates(d_templates):
    t_p_dic ={
        "科普类":'''你是一名科普类短视频博主，你的主要观众在小红书。你需要从科技类演讲的速记稿中寻找适合做科普短视频的案例和包含案例前因后果的具体文字。你需要对速记稿中的每一个案例内容进行仔细打分，得分点如下：
1. 故事情节的完整程度，加0到10分
3. 激发读者的画面感的生动程度，加0到10分
4. 细节动作描写的连贯程度，加0到10分
5. 文字中提到日常工作生活会用到的物品的流行程度，加0到10分
6. 问题解决前后对比的差异程度，加0-10分
7. 面向观众人群理解的通俗程度，加0-10分
打分过程示例：
得分点1得分5分，得分点2得分3分，得分点3得分0分。最后得分：5+3+0=8 分
你需要一步一步的思考如何完成工作，先找出符合需求的案例进行打分，再输出得分最高的5个案例。
输出的格式如下：
第一步：找出案例并打分
1. 案例：[案例的具体文字]，得分点：[得分点]，分数：[分数]，
1. 案例：[案例的具体文字]，得分点：[得分点]，分数：[分数]，
第二步：输出得分最高的5个案例''',


        "教培类":'''你是一名科普类短视频博主，你的主要观众在小红书。你需要从科技类演讲的速记稿中寻找适合做科普短视频的案例和包含案例前因后果的具体文字。你需要对速记稿中的每一个案例内容进行仔细打分，注意你打分的评价标准是参加信息学竞赛的家长的接受度和喜爱程度。得分点如下：
1. 故事情节的完整程度，加0到10分
3. 激发读者的画面感的生动程度，加0到10分
4. 细节动作描写的连贯程度，加0到10分
5. 文字中提到日常工作生活会用到的物品的流行程度，加0到10分
6. 问题解决前后对比的差异程度，加0-10分
7. 面向观众人群理解的通俗程度，加0-10分
8. 引发家长的焦虑程度，加0-10分
打分过程示例：
得分点1得分5分，得分点2得分3分，得分点3得分0分。最后得分：5+3+0=8 分
你需要一步一步的思考如何完成工作，先找出符合需求的案例进行打分，再输出得分最高的5个案例。
输出的格式如下：
第一步：找出案例并打分
1. 案例：[案例的具体文字]，得分点：[得分点]，分数：[分数]，
1. 案例：[案例的具体文字]，得分点：[得分点]，分数：[分数]，
第二步：输出得分最高的5个案例''',



        "爱国类":"",
    }
    return  t_p_dic[d_templates]
def gen_full_text(srt_file, path = ''):
    # #print(f"srt_file:{srt_file}")
    # if os.path.isabs(srt_file):
    #     srt_file = srt_file
    # else:
    srt_file = os.path.join(path, srt_file)
    subs = pysubs2.load(srt_file)
    full_txt = ''
    for line in subs:
        full_txt += line.text + '\n'

    return [ len(full_txt), full_txt, subs.to_string('srt')]

def load_text_from_srt(srt_file, path = ''):
    if srt_file is None:
        return ["",""]
    #print(f"srt_file:{srt_file}")
    srt_file = os.path.join(path, srt_file)
    subs = pysubs2.load(srt_file)
    full_txt = ''
    for line in subs:
        full_txt += line.text + '\n'

    return [full_txt, subs.to_string('srt')]
def gen_key_words( target, like):
    format_str = """你是严格按照工作要求的句子剪辑器。你的输入是现场演讲的速记稿。注意你需要对速记稿从前到后分析后，才能开始剪辑。你需要发现打动人心的文字或者案例。你的工作需要分步骤完成：
* 面向{}人群的需求，输出不超过7个片段的小标题，输出案例摘要，案例关键词，输出案例内容中的日常物品
* 根据{}的喜好，从上一步的案例中再筛选出不超过5个的案例并输出
注意如果没有找到就输出没有并终止输出。注意匹配出的句子需要保持原文。注意输出格式：
-  “输出”
- """
    return format_str.format(target, like)
    
def gen_system_prompt(target, like, style, key_words, topic):
    if key_words == "":
        prev = """你是严格按照工作要求的句子剪辑器。你的输入是现场演讲的速记稿。注意输出的是速记稿中的原文段落，注意需要对输出的内容添加上标点符号。你的工作需要分步骤完成：\n"""
        content = ""
        for key in key_words.split(' '):
         
            content += f"""* 输出 '{topic}' 主题匹配的全部原文\n* 输出它的前一个段落\n* 输出它的后一个段落\n"""
        post = """注意如果没有找到就输出没有并终止输出。注意匹配出的句子需要保持原文。注意输出格式，\“\”是连接符号：
- 输出“每步的输出”"""
        return prev + content + post
    else: 
        prev = """你是严格按照工作要求的句子剪辑器。你的输入是现场演讲的速记稿。注意输出的是速记稿中的原文段落，注意需要对输出的内容添加上标点符号。你的工作需要分步骤完成：\n"""
        content = ""
        for key in key_words.split(' '):
         
            content += f"""* 输出 {key} 所在的段落\n* 输出它的前一个段落\n* 输出它的后一个段落\n"""
        post = """注意如果没有找到就输出没有并终止输出。注意匹配出的句子需要保持原文。注意输出格式，\“\”是连接符号：
- 输出“每步的输出”"""
        return prev + content + post
def call_stream_with_messages(full_text, model_select, system_prompt, user_prompt,  temperature=0.1, num_predict=3000, key = None ):
    print('call online model')
    dashscope.api_key = key # 
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt+full_text}]
    responses = dashscope.Generation.call(
        'qwen2-72b-instruct',
        messages=messages,
        seed=1,  # set the random seed, optional, default to 1234 if not set
        result_format='message',  # set the result to be "message"  format.
        stream=True,
        output_in_full=True,  # get streaming output incrementally
        temperature=temperature,
        max_tokens=num_predict

    )

    for response in responses:
        if response.status_code == HTTPStatus.OK:
            print(response.output.choices[0]['message']['content'])
            yield response.output.choices[0]['message']['content']
        else:
            yield ('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code,
                response.code, response.message
            ))

async def run_model(system_prompt, full_text, model_select, user_prompt,  temperature=0.1, num_ctx=30000,keep_alive=-1, num_predict=250, local_or_online='local', key=None, stream=False):
    #print(f"full_text is {full_text}")
    if local_or_online == 'local':
        pre_out = ""
        ollama = AsyncClient() #(host="100.103.46.96")
        print(f"full_text is {full_text}, system_prompt is {system_prompt}\
            user_prompt is {user_prompt}\
                temperature is {temperature}\
                    num_ctx is {num_ctx}\
                        num_predict is {num_predict}\
                            ")
        try:
            async for chunk in await ollama.chat(model=model_select, messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt.format(full_text)  }
            ],options= {
                "num_ctx": num_ctx ,
                "temperature" : temperature,
                'num_predict' : num_predict
            }, keep_alive=keep_alive, stream=True):
                if stream == False:
                    pre_out = pre_out + chunk['message']['content']
                else:
                    yield chunk['message']['content']
                #print(pre_out)
                yield pre_out
        except TimeoutError as t:
            
            print(t)
    #print(part['message']['content'], end='', flush=True)
    elif local_or_online == 'online':
         
        yield  call_stream_with_messages(full_text, model_select, system_prompt, user_prompt,  temperature, num_predict, key)



def invert_find(short_text,srt_text, fuzz_param):
    print(f'srt_text is {srt_text}')
    last_cursor = 0
    subs = pysubs2.SSAFile.from_string(srt_text, 'srt')                                      
    subs_out = pysubs2.SSAFile()
    # read short_text by line
    for line in short_text.split('\n'):
        matches = re.findall(r'"(.*?)"', line)
        for match in matches:
            split_text = re.split(r'[，,、？ 。！…：；]', match)
            
            for seg in split_text:
                #print(f"seg is {seg}")
                for i in range(last_cursor, last_cursor + len(subs)):
                    current_index = i % len(subs)
                    score = (fuzz.ratio(seg, subs[current_index].text))
                    #print(f"score is {score}")
                    if score > fuzz_param :
                        last_cursor = current_index + 1
                        subs_out.append(subs[current_index])
                        break


    #print(subs_out.to_string('srt'))
    return subs_out.to_string('srt')


def get_file_list(directory):
    """获取指定目录下的所有文件名列表"""
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    #print(f"files is {files}")
    return files
def move_file_to(file_name, file_path="srts" ):
    print(f"move_file_to is {file_name}")
            # Ensure the directory exists
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    if os.path.exists(file_name):
        new_file_name = shutil.move(file_name, file_path)
        print(f"new_file_name is {new_file_name}")
        return new_file_name
def gen_prev_video(srt_file, video_file):
    video_file = video_file
    print("merge clips")
    subs = pysubs2.SSAFile.from_string(srt_file)
#subs = pysubs2.load('cliped_srt/clip1.srt')
    
    # get current timestamp as second
    ts = int(time.time())
    output_file = 'stream' + f'/output_{ts}.m3u8'

    clips = []
    for i in range(len(subs)):
        sub1 = subs[i]
        st = datetime.fromtimestamp(sub1.start/1000, pytz.timezone('utc'))
        ed = datetime.fromtimestamp(sub1.end/1000, pytz.timezone('utc'))
        start_time = st.strftime('%H:%M:%S.%f')[:-3] #'00:00:12.1' # Start time for trimming (HH:MM:SS)
        end_time = ed.strftime('%H:%M:%S.%f')[:-3] # End time for trimming (HH:MM:SS)
        print(start_time, end_time	)
        clips.append(ffmpeg.input(video_file,  ss=start_time, to=end_time)) #hwaccel = 'cpu'

    video_concat = ffmpeg.concat(*[stream['v'] for stream in clips], v=1, a=0).node
    audio_concat = ffmpeg.concat(*[stream['a'] for stream in clips], v=0, a=1).node
    
    output = ffmpeg.output(video_concat['v'].filter('scale', width='640', height='478'), audio_concat['a'], output_file,format='hls', start_number=0, hls_time=10, hls_list_size=0, vcodec='h264_nvenc', init_hw_device="cuda:1") #, vcodec='h264_nvenc', acodec='copy')
    output = ffmpeg.overwrite_output(output) 
    
    ffmpeg.run(output)

    #demo.load(None,None,None,js=scripts)
    #fix for gradio 5.0
    return f"/gradio_api/file="+ output_file
def gen_download_video(srt_file, video_file):
    video_file = video_file
    print("merge clips")
    subs = pysubs2.SSAFile.from_string(srt_file)
#subs = pysubs2.load('cliped_srt/clip1.srt')
    
    # get current timestamp as second
    ts = int(time.time())
    output_file = 'stream' + f'/output_{ts}.mp4'
    movie = VideoFileClip(video_file)
    clips = []
    for i in range(len(subs)):
        sub1 = subs[i]
        st = datetime.fromtimestamp(sub1.start/1000, pytz.timezone('utc'))
        ed = datetime.fromtimestamp(sub1.end/1000, pytz.timezone('utc'))
        start_time = st.strftime('%H:%M:%S.%f')[:-3] #'00:00:12.1' # Start time for trimming (HH:MM:SS)
        end_time = ed.strftime('%H:%M:%S.%f')[:-3] # End time for trimming (HH:MM:SS)
        print(start_time, end_time	)
        clips.append(movie.subclip(start_time, end_time)) #hwaccel = 'cpu'

    out_clips = concatenate_videoclips(clips)
    
    out_clips.write_videofile(output_file, fps=24)

    #demo.load(None,None,None,js=scripts)

    return output_file




def translate_filename_to_pinyin(chinese_filename):
    parts = chinese_filename.split('.')
    name_part = parts[0]
    extension = parts[1] if len(parts) > 1 else ''
    
    pinyin_parts = lazy_pinyin(name_part)
    pinyin_name = '_'.join(pinyin_parts)
    
    if extension:
        return f"{pinyin_name}.{extension}"
    else:
        return pinyin_name