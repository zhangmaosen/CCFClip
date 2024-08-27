import ollama
import pysubs2
from pysubs2 import Alignment, Color, SSAFile, SSAStyle

model_name = 'deepseek-v2:16b'#'gemma2:27b-instruct-q4_0' #'llama3.1:70b-instruct-q2_K'
srt_file_name = 'srts/full_txt.txt'
sys_prompt_file_name = 'sys_prompts/system_prompt_9.txt'
all_text = ""
subs = pysubs2.load(srt_file_name)


max_line_length = 200
ajust_line_length = 8
i = 0
chunks = []
while i < len(subs):
    chunk_subs = SSAFile()
    if i > ajust_line_length:
        start = i - ajust_line_length
    else:
        start = 0
    
    end = i + max_line_length

    # print("i:", i)
    # print("start: ", start) 
    # print("end: ", end)

    for j in range(start, end):
        if j >= len(subs):
            break
        subs[j].text = subs[j].text.replace('\n', ' ')
        chunk_subs.append(subs[j])
        #print(subs[j].text)
    chunks.append(chunk_subs.to_string('srt'))
    i = i + max_line_length
    #print("\n")

print('chunk len: ', len(chunks))
# open srt file read content to variable system_prompt
with open(sys_prompt_file_name, 'r') as f:
    system_prompt = f.read()

for idx in range(0,1):
    out_puts = ""
    for prompt in chunks:

        prompt = '这是待裁剪的视频srt字幕：\n' + prompt #+ '\n. 请一步一步裁剪字幕，逐步完成字幕编辑的工作：'

        response = ollama.chat(model=model_name, messages=[

            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': prompt}
        ],options= {
            "num_ctx": 38096 ,
            "temperature" : 0.01
        }, keep_alive=-1)

    # gemma2:27b-instruct-q4_0
    # response = ollama.generate(model='qwen2:72b-instruct', prompt=user_prompt, system=system_prompt,options= {
    #     "num_ctx": 34096
    #   })
    #print(response)
        print("\n精彩字幕：")
        print(response['message']['content'])
        out_puts = out_puts + response['message']['content'] + "\n"


# write out_puts to file
with open('outputs/out_puts_3.txt', 'w') as f:
    f.write(out_puts)