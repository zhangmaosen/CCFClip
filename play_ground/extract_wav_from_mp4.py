import ffmpeg 
import gradio as gr
from funasr import AutoModel
from utils.subtitle_utils import *
import os

funasr_model = AutoModel(model="iic/speech_seaco_paraformer_large_asr_nat-zh-cn-16k-common-vocab8404-pytorch",
                                vad_model="damo/speech_fsmn_vad_zh-cn-16k-common-pytorch",
                                punc_model="damo/punc_ct-transformer_zh-cn-common-vocab272727-pytorch",
                                spk_model="damo/speech_campplus_sv_zh-cn_16k-common",
                                disable_update=True
                                )

# extract audio from mp4 file
def extract_audio(input_file):
    input_file_name = os.path.basename(input_file)
    input_file_name_without_ext = os.path.splitext(input_file_name)[0]
    output_file = f"./wav/{input_file_name_without_ext}.wav"
    try:
        (
            ffmpeg
            .input(input_file)
            .output(output_file, format='wav')
            .run(overwrite_output=True)
        )
    except ffmpeg.Error as e:
        print('stdout:', e.stdout.decode('utf8'))
        print('stderr:', e.stderr.decode('utf8'))
    rec_result = funasr_model.generate(input=output_file)
    srt = generate_srt(rec_result[0]['sentence_info'])
    
    with open(f"./srts/{input_file_name_without_ext}.srt", "w", encoding='utf-8') as file:
        file.write(srt)
    return f"./srts/{input_file_name_without_ext}.srt"
with gr.Blocks() as demo:
    video_file = gr.FileExplorer(root_dir="video", file_count="single")
    srt_file = gr.FileExplorer(root_dir="srts", file_count="single")
    gr.Interface(fn=extract_audio, inputs=video_file, outputs=srt_file)
    
demo.launch()