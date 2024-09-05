import ffmpeg
ffmpeg.input('video/jinrongzichan.mp4').filter('scale', width='640', height='478').output('stream/output.m3u8',format='hls', start_number=0, hls_time=10, hls_list_size=0).run()