import pysubs2
import ollama
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

def gen_full_text(srt_file):
    subs = pysubs2.load(srt_file)
    full_txt = ''
    for line in subs:
        full_txt += line.text + '\n'
    return [ len(full_txt), full_txt, subs.to_string('srt')]

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
def run_model(system_prompt, full_text, model_select, user_prompt,  temperature=0.1, num_ctx=30000,keep_alive=-1, num_predict=150, local_or_online='local', key=None):
    if local_or_online == 'local':
        pre_out = ""
        response = ollama.chat(model=model_select, messages=[

            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt + full_text }
        ],options= {
            "num_ctx": num_ctx ,
            "temperature" : temperature,
            'num_predict' : num_predict
        }, keep_alive=keep_alive, stream=True)
        for chunk in response:
            pre_out = pre_out + chunk['message']['content']
            yield pre_out
    elif local_or_online == 'online':
         
        yield from call_stream_with_messages(full_text, model_select, system_prompt, user_prompt,  temperature, num_predict, key)



def invert_find(short_text,srt_text, fuzz_param):

    last_cursor = 0
    subs = pysubs2.SSAFile.from_string(srt_text)                                      
    subs_out = pysubs2.SSAFile()
    # read short_text by line
    for line in short_text.split('\n'):
        matches = re.findall(r'“(.*?)”', line)
        for match in matches:
            split_text = re.split(r'[，,、？。！…：；]', match)
            
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
    return files
def gen_prev_video(srt_file, video_file):
    video_file = 'video/' + video_file
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

    return "http://127.0.0.1:7860/file="+ output_file
def gen_download_video(srt_file, video_file):
    video_file = 'video/' + video_file
    print("merge clips")
    subs = pysubs2.SSAFile.from_string(srt_file)
#subs = pysubs2.load('cliped_srt/clip1.srt')
    
    # get current timestamp as second
    ts = int(time.time())
    output_file = 'stream' + f'/output_{ts}.mp4'

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
    
    output = ffmpeg.output(video_concat['v'], audio_concat['a'], output_file,format='mp4',  vcodec='h264_nvenc', init_hw_device="cuda:1") #, vcodec='h264_nvenc', acodec='copy')
    output = ffmpeg.overwrite_output(output) 
    
    ffmpeg.run(output)

    #demo.load(None,None,None,js=scripts)

    return output_file