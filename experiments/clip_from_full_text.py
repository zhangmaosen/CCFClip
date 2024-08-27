import ollama
import pysubs2
from pysubs2 import Alignment, Color, SSAFile, SSAStyle


all_text = ""
num_ctx = 28192
temperature = 0.1
model_name = 'qwen2:72b-instruct' #'deepseek-v2:16b'#'gemma2:27b-instruct-q4_0' #'llama3.1:70b-instruct-q2_K'
srt_file_name = 'srts/jinrongzichan.txt'
sys_prompt_file_name = 'sys_prompts/best_prompt.txt'
# read all text from file into all_text
with open(srt_file_name, 'r') as f:
    all_text = f.read()


all_lines = all_text.split('\n')
max_line_length = 100
ajust_line_length = 8
i = 0
chunks = []

#print(all_lines)


while i < len(all_lines):

    if i > ajust_line_length:
        start = i - ajust_line_length
    else:
        start = 0
    
    end = i + max_line_length

    # print("i:", i)
    # print("start: ", start) 
    # print("end: ", end)

    # merge all_lines[start:end] to str
    subs = " ".join(all_lines[start:end]) 
    chunks.append(subs)
    i = i + max_line_length
    #print("\n")
    #print(chunks)


# open srt file read content to variable system_prompt
with open(sys_prompt_file_name, 'r') as f:
    system_prompt = f.read()

out_puts = ""
for prompt in chunks:
    print("prompt: ", prompt)
    prompt = '这是视频的速记稿内容：\n'  + prompt + "。\n请按照工作要求，开始摘录的工作："

    #continue
    response = ollama.chat(model=model_name, messages=[

        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': prompt}
    ],options= {
        "num_ctx": num_ctx ,
        "temperature" : temperature
    }, keep_alive=-1)

# gemma2:27b-instruct-q4_0
# response = ollama.generate(model='qwen2:72b-instruct', prompt=user_prompt, system=system_prompt,options= {
#     "num_ctx": 34096
#   })
#print(response)
    print("\n精彩摘录：")
    print(response['message']['content'])
    print("\n")
    out_puts = out_puts + response['message']['content'] + "\n"


# write out_puts to file
with open('outputs/out_puts_3.txt', 'w') as f:
    f.write(out_puts)