from PIL import Image, ImageEnhance

# Open the original image
image = Image.open("C:/Users/go_ar/Downloads/final_targeted_color_adjusted_logo.png")

# Convert the image to grayscale (black and white)
grayscale_image = image.convert("L")

# Increase contrast to make it more monochrome
enhancer = ImageEnhance.Contrast(grayscale_image)
monochrome_image = enhancer.enhance(10.0)  # Adjust contrast level (2.0 = double contrast)

# Save the result
monochrome_image.save("C:/Users/go_ar/Downloads/black_and_white_logo3.png")
