import pysubs2
sub_file = 'srts/jinrongzichan.srt'
out_file = 'srts/jinrongzichan.txt'
#use pysubs2 to read the subtitle file and output pure text 
def gen_full_txt(sub_file):
    subs = pysubs2.load(sub_file)
    full_txt = ''
    for line in subs:
        full_txt += line.text + '\n'
    return full_txt

# main func 
if __name__ == '__main__':
    sub_file = sub_file
    full_txt = gen_full_txt(sub_file)
    #write full_txt to a file
    with open(out_file, 'w') as f:
        f.write(full_txt)
    print(full_txt)
    # count the  tokens in full_txt
    #print(len(full_txt))
    #print(len(full_txt.split()))