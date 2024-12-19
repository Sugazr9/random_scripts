from PIL import Image

# Load the original image
image = Image.open("C:/Users/go_ar/Downloads/your_transparent_image2.png")

# Resize the image to make the dots smaller
new_width, new_height = image.size[0] // 2, image.size[1] // 2  # Reduce size by 50%
resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

# Save the resized image
resized_image.save("C:/Users/go_ar/Downloads/your_transparent_image2_resize.png")
