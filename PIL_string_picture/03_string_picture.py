# coding:utf-8

# 此程序功能：将图片转为字符画
from PIL import Image, ImageFilter

# 这个字符串是我随便敲的，就是大小写字母加一些常见字符
codeLib = '''ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz<=>:;+~-,.^"'*`_'''
count = len(codeLib)

def transform1(image_file):
	image_file = image_file.convert("L")						# L 为“黑白模式”
	codePic = ""												# 存储字符
	for h in range(image_file.size[1]):							# 图片的纵向像素值
		for w in range(image_file.size[0]):						# 图片的横向像素值
			gray = image_file.getpixel((w, h))					# 计算每个点的“灰度值”，也有别的方法
			codePic += codeLib[ int(count*gray/256)]			# 因为字符串不足 256 个
		codePic += "\r\n"										# 回车

	return codePic

fp = open(u"fish.png", "rb")									# 要变成字符画的原图，png 那张清楚一些
image_file = Image.open(fp)
image_file = image_file.resize((int(image_file.size[0]*0.5), \
                                int(image_file.size[1]*0.25)))	# 高质量缩放

tmp = open("fish.txt", "w")										# 变成字符画后的文件
tmp.write(transform1(image_file))
tmp.close()

