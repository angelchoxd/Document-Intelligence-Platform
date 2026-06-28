import subprocess
from pathlib import Path


def run_ollama_ocr(image_path, model_name):
    image_path = Path(image_path)

    prompt = (
        "Extract all readable text from this image. "
        "Return only the extracted text. Do not explain anything. "
        f"Image path: {image_path}"
    )

    result = subprocess.run(
        ["ollama", "run", model_name, prompt],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
    )

    if result.returncode != 0:
        return f"OCR error: {result.stderr}"

    return result.stdout.strip()


def glm_ocr(image_path):
    return run_ollama_ocr(image_path, "glm-ocr:latest")


def deepseek_ocr(image_path):
    return run_ollama_ocr(image_path, "deepseek-ocr:latest")


def extract_text_from_image(image_path, engine="GLM-OCR"):
    if engine == "GLM-OCR":
        return glm_ocr(image_path)

    if engine == "DeepSeek-OCR":
        return deepseek_ocr(image_path)

    if engine == "Auto":
        return glm_ocr(image_path)

    return glm_ocr(image_path)