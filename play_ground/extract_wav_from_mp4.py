import ffmpeg 
import gradio as gr
from funasr import AutoModel

funasr_model = AutoModel(model="iic/speech_seaco_paraformer_large_asr_nat-zh-cn-16k-common-vocab8404-pytorch",
                                vad_model="damo/speech_fsmn_vad_zh-cn-16k-common-pytorch",
                                punc_model="damo/punc_ct-transformer_zh-cn-common-vocab272727-pytorch",
                                spk_model="damo/speech_campplus_sv_zh-cn_16k-common",
                                )

# extract audio from mp4 file
def extract_audio(input_file):
    output_file = "output_file.wav"
    # try:
    #     (
    #         ffmpeg
    #         .input(input_file)
    #         .output(output_file, format='wav')
    #         .run(capture_stdout=True, capture_stderr=True)
    #     )
    # except ffmpeg.Error as e:
    #     print('stdout:', e.stdout.decode('utf8'))
    #     print('stderr:', e.stderr.decode('utf8'))
    result = funasr_model.generate(input=output_file)
    return result

demo = gr.Interface(fn=extract_audio, inputs="video", outputs="text")
demo.launch()