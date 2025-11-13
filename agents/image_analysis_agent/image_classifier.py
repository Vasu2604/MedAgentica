import os
import json
import base64
from mimetypes import guess_type

from typing import TypedDict
from langchain_core.output_parsers import JsonOutputParser
from .chest_xray_agent.covid_chest_xray_inference import ChestXRayClassification
import logging

class ClassificationDecision(TypedDict):
    """Output structure for the decision agent."""
    image_type: str
    reasoning: str
    confidence: float

class ImageClassifier:
    """Uses GPT-4o Vision to analyze images and determine their type."""

    def __init__(self, vision_model, chest_xray_model_path=None, skin_lesion_model_path=None, brain_tumor_model_path=None):
        self.vision_model = vision_model
        self.json_parser = JsonOutputParser(pydantic_object=ClassificationDecision)

        # Initialize trained models
        self.chest_xray_classifier = None
        self.skin_lesion_classifier = None
        self.brain_tumor_classifier = None

        if chest_xray_model_path and os.path.exists(chest_xray_model_path):
            try:
                self.chest_xray_classifier = ChestXRayClassification(chest_xray_model_path)
                print(f"[ImageAnalyzer] Chest X-ray model loaded from {chest_xray_model_path}")
            except Exception as e:
                print(f"[ImageAnalyzer] Failed to load chest X-ray model: {e}")

        if skin_lesion_model_path and os.path.exists(skin_lesion_model_path):
            try:
                # Initialize skin lesion model (would need similar class)
                print(f"[ImageAnalyzer] Skin lesion model path provided: {skin_lesion_model_path}")
            except Exception as e:
                print(f"[ImageAnalyzer] Failed to load skin lesion model: {e}")

        if brain_tumor_model_path and os.path.exists(brain_tumor_model_path):
            try:
                # Initialize brain tumor model (would need similar class)
                print(f"[ImageAnalyzer] Brain tumor model path provided: {brain_tumor_model_path}")
            except Exception as e:
                print(f"[ImageAnalyzer] Failed to load brain tumor model: {e}")
        
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
            
            # Calculate key metrics
            gray_mean = np.mean(gray)
            color_variance = np.var(img)
            
            # Check if image is predominantly grayscale
            color_diff = np.max(std_color) - np.min(std_color)
            bgr_diff = np.max(mean_color) - np.min(mean_color)
            is_grayscale_like = color_diff < 20 and bgr_diff < 20  # Slightly relaxed for better detection
            
            # Get color channel values (BGR format)
            red_channel = mean_color[2]
            green_channel = mean_color[1]
            blue_channel = mean_color[0]
            
            # Calculate color saturation and hue characteristics
            saturation = np.mean(hsv[:, :, 1])  # Saturation channel
            hue_mean = np.mean(hsv[:, :, 0])  # Hue channel
            
            # Skin lesion characteristics (STRONG INDICATORS):
            # 1. Significant color variation (not grayscale)
            # 2. Warm tones (red/brown/pink dominant)
            # 3. Higher saturation (colorful, not monochrome)
            # 4. Texture and detail visible
            # 5. Often has organic shapes, not geometric X-ray patterns
            
            has_warm_tones = red_channel > green_channel and red_channel > blue_channel
            has_high_saturation = saturation > 40  # Skin images have more color saturation
            has_color_variation = std_color.mean() > 20  # More variation in skin images
            is_not_grayscale = not is_grayscale_like
            
            # Calculate skin lesion score
            skin_lesion_score = 0
            if has_warm_tones:
                skin_lesion_score += 2
            if has_high_saturation:
                skin_lesion_score += 2
            if has_color_variation:
                skin_lesion_score += 1
            if is_not_grayscale:
                skin_lesion_score += 2
            if red_channel > 100:  # Skin typically has higher red values
                skin_lesion_score += 1
            
            # Brain MRI characteristics (STRONG INDICATORS):
            # 1. Grayscale medical image (like X-ray)
            # 2. BUT: More uniform intensity, less contrast than X-rays
            # 3. Darker overall (brain tissue appears darker than lungs on X-ray)
            # 4. Square or nearly square aspect ratio (MRI scans are typically square)
            # 5. Axial/sagittal/coronal views with distinct brain structures
            # 6. Higher intensity in certain regions (CSF appears bright)
            
            is_square_aspect = 0.9 < aspect_ratio < 1.1  # MRIs are usually square
            is_darker_intensity = gray_mean < 80  # Brain MRIs tend to be darker
            is_moderate_intensity = 40 < gray_mean < 120  # Moderate range
            has_low_contrast = std_color.mean() < 15  # More uniform than X-rays
            is_very_grayscale = bgr_diff < 5  # Very tight color channels (pure grayscale)
            
            # Calculate brain MRI score
            brain_mri_score = 0
            if is_square_aspect:
                brain_mri_score += 3  # Strong indicator
            if is_grayscale_like:
                brain_mri_score += 2
            if is_darker_intensity:
                brain_mri_score += 2  # Brain MRIs are typically darker
            if is_very_grayscale:
                brain_mri_score += 2
            if is_low_saturation:
                brain_mri_score += 1
            if has_low_contrast:
                brain_mri_score += 1
            
            # X-ray characteristics (STRONG INDICATORS):
            # 1. Predominantly grayscale (very low color variation)
            # 2. Specific intensity range (typical of X-ray images)
            # 3. Lower saturation (monochrome)
            # 4. Often rectangular aspect ratio (chest X-rays are taller)
            # 5. Higher contrast (bones vs soft tissue)
            
            is_xray_intensity = 80 < gray_mean < 220  # X-rays are brighter than MRIs
            is_low_saturation = saturation < 30  # X-rays are very desaturated
            is_rectangular_aspect = aspect_ratio < 0.9 or aspect_ratio > 1.1  # Not square
            has_high_contrast = std_color.mean() > 15  # More variation than MRIs
            
            # Calculate X-ray score
            xray_score = 0
            if is_grayscale_like:
                xray_score += 2  # Indicator but not as strong (MRI also grayscale)
            if is_xray_intensity:
                xray_score += 3  # Strong indicator (brighter than MRI)
            if is_low_saturation:
                xray_score += 2
            if is_rectangular_aspect:
                xray_score += 2  # X-rays are typically not square
            if bgr_diff < 10:  # Very low color difference = grayscale
                xray_score += 1
            if has_high_contrast:
                xray_score += 2  # Higher contrast than MRI
            
            print(f"  - Color difference: {color_diff:.2f}")
            print(f"  - BGR difference: {bgr_diff:.2f}")
            print(f"  - Saturation: {saturation:.2f}")
            print(f"  - Aspect ratio: {aspect_ratio:.2f}")
            print(f"  - Gray mean: {gray_mean:.2f}")
            print(f"  - Is grayscale-like: {is_grayscale_like}")
            print(f"  - Is square aspect: {is_square_aspect}")
            print(f"  - Skin lesion score: {skin_lesion_score}")
            print(f"  - Brain MRI score: {brain_mri_score}")
            print(f"  - X-ray score: {xray_score}")
            
            # Decision logic: Compare scores and route accordingly
            # Priority order: Skin Lesion > Brain MRI > Chest X-ray
            # This prevents misrouting of colorful or square grayscale images
            
            # 1. Strong skin lesion indicators (check first - most distinctive)
            if skin_lesion_score >= 4 and skin_lesion_score >= max(brain_mri_score, xray_score):
                return {
                    "image_type": "SKIN LESION",
                    "reasoning": f"Heuristic classification: Colorful image with warm tones (score: {skin_lesion_score}), likely skin lesion",
                    "confidence": min(0.85, 0.5 + (skin_lesion_score * 0.05))
                }
            
            # 2. Moderate skin lesion indicators
            if skin_lesion_score >= 3 and skin_lesion_score > max(brain_mri_score, xray_score):
                return {
                    "image_type": "SKIN LESION",
                    "reasoning": f"Heuristic classification: Image shows color characteristics suggesting skin lesion (score: {skin_lesion_score} vs MRI: {brain_mri_score}, X-ray: {xray_score})",
                    "confidence": 0.7
                }
            
            # 3. Strong brain MRI indicators (check before X-ray)
            if brain_mri_score >= 6 and brain_mri_score > xray_score:
                return {
                    "image_type": "BRAIN MRI",
                    "reasoning": f"Heuristic classification: Square grayscale image with MRI characteristics - darker intensity, uniform appearance (score: {brain_mri_score})",
                    "confidence": min(0.85, 0.55 + (brain_mri_score * 0.05))
                }
            
            # 4. Moderate brain MRI indicators (likely brain MRI)
            if brain_mri_score >= 4 and is_square_aspect and is_grayscale_like:
                return {
                    "image_type": "BRAIN MRI",
                    "reasoning": f"Heuristic classification: Square grayscale medical image, likely brain MRI (score: {brain_mri_score} vs X-ray: {xray_score})",
                    "confidence": 0.7
                }
            
            # 5. Strong X-ray indicators
            if xray_score >= 7 and is_grayscale_like and is_xray_intensity:
                return {
                    "image_type": "CHEST X-RAY",
                    "reasoning": f"Heuristic classification: Bright grayscale medical image with X-ray characteristics - rectangular, higher contrast (score: {xray_score})",
                    "confidence": min(0.9, 0.6 + (xray_score * 0.05))
                }
            
            # 6. Moderate X-ray indicators (but not square/dark like MRI)
            if xray_score >= 5 and is_grayscale_like and not is_square_aspect:
                return {
                    "image_type": "CHEST X-RAY",
                    "reasoning": f"Heuristic classification: Rectangular grayscale image with X-ray intensity (score: {xray_score})",
                    "confidence": min(0.75, 0.5 + (xray_score * 0.05))
                }
            
            # 7. Weak brain MRI indicators (grayscale + square = likely MRI)
            if brain_mri_score >= 3 and is_square_aspect:
                return {
                    "image_type": "BRAIN MRI",
                    "reasoning": f"Heuristic classification: Square medical image suggesting brain MRI (score: {brain_mri_score})",
                    "confidence": 0.6
                }
            
            # 8. If skin lesion has any positive indicators, prefer it over defaulting
            if skin_lesion_score >= 2:
                return {
                    "image_type": "SKIN LESION",
                    "reasoning": f"Heuristic classification: Image shows color characteristics suggesting skin lesion (score: {skin_lesion_score})",
                    "confidence": 0.6
                }
            
            # 9. Check if it's clearly NOT an X-ray (has color)
            if not is_grayscale_like and has_color_variation:
                return {
                    "image_type": "SKIN LESION",
                    "reasoning": "Heuristic classification: Colorful medical image, likely skin lesion rather than X-ray/MRI",
                    "confidence": 0.55
                }
            
            # 10. Ambiguous grayscale - check aspect ratio for final hint
            if is_grayscale_like:
                if is_square_aspect:
                    return {
                        "image_type": "BRAIN MRI",
                        "reasoning": f"Heuristic classification: Square grayscale image (MRI: {brain_mri_score}, X-ray: {xray_score}), defaulting to brain MRI with low confidence",
                        "confidence": 0.45  # Low confidence triggers clarification
                    }
                else:
                    return {
                        "image_type": "CHEST X-RAY",
                        "reasoning": f"Heuristic classification: Rectangular grayscale image (X-ray: {xray_score}, MRI: {brain_mri_score}), defaulting to chest X-ray with low confidence",
                        "confidence": 0.45  # Low confidence triggers clarification
                    }
            
            # 11. Final fallback: Truly ambiguous - return unknown to trigger clarification
            return {
                "image_type": "unknown",
                "reasoning": f"Heuristic classification: Ambiguous medical image (Skin: {skin_lesion_score}, MRI: {brain_mri_score}, X-ray: {xray_score})",
                "confidence": 0.3  # Very low confidence to trigger clarification prompt
            }
            
        except Exception as e:
            print(f"[ImageAnalyzer] Heuristic classification failed: {e}")
            import traceback
            traceback.print_exc()
            # Don't default to X-ray on error - be more conservative
            return {
                "image_type": "unknown", 
                "reasoning": f"Classification error: {str(e)}",
                "confidence": 0.0
            }

        # return response.content.strip().lower()

    def classify_chest_xray(self, image_path: str) -> str:
        """Classify chest X-ray using the trained model."""
        if not self.chest_xray_classifier:
            print("[ImageAnalyzer] Chest X-ray classifier not loaded")
            return "unknown"

        try:
            print(f"[ImageAnalyzer] Classifying chest X-ray: {image_path}")
            prediction = self.chest_xray_classifier.predict(image_path)
            print(f"[ImageAnalyzer] Chest X-ray prediction: {prediction}")
            return prediction
        except Exception as e:
            print(f"[ImageAnalyzer] Error classifying chest X-ray: {e}")
            return "unknown"
