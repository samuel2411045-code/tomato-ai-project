import numpy as np
from PIL import Image
from weather import get_location_from_ip
from ocr_utils import extract_soil_values
from disease_model import predict_leaf_disease

def test_location():
    print("Testing Location Detection...")
    loc = get_location_from_ip()
    if loc:
        print(f"✅ Location detected: {loc}")
    else:
        print("ℹ️ Location detection failed (expected if IP detection is blocked or no net)")

def test_ocr_fallback():
    print("\nTesting OCR Fallback...")
    mock_img = Image.new('RGB', (100, 100), color='white')
    card = extract_soil_values(mock_img)
    if card.n == 200.0:
        print("✅ OCR Fallback successful (default values returned)")
    else:
        print("❌ OCR Fallback failed")

def test_disease_model_placeholders():
    print("\nTesting Disease Model Placeholders...")
    mock_array = np.zeros((224, 224, 3), dtype=np.uint8)
    
    res_cnn = predict_leaf_disease(image_rgb=mock_array, model_type="CNN")
    print(f"CNN Placeholder: {res_cnn.label} (Model Path: {res_cnn.remedy[:30]}...)")
    
    res_vit = predict_leaf_disease(image_rgb=mock_array, model_type="ViT")
    print(f"ViT Placeholder: {res_vit.label} (Model Path: {res_vit.remedy[:30]}...)")
    
    if res_cnn.model_type == "CNN" and res_vit.model_type == "ViT":
        print("✅ Model type correctly identifies in predictions")

if __name__ == "__main__":
    test_location()
    test_ocr_fallback()
    test_disease_model_placeholders()
