# from PIL import Image
# import numpy as np
# import cv2

# # Function to convert the image to grayscale
# def preprocess_image_grayscale(image_path: str) -> Image:
#     """
#     Convert the image at the specified path to grayscale using OpenCV.
    
#     Args:
#     - image_path (str): Path to the image file.
    
#     Returns:
#     - Image: PIL Image object after converting to grayscale.
#     """
#     try:
#         # Open the image using PIL
#         image = Image.open(image_path)

#         # Convert PIL Image to OpenCV format (numpy array)
#         image_cv = np.array(image)

#         # Convert the image to grayscale using OpenCV
#         gray_image_cv = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)

#         # Convert the numpy array back to a PIL Image
#         gray_image = Image.fromarray(gray_image_cv)

#         return gray_image
#     except Exception as e:
#         raise Exception(f"❌ Error during image preprocessing (grayscale): {e}")
