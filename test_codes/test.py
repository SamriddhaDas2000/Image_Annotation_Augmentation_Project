from PIL import Image

im = Image.open('images/20250110_151058.jpg')

print(im.size)
print(type(im.size))
# (400, 225)
# <class 'tuple'>

w, h = im.size
print('width: ', w)
print('height:', h)