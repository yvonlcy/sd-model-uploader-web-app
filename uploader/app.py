import os
import gradio as gr
import time

# set baser directory for uploaded files, default is '/shared_models'
BASE_DIR = os.environ.get("BASE_DIR", "/shared_models")

# directory for different model types
UPLOAD_DIRS = {
    "loras": os.path.join(BASE_DIR, "loras"),
    "checkpoints": os.path.join(BASE_DIR, "checkpoints")
}

# ensure upload directories exist
for dir_path in UPLOAD_DIRS.values():
    os.makedirs(dir_path, exist_ok=True)

# convert bytes to human-readable file size format
def human_readable_size(num_bytes):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if num_bytes < 1024:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.1f} PB"

# get info table for uploaded models
def get_uploaded_models_info_table(model_type):
    dir_path = UPLOAD_DIRS.get(model_type, UPLOAD_DIRS["loras"])
    rows = []

    # check if directory exists
    if not os.path.exists(dir_path):
        return [["Directory not found", "N/A", "N/A"]]
    
    try:
        for filename in os.listdir(dir_path):
            # filter files by type
            if model_type == "loras" and not filename.endswith(".safetensors"):
                continue
            if model_type == "checkpoints" and not filename.endswith((".ckpt", ".safetensors")):
                continue

            path = os.path.join(dir_path, filename)
            try:
                size = os.path.getsize(path)
                mtime = os.path.getmtime(path)
                size_str = human_readable_size(size)
                date_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
                rows.append([filename, size_str, date_str])
            except OSError as e:
                rows.append([filename, f"Error: {e}", "N/A"])
    except OSError as e:
        rows.append(["Error", f"Cannot list directory: {e}", "N/A"])

    return rows if rows else [["No models", "N/A", "N/A"]]

# copy large files in chunks to avoid memory overload
def copy_file_in_chunks(src, dst, chunk_size=10*1024*1024):
    with open(src, 'rb') as fsrc, open(dst, 'wb') as fdst:
        while True:
            chunk = fsrc.read(chunk_size)
            if not chunk:
                break
            fdst.write(chunk)

# upload models to the appropriate directory
def upload_models(file_paths, model_type):
    if not file_paths:
        return "No files uploaded."
    target_dir = UPLOAD_DIRS.get(model_type, UPLOAD_DIRS["loras"])
    saved_files = []

    valid_types = {"loras": ".safetensors", "checkpoints": (".ckpt", ".safetensors")}
    
    for file_path in file_paths:
        filename = os.path.basename(file_path)
        if not any(filename.endswith(ext) for ext in ([valid_types[model_type]] if isinstance(valid_types[model_type], str) else valid_types[model_type])):
            continue

        try:
            dest_path = os.path.join(target_dir, filename)
            copy_file_in_chunks(file_path, dest_path)
            saved_files.append(filename)
        except OSError as e:
            return f"Error uploading {filename}: {e}"
    
    return f"Uploaded: {', '.join(saved_files)}" if saved_files else "No valid files uploaded."

# Gradio UI definition
with gr.Blocks() as demo:
    gr.Markdown("## Models Uploader")
    gr.Markdown("Upload model files (LoRAs or Checkpoints) to ~/fooocus/data/models/")
    
    # dropdown to select model type
    model_type = gr.Dropdown(
        choices=["loras", "checkpoints"],
        label="Model Type",
        value="loras"
    )

    # file uploader allowing multiple file selections
    upload_input = gr.File(
        label="Upload Model(s)",
        file_count="multiple",
        file_types=[".safetensors", ".ckpt"],
        type="filepath"
    )

    # status textbox after upload
    upload_out = gr.Textbox(label="Upload Status")
    upload_button = gr.Button("Upload")

    # dataframe showing uploaded files info
    file_info_table = gr.Dataframe(
        headers=["Filename", "Size", "Uploaded Date"],
        datatype=["str", "str", "str"],
        value=get_uploaded_models_info_table("loras"),
        label="Uploaded Models Info (from ~/fooocus/data/models/)",
        wrap=True
    )

    # button to refresh file info table
    refresh_table_button = gr.Button("Refresh File Info")

    # update table when model type changes
    model_type.change(
        fn=get_uploaded_models_info_table,
        inputs=model_type,
        outputs=file_info_table
    )

    # upload button action
    upload_button.click(
        upload_models,
        inputs=[upload_input, model_type],
        outputs=upload_out
    ).then(
        fn=get_uploaded_models_info_table,
        inputs=model_type,
        outputs=file_info_table
    )

    # manually refresh file info table
    refresh_table_button.click(
        fn=get_uploaded_models_info_table,
        inputs=model_type,
        outputs=file_info_table
    )

# start the Gradio app
demo.launch(
    server_name="0.0.0.0",
    server_port=7860
)
