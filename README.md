# SD Model Uploader Web App

This application provides a simple Gradio-based interface to upload models (`.safetensors`, `.ckpt`) to Fooocus container (`fooocus-mashb1t:latest`). It manages uploads for two model types:

- **Lora Models**
- **Checkpoint Models**

## 📦 Setup

### Docker Compose Setup:

```yaml
services:
  uploader:
    build: .
    image: ${CI_REGISTRY_IMAGE:-sd-model-uploader}:${IMAGE_VERSION:-latest}
    ports:
      - "7860:7860"
    volumes:
      - ~/fooocus/data/models/loras:/shared_models/loras
      - ~/fooocus/data/models/checkpoints:/shared_models/checkpoints
    environment:
      BASE_DIR: /shared_models
    deploy:
      resources:
        limits:
          memory: 8g
    ulimits:
      nofile:
        soft: 65536
        hard: 65536
```

