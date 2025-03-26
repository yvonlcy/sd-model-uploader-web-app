# SD Model Uploader Web App

A simple Gradio-based web interface for uploading Stable Diffusion models to a Fooocus container. This application makes it easy to manage and organize model files without needing direct file system access.

## ✨ Features

- 🔄 Easy upload of model files (`.safetensors`, `.ckpt`) to your Fooocus container
- 🗂️ Support for multiple model types:
  - **Lora Models** - LoRA fine-tuned models
  - **Checkpoint Models** - Full model checkpoints
- 💻 Clean and intuitive Gradio user interface
- 🐳 Designed for Docker integration with Fooocus container

## 🔧 Prerequisites

- Python 3.8+
- Docker & Docker Compose (for containerized deployment)
- Running Fooocus container with shared volumes

## 🚀 Installation

### Local Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yvonlcy/sd-model-uploader-web-app.git
   cd sd-model-uploader-web-app
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

### Docker Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yvonlcy/sd-model-uploader-web-app.git
   cd sd-model-uploader-web-app
   ```

2. Create a `docker-compose.yml` file based on the template:
   ```bash
   cp docker-compose.template.yml docker-compose.yml
   ```

3. Edit the `docker-compose.yml` file to configure your paths:
   ```yaml
   services:
     uploader:
       # Configure image name, volumes, etc.
       volumes:
         - ~/fooocus/data/models/loras:/shared_models/loras  # Path to your lora models
         - ~/fooocus/data/models/checkpoints:/shared_models/checkpoints  # Path to checkpoints
   ```

4. Build and run the container:
   ```bash
   docker-compose up -d
   ```

## 🎮 Usage

1. Access the UI at `http://localhost:7860` (or your configured URL for Docker deployment)

2. Select the model type you wish to upload (Lora or Checkpoint)

3. Drag and drop or click to select your model file (`.safetensors` or `.ckpt`)

4. The upload will begin automatically and show progress

5. Once complete, the model will be available in your Fooocus instance

## ⚙️ Configuration
      resources:
        limits:
          memory: 8g
    ulimits:
      nofile:
        soft: 65536
        hard: 65536
```

