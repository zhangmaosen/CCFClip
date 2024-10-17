import gradio as gr

# Paths can be a list of strings or pathlib.Path objects
# corresponding to filenames or directories.
gr.set_static_paths(paths=["test/test_files/"])

# The example files and the default value of the input
# will not be copied to the gradio cache and will be served directly.
demo = gr.Interface(
    lambda s: s.rotate(45),
    gr.Image(value="test/test_files/1.jpeg", type="pil"),
    gr.Image(),
    examples=["test/test_files/bus.png"],
)

demo.launch()