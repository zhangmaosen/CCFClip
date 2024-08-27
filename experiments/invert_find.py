from rapidfuzz import fuzz
import pysubs2
import pytz

import re
from datetime import datetime
sub_name = "srts/jinrongzichan.srt"
clip_name = "outputs/out_puts_3.txt"
subs = pysubs2.load(sub_name)
# 一行一行的读取，直到读取完毕
with open(clip_name, "r", encoding="utf-8") as f:
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
                    if score > 50:
                        o = pysubs2.SSAFile()
                        out_sub = subs[i]
                        #print(out_sub.type)
                        #o.append(out_sub)
                        o.insert(i, out_sub)
                        tt = (o.to_string('srt'))
                        # remove first line of tt
                        tt = tt[tt.find('\n')+1:]
                        # add i in first line of tt
                        tt = str(i) +"\n"  + tt
                        print(tt)

                        # start = datetime.fromtimestamp(subs[i].start/1000.0, pytz.utc).strftime('%H:%M:%S,%f')[:-3]
                        # end = datetime.fromtimestamp(subs[i].end/1000.0, pytz.utc).strftime('%H:%M:%S,%f')[:-3]
                        # print(str(i+1) + ". [" + start + " - " + end + "] " + seg)
