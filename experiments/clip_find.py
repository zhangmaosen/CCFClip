from rapidfuzz import fuzz
import pysubs2
import pytz

import re
from datetime import datetime

subs = pysubs2.load("srts/jushenzhineng.srt")
# 一行一行的读取，直到读取完毕
with open("outputs/out_puts_3.txt", "r", encoding="utf-8") as f:
    while True:
        line = f.readline()
        if not line:
            break
        # 使用正则表达式匹配双引号中的内容
        matches = re.findall(r'"(.*?)"', line)

        # 输出匹配到的内容
        for match in matches:
            #print(match)
            split_text = re.split(r'[，、？。！…]', match)

            for seg in split_text:
                #print(seg)

                for i in range(len(subs)):
                    #print(subs[i].text)
                    score = (fuzz.ratio(seg, subs[i].text))
                    if score > 70:
                        #按照下列格式：1. [开始时间-结束时间] 文本，注意其中的连接符是“-”，将subs的内容输出
                        #把milliseconds 转换为 timestamp格式输出
                        #print(subs[i].start)
                        start = datetime.fromtimestamp(subs[i].start/1000.0, pytz.utc).strftime('%H:%M:%S,%f')[:-3]
                        end = datetime.fromtimestamp(subs[i].end/1000.0, pytz.utc).strftime('%H:%M:%S,%f')[:-3]
                        print(str(i+1) + ". [" + start + " - " + end + "] " + seg)
                        #print(subs[i])
# score = fuzz.ratio("AI如何改变艺术创作？", "那么呃 AI 对于艺术的全面介入啊")
# print(score)