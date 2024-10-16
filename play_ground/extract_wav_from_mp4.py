import ffmpeg 
import gradio as gr
# extract audio from mp4 file
def extract_audio(input_file):
    output_file = "output_file.wav"
    try:
        (
            ffmpeg
            .input(input_file)
            .output(output_file, format='wav')
            .run(capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        print('stdout:', e.stdout.decode('utf8'))
        print('stderr:', e.stderr.decode('utf8'))

    return output_file

demo = gr.Interface(fn=extract_audio, inputs="video", outputs="file")
demo.launch()