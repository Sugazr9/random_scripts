from PIL import Image

# Load the image
image = Image.open("C:/Users/go_ar/Downloads/benday_dot_pattern.png").convert("RGBA")

# Prepare a new data array for the modified pixels
data = image.getdata()
new_data = []

# Define a threshold for white (to handle slight variations in white pixels)
black_threshold = 80
for item in data:
    # Check if the pixel is approximately white
    if item[0] > black_threshold and item[1] > black_threshold and item[2] > black_threshold:
        # Replace with transparent pixel
        new_data.append((255, 255, 255, 0))  # RGBA: (R, G, B, Alpha)
    else:
        # Keep the original pixel
        new_data.append(item)

# Update the image with the new data
image.putdata(new_data)

# Save the modified image with transparency
image.save("C:/Users/go_ar/Downloads/your_transparent_imageb2.png", "PNG")
