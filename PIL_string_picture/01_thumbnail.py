# coding:utf-8

# 此程序功能：缩放
from PIL import Image

im = Image.open("fish.jpg")
w, h = im.size					# 获得图像大小；w: 宽，h: 高
im.thumbnail((w//2, h//2))		# 将新图的宽与高均设置为原来的一半
im.save("fish_thumbnail.jpg", "jpeg")

