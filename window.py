import tkinter as tk
from tkinter import ttk

# 创建主窗口
window = tk.Tk()
window.title("居中窗口")

# 获取屏幕的宽度和高度
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# 计算窗口的坐标位置
window_width = 900
window_height = 400
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# 设置窗口的大小和位置
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# 创建表格
tree = ttk.Treeview(window)

# 定义表格的列
tree["columns"] = ("select", "id", "seq", "password")

# 设置表格的列宽度和标题
tree.column("select", width=50, anchor="center")
tree.column("id", width=200, anchor="center")
tree.column("seq", width=100, anchor="center")
tree.column("password", width=200, anchor="center")

tree.heading("select", text="")
tree.heading("id", text="ID")
tree.heading("seq", text="Seq")
tree.heading("password", text="Password")

# 插入数据
json_data = [
    {'id': '2b49b0804f9045aaaf53623ded7efe72', 'seq': '10', 'password': ''},
    {'id': '6188d4fea0ff43f5ac2706853e53ea4a', 'seq': '9', 'password': 'Lilinhaifacai10009'},
    {'id': 'f3a508b1191a40a98136616ba844e99a', 'seq': '8', 'password': 'Lilinhaifacai10008'},
    {'id': '58fde22055cb4fb0917317208ed56723', 'seq': '7', 'password': 'Lilinhaifacai10007'},
    {'id': 'e1b3e19a942a4b918627636add36378e', 'seq': '6', 'password': 'Lilinhaifacai10006'},
    {'id': '7d6243dc319b405983e15928e83dd6f4', 'seq': '5', 'password': 'Lilinhaifacai10005'},
    {'id': '4a698055ec234b7d8dbe642e2d414214', 'seq': '4', 'password': 'Lilinhaifacai10004'},
    {'id': '1f2523bd9dfc4dae864a0a6e7a0a8d7a', 'seq': '3', 'password': 'Lilinhaifacai10003'},
    {'id': 'cd625bac7cc64a609a956d77c263a114', 'seq': '2', 'password': 'Lilinhaifacai10002'},
    {'id': '6ab388a860604795a6ce5f5c64ecddc0', 'seq': '1', 'password': 'Lilinhaifacai123'}
]

selected_items = []  # 存储选中的行的索引


def print_selected_items():
    for item in selected_items:
        values = tree.item(item)['values'][1:]  # Skip the checkbox column
        print(values)


def on_select(event):
    selected_items.clear()
    for item in tree.selection():
        selected_items.append(item)


def toggle_select(event):
    item = tree.identify("item", event.x, event.y)
    if item:
        checkbox_state = tree.set(item, "select")
        checkbox = window.nametowidget(checkbox_state)
        checkbox.toggle()
        on_select(None)


for item in json_data:
    seq = item['seq']
    select_var = tk.StringVar(value="")
    checkbox = tk.Checkbutton(window, variable=select_var)
    values = (checkbox, item['id'], item['seq'], item['password'])
    item_id = tree.insert("", "end", values=values, tags=("unselected",))

# 绑定事件
tree.tag_configure("selected", background="#A9A9A9")
tree.tag_bind("unselected", "<Button-1>", toggle_select)
tree.bind("<<TreeviewSelect>>", on_select)

# 显示表格
tree.pack()

# 创建标签组件
label = tk.Label(window, text="居中窗口")
label.pack()

# 使用按钮控件调用函数
button = tk.Button(window, text="打印选中项", command=print_selected_items)
button.pack()

# 运行主循环
window.mainloop()
