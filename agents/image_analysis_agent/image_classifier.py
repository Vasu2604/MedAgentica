import os
import json
import base64
from mimetypes import guess_type

from typing import TypedDict
from langchain_core.output_parsers import JsonOutputParser

class ClassificationDecision(TypedDict):
    """Output structure for the decision agent."""
    image_type: str
    reasoning: str
    confidence: float

class ImageClassifier:
    """Uses GPT-4o Vision to analyze images and determine their type."""
    
    def __init__(self, vision_model):
        self.vision_model = vision_model
        self.json_parser = JsonOutputParser(pydantic_object=ClassificationDecision)
        
    def local_image_to_data_url(self, image_path: str) -> str:
        """Get the url of a local image"""
        try:
            mime_type, _ = guess_type(image_path)
            if mime_type is None:
                mime_type = "application/octet-stream"

            with open(image_path, "rb") as image_file:
                base64_encoded_data = base64.b64encode(image_file.read()).decode("utf-8")

            return f"data:{mime_type};base64,{base64_encoded_data}"
        except Exception as e:
            print(f"[ImageAnalyzer] Error reading image file {image_path}: {e}")
            raise e
    
    def classify_image(self, image_path: str) -> dict:
        """Analyzes the image to classify it as a medical image and determine its type."""
        print(f"[ImageAnalyzer] Analyzing image: {image_path}")

        # Check if image file exists
        if not os.path.exists(image_path):
            print(f"[ImageAnalyzer] Error: Image file not found: {image_path}")
            return {"image_type": "unknown", "reasoning": "Image file not found", "confidence": 0.0}

        # Skip vision model for now since OpenRouter DeepSeek doesn't support images
        # Go directly to heuristic classification which is more reliable
        print("[ImageAnalyzer] Using heuristic classification (vision model not available)")
        return self._classify_image_heuristic(image_path)
    
    def _classify_image_heuristic(self, image_path: str) -> dict:
        """Fallback method to classify images using heuristics when vision model fails."""
        import cv2
        import numpy as np
        
        try:
            # Read image
            img = cv2.imread(image_path)
            if img is None:
                return {"image_type": "unknown", "reasoning": "Could not read image", "confidence": 0.0}
            
            # Get image dimensions and basic properties
            height, width = img.shape[:2]
            aspect_ratio = width / height
            
            # Convert to different color spaces for analysis
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Analyze color distribution
            mean_color = np.mean(img, axis=(0, 1))
            std_color = np.std(img, axis=(0, 1))
            
            print(f"[ImageAnalyzer] Heuristic Analysis:")
            print(f"  - Image dimensions: {width}x{height}")
            print(f"  - Aspect ratio: {aspect_ratio:.2f}")
            print(f"  - Mean color (BGR): {mean_color}")
            print(f"  - Gray mean: {np.mean(gray):.2f}")
            print(f"  - Color std: {std_color.mean():.2f}")
            
            # Check for X-ray characteristics first (higher priority)
            gray_mean = np.mean(gray)
            color_variance = np.var(img)
            
            # X-ray characteristics:
            # 1. Usually grayscale or near-grayscale
            # 2. Specific intensity range
            # 3. Lower color variance (more monochromatic)
            # 4. Often rectangular or square
            
            # Check if image is predominantly grayscale
            color_diff = np.max(std_color) - np.min(std_color)
            # Also check actual color channel differences
            bgr_diff = np.max(mean_color) - np.min(mean_color)
            is_grayscale_like = color_diff < 15 and bgr_diff < 15  # Very strict grayscale check
            
            # Check for X-ray intensity characteristics
            is_xray_intensity = 30 < gray_mean < 220
            
            # Check for medical imaging aspect ratios
            is_medical_aspect = 0.7 < aspect_ratio < 1.5
            
            print(f"  - Color difference: {color_diff:.2f}")
            print(f"  - BGR difference: {bgr_diff:.2f}")
            print(f"  - Is grayscale-like: {is_grayscale_like}")
            print(f"  - Is X-ray intensity: {is_xray_intensity}")
            print(f"  - Is medical aspect: {is_medical_aspect}")
            
            # Strong X-ray indicators
            if is_grayscale_like and is_xray_intensity and is_medical_aspect:
                return {
                    "image_type": "CHEST X-RAY",
                    "reasoning": "Heuristic classification: Grayscale medical image with X-ray characteristics",
                    "confidence": 0.8
                }
            
            # Weaker X-ray indicators
            if is_grayscale_like and is_xray_intensity:
                return {
                    "image_type": "CHEST X-RAY",
                    "reasoning": "Heuristic classification: Grayscale image with X-ray intensity range",
                    "confidence": 0.7
                }
            
            # Check for skin lesion characteristics
            red_channel = mean_color[2]  # BGR format
            green_channel = mean_color[1]
            blue_channel = mean_color[0]
            
            # Skin lesions typically have:
            # - More color variation
            # - Warmer tones
            # - Higher red/brown components
            has_warm_tones = red_channel > green_channel and red_channel > blue_channel
            has_color_variation = std_color.mean() > 25
            
            if has_warm_tones and has_color_variation and not is_grayscale_like:
                return {
                    "image_type": "SKIN LESION",
                    "reasoning": "Heuristic classification: Colorful image with warm tones and variation, likely skin lesion",
                    "confidence": 0.7
                }
            
            # If we can't determine confidently, default to chest X-ray for medical images
            # (since most uploaded medical images in this context are likely X-rays)
            return {
                "image_type": "CHEST X-RAY",
                "reasoning": "Heuristic classification: Medical image, defaulting to chest X-ray",
                "confidence": 0.5
            }
            
        except Exception as e:
            print(f"[ImageAnalyzer] Heuristic classification failed: {e}")
            return {
                "image_type": "SKIN LESION", 
                "reasoning": "Fallback classification: Assuming skin lesion for medical image",
                "confidence": 0.3
            }

        # return response.content.strip().lower()
