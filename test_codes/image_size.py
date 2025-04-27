from PIL import Image, ExifTags

image_path = 'image_test/sam_combined (92).jpg'
image = Image.open(image_path)

# Handle EXIF orientation
try:
    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation] == 'Orientation':
            break
    exif = image._getexif()
    if exif is not None:
        orientation_value = exif.get(orientation)
        if orientation_value == 3:
            image = image.rotate(180, expand=True)
        elif orientation_value == 6:
            image = image.rotate(270, expand=True)
        elif orientation_value == 8:
            image = image.rotate(90, expand=True)
except (AttributeError, KeyError, IndexError):
    # Cases where there's no EXIF data
    pass

# Now get corrected size
width, height = image.size
print(f"Corrected image size: {width}x{height} (width x height)")
