import ffmpeg
input = ffmpeg.input("video/jinrongzichan.mp4", hwaccel = 'cuda')
(
    ffmpeg
    .concat(
        input.trim(start_frame=10, end_frame=20),
        input.trim(start_frame=300, end_frame=400),
        v=1,
        a=1
    )
    .output('out.mp4')
    .run()
)