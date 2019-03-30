import turtle as tt
from math import sqrt

tt.setup(600, 600)			# 设置 600 x 600 的画布并居中
tt.hideturtle()				# 隐藏画笔
tt.pensize(6)				# 设置画笔粗细
tt.pencolor("#00f5ff")		# 设置画笔颜色

# 走到右上角
tt.seth(45)
tt.pu()
tt.fd(200)
tt.pd()

# 鱼的“脑门”
tt.seth(135)
tt.circle(200, 130)			# 相当于极坐标的 roll(r, angle)

# 鱼嘴
tt.pu()
tt.circle(200, 10)
tt.pd()

# 鱼腹
tt.circle(200, 130)

# 鱼“屁股”
tt.seth(0)
tt.circle(200/sqrt(2), -90)

# 鱼尾（开始）
tt.seth(-90)
tt.circle(100, 135)

tt.seth(0)
tt.circle(100/sqrt(2), -180)

# 鱼尾（结束）
tt.seth(135)
tt.circle(100, 135)

# 鱼“后背”
tt.seth(90)
tt.circle(-200/sqrt(2), 90)

# 鱼目
tt.pu()
tt.goto(-110, 50)
tt.pd()
tt.circle(20)

# 鱼珠
tt.pu()
tt.goto(-113, 70)
tt.pd()
tt.circle(6)

# 鱼嘴旁的小气泡
tt.pu()
tt.goto(-230, 60)
tt.pd()
tt.circle(15)

# 鱼嘴旁的大气泡
tt.pu()
tt.goto(-250, 120)
tt.pd()
tt.circle(30)

# 打个标签
tt.pu()
tt.goto(50, -260)
tt.pd()
tt.write("—— by YorkFish", font=("consolas", 20, "bold"))

tt.done()					# 绘制结束后停住