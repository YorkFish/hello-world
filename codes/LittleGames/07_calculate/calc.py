import re
from tkinter import *


def validate_input():
    """验证输入是否合法
    +123 -123
    123. .123
    -123.456
    """
    reg = r"^[+-]?[1-9]\d*\.?\d*|\.\d+|0$"
    r1 = re.match(reg, op1.get())
    r2 = re.match(reg, op2.get())
    return r1 and r2


def cmd_math(ops):
    if validate_input():
        # eval() 挺危险的，如 eval("os.system('rm -rf *')")
        op1_val = eval(op1.get())
        op2_val = eval(op2.get())
        if ops == '+':
            res = op1_val + op2_val
        elif ops == '-':
            res = op1_val - op2_val
        elif ops == '*':
            res = op1_val * op2_val
        elif ops == '/':
            res = op1_val / op2_val
        elif ops == '%':
            res = op1_val % op2_val
        elif ops == '//':
            res = op1_val // op2_val
        elif ops == '**':
            res = op1_val ** op2_val
        res_var.set(round(res, 2))  # round:离目标位更近的数，若是5，选择偶数那一端
    else:
        res_var.set("请输入正确的操作数！")


def clear():
    op1.delete(0, END)
    op2.delete(0, END)
    res_var.set("Show Result")


def calc_art():
    ex = op_art.get()
    if re.findall("[a-zA-Z]", ex):
        res_str.set("别乱输入，不能有字母！")
    elif ex != '':
        res = eval(ex)
        res_str.set(res)


def clear_art():
    op_art.delete(0, END)
    res_str.set("计算结果")


def calc_bmi():
    gender = var_gender.get()
    height = float(var_height.get()) / 100
    weight = float(var_weight.get())
    res = weight / (height * height)
    res = round(res, 2)
    var_bmi1.set(str(res))
    if res <= 18.4:
        var_bmi2.set("偏瘦")
    elif res <= 23.9:
        var_bmi2.set("正常")
    elif res <= 27.9:
        var_bmi2.set("过重")
    elif res < 32:
        var_bmi2.set("肥胖")
    else:
        var_bmi2.set("建议重新输入")


# 创建窗口
root = Tk()

f2 = Frame(root)
f2.grid(row=0, column=0, sticky="news")
f1 = Frame(root)
f1.grid(row=0, column=0, sticky="news")

f3 = Frame(root)
f3.grid(row=0, column=0, sticky="news")

# 设置菜单栏
menubar = Menu(root)
menu1 = Menu(menubar)
menu1.add_command(label="普通", command=lambda: f1.tkraise())
menu1.add_command(label="文艺", command=lambda: f2.tkraise())
menubar.add_cascade(label="模式", menu=menu1)

menu2 = Menu(menubar)
menu2.add_command(label="BMI", command=lambda: f3.tkraise())
menubar.add_cascade(label="健康", menu=menu2)
root.config(menu=menubar)

# 普通模式
# 创建组件
note1 = StringVar()
note1.set("num1:")
num1 = Label(f1, textvariable=note1)
note2 = StringVar()
note2.set("num2:")
num2 = Label(f1, textvariable=note2)

op1 = Entry(f1)
op2 = Entry(f1)

btn_add = Button(f1, text='+', padx=50, pady=10,
                 command=lambda: cmd_math('+'))
btn_sub = Button(f1, text='-', padx=50, pady=10,
                 command=lambda: cmd_math('-'))
btn_mul = Button(f1, text='*', padx=50, pady=10,
                 command=lambda: cmd_math('*'))
btn_div = Button(f1, text='/', padx=50, pady=10,
                 command=lambda: cmd_math('/'))
btn_mod = Button(f1, text='%', padx=50, pady=10,
                 command=lambda: cmd_math('%'))
btn_flr = Button(f1, text='//', padx=50, pady=10,
                 command=lambda: cmd_math('//'))
btn_exp = Button(f1, text='**', padx=50, pady=10,
                 command=lambda: cmd_math('**'))
btn_clr = Button(f1, text='Clear', padx=50, pady=10, command=clear)

# 摆放组件
res_var = StringVar()
res_var.set("Show Result")
result = Label(f1, textvariable=res_var, pady=50)

num1.grid(row=0, column=0)
op1.grid(row=0, column=1, columnspan=3, sticky="WE")
num2.grid(row=1, column=0)
op2.grid(row=1, column=1, columnspan=3, sticky="WE")

btn_add.grid(row=2, column=0, sticky="WE")
btn_sub.grid(row=2, column=1, sticky="WE")
btn_mul.grid(row=2, column=2, sticky="WE")
btn_div.grid(row=2, column=3, sticky="WE")
btn_mod.grid(row=3, column=0, sticky="WE")
btn_flr.grid(row=3, column=1, sticky="WE")
btn_exp.grid(row=3, column=2, sticky="WE")
btn_clr.grid(row=3, column=3, sticky="WE")
result.grid(row=4, column=0, columnspan=4, sticky="WE")

# 文艺模式
# 创建组件
op_art = Entry(f2)
btn_art = Button(f2, text="计算", command=calc_art)
btn_art_clr = Button(f2, text='Clear', command=clear_art)

res_str = StringVar()
res_str.set("计算结果")
label_art = Label(f2, textvariable=res_str)

# 摆放组件
op_art.pack(fill=BOTH)
btn_art.pack(fill=BOTH)
btn_art_clr.pack(fill=BOTH)
label_art.pack(fill=BOTH)

# BMI
# 创建组件
var_gender = StringVar()
var_gender.set('F')
res_f3 = Label(f3, textvariable=var_gender, pady=50)
btn_bmi_gender0 = Radiobutton(f3, text="女性", variable=var_gender, value='F')
btn_bmi_gender1 = Radiobutton(f3, text="男性", variable=var_gender, value='M')
btn_bmi_gender0.place(x=160, y=20)
btn_bmi_gender1.place(x=230, y=20)

# 摆放组件
Label(f3, text="我的性别：").place(x=80, y=20)
Label(f3, text="我的身高：").place(x=80, y=60)
Label(f3, text="厘米 cm").place(x=310, y=60)
Label(f3, text="我的体重：").place(x=80, y=100)
Label(f3, text="千克 Kg").place(x=310, y=100)
Label(f3, text="BMI 标准：    中国标准").place(x=80, y=140)
Label(f3, text="计算结果：").place(x=80, y=180)
Label(f3, text="数值分析：").place(x=80, y=220)

var_height = StringVar()
entry_height = Entry(f3, textvariable=var_height)
entry_height.place(x=160, y=60)

var_weight = StringVar()
entry_weight = Entry(f3, textvariable=var_weight)
entry_weight.place(x=160, y=100)

var_bmi1 = StringVar()
entry_bmi1 = Entry(f3, textvariable=var_bmi1)
entry_bmi1.place(x=160, y=180)

var_bmi2 = StringVar()
entry_bmi2 = Entry(f3, textvariable=var_bmi2)
entry_bmi2.place(x=160, y=220)

btn_bmi_calc = Button(f3, bg="#209aea", text="计算 BMI", command=calc_bmi)
btn_bmi_calc.place(x=400, y=220)

# root.geometry("400x400+100+100")
mainloop()
