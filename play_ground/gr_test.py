import gradio as gr

html = """
<html>
  <body>

    <video id="videoPlayer" controls></video>
    <button type="testButton" onclick="testFn()"> Start </button>
  </body>
</html>
"""

scripts = """
async () => {

    const script = document.createElement("script");
    script.onload = () =>  console.log("d3 loaded") ;
    script.src = "https://cdn.jsdelivr.net/npm/hls.js@latest";
    document.head.appendChild(script)

    globalThis.testFn = () => {
      document.getElementById('demo').innerHTML = "Hello"
    }

    script.addEventListener('load', () => {
        var video = document.getElementById('videoPlayer');

        if (Hls.isSupported()) {
            var hls = new Hls();

            // HLS.js 事件监听
            hls.on(Hls.Events.MEDIA_ATTACHED, function () {
                console.log('Video and HLS.js are attached');
            });

            hls.on(Hls.Events.MANIFEST_PARSED, function () {
                console.log('Manifest has been successfully parsed');
            });

            hls.on(Hls.Events.ERROR, function (event, data) {
                var errorType = data.type;
                var errorDetails = data.details;
                console.error('HLS.js error occurred:', errorType, errorDetails);
            });

            // Video 元素事件监听
            video.addEventListener('play', function () {
                console.log('Video started playing');
            });

            video.addEventListener('pause', function () {
                console.log('Video paused');
            });

            video.addEventListener('ended', function () {
                console.log('Video ended');
            });

            video.addEventListener('error', function () {
                console.error('Video playback error occurred');
            });

            // 加载 HLS 视频源
            hls.loadSource('http://127.0.0.1:9999/stream/output.m3u8');
            hls.attachMedia(video);
        } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
            video.src = 'http://127.0.0.1:9999/stream/output.m3u8';
            video.addEventListener('canplay', function () {
                console.log('Video can start playing');
                video.play();
            });
            video.addEventListener('error', function () {
                console.error('Video playback error occurred');
            });
        }
})
}
"""



with gr.Blocks() as demo:   
    input_mic = gr.HTML(html)
    out_text  = gr.Textbox()
    # run script function on load,
    demo.load(None,None,None,js=scripts)
    #demo.load(None,None,None,js=scripts2)


demo.launch()