from funasr import AutoModel

model = AutoModel(model="iic/emotion2vec_plus_large")
wav_file = f"wav/9.27刘湘雯_ok.wav"
res = model.generate(wav_file, output_dir="./outputs", granularity="frame", extract_embedding=True)
print(res)