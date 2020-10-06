# coding:utf-8

# 此程序功能：加滤镜
from PIL import Image, ImageFilter

im1 = Image.open("fish.jpg")

im2 = im1.filter(ImageFilter.BLUR)
im2.save("fish_blur.jpg", "jpeg")

