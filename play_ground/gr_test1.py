import gradio as gr

# Paths can be a list of strings or pathlib.Path objects
# corresponding to filenames or directories.
gr.set_static_paths(paths=["images", "stream"])

# The example files and the default value of the input
# will not be copied to the gradio cache and will be served directly.
demo = gr.Interface(
    lambda s: s.rotate(45),
    gr.Image(value="images/1.jpeg", type="pil"),
    gr.Image(),
    examples=["images/1.jpeg"],
)

demo.launch()