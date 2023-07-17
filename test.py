from tkinter import *  # 导入窗口控件
from tkinter.ttk import *

root = Tk()  # 创建窗口
root.title("label-test")
root.geometry("800x550+300+100")  # 小写x代表乘号500x400为窗口大小，+500+300窗口显示位置

# 这句很关键
root.columnconfigure(0, weight=1)  # 保证可以随着窗口一起缩放
root.columnconfigure(1, weight=1)  # 保证可以随着窗口一起缩放
root.columnconfigure(2, weight=1)  # 保证可以随着窗口一起缩放
root.rowconfigure(1, weight=1)  # 允许treeview跟着窗口大小一起缩放


def test():
    pass


# 执行排序操作
def treeview_sortColumn(col):
    global reverseFlag  # 定义排序标识全局变量
    lst = [(tree_name.set(st, col), st) for st in tree_name.get_children("")]
    print(lst)  # 打印列表
    lst.sort(reverse=reverseFlag)  # 排序列表
    print(lst)  # 打印列表
    for index, item in enumerate(lst):  # 重新移动项目内容
        tree_name.move(item[1], "", index)
    reverseFlag = not reverseFlag  # 更改排序标识


# 对表格间隔颜色
def tree_color():  # 表格栏隔行显示不同颜色函数
    items = tree1.get_children()  # 得到根目录所有行的iid
    i = 0  # 初值
    for hiid in items:
        if i / 2 != int(i / 2):  # 判断奇偶
            tag1 = ''  # 奇数行
        else:
            tag1 = 'even'  # 偶数行
        tree1.item(hiid, tag=tag1)  # 偶数行设为浅蓝色的tag='even'
        i += 1  # 累加1


# 动态插入数据
def update_treeview(tree_name, tree_values):
    header_info = tree_values[0]

    tree_name["columns"] = header_info

    for head_name in header_info:
        # tree_name.heading(head_name, text=head_name)
        tree_name.heading(head_name, text=head_name, command=lambda c=head_name: treeview_sortColumn(c))  # 重点是command

    for i in range(1, len(tree_values)):
        if i % 2 == 1:
            tree_name.insert("", index=END, text="", values=tree_values[i], tags='evenColor')
        else:
            tree_name.insert("", index=END, text="", values=tree_values[i])


# 删除所有的项目
def delete_all_item():
    iids = tree_name.get_children()  # 获取根节点下所有行的iid，元组
    for iid in iids:  # 用循环把所有行再重新设置新的tags
        tree_name.delete(iid)

    tree_name.update()  # 及时更新treeview


def update_info():
    update_treeview(tree, tree_head_value_list)


Button(root, text="发版系统查询", command=update_info).grid(row=0, column=0)
Button(root, text="任务查询", command=test).grid(row=0, column=1)
Button(root, text="缺陷查询", command=test).grid(row=0, column=2)

reverseFlag = False

tree = Treeview(root, show="headings", selectmode=EXTENDED)  # 表格第一列不显示
tree.tag_configure('evenColor', background='lightblue')  # 打了标签
tree.grid(row=1, column=0, columnspan=3, sticky=W + E + N + S)


def fixed_map(option):
    return [elm for elm in style.map("Treeview", query_opt=option) if elm[:2] != ("!disabled", "!selected")]


style = Style()
style.map("Treeview", foreground=fixed_map("foreground"), background=fixed_map("background"))

tree_head_value_list = []
tree_head_value_list.append(("序号", "企业名称", "详细信息", "aa"))

name = "辽宁忠旺集团"
addurl = "辽宁省沈阳市铁西区22号"
aa = ".........................................................."

for i in range(16):
    tree_head_value_list.append((i, name, addurl, aa))

'''
tree["columns"] = ("序号", "企业名称", "详细信息","aa")   #这种方式设置的话，就没有占用图栏位了

# 格式化栏位，可以要也可以不要 设置列，不显示
tree.column("序号", width=100, anchor = CENTER)
tree.column("企业名称", width=100)
tree.column("详细信息", width=300)
tree.column("aa", width=300)

# 显示表头
tree.heading("序号", text="序号")
tree.heading("企业名称", text="企业名称")
tree.heading("详细信息", text="详细信息")
tree.heading("aa", text="aa")

i = 0
ii = 0
name = "辽宁忠旺集团"
addurl = "辽宁省沈阳市铁西区22号"
aa = ".........................................................."

tree.insert("", index=0, text="", values=(i, name, addurl, aa)) #text本来应该是写图栏位的名字的，但是我们没有设置，所以为空
tree.insert("", index=0, text="", values=(ii, "1", addurl, aa)) #index=0表示插入第一行
tree.insert("", index=END, text="", values=(ii, "2", addurl, aa))   #index=END表示插入最后一行
tree.insert("", i, text="", values=(ii, "3", addurl, aa))
tree.insert("", i, text="", values=(ii, "4", addurl, aa))
tree.insert("", i, text="", values=(ii, "5", addurl, aa))
tree.insert("", i, text="", values=(ii, "6", addurl, aa))
tree.insert("", i, text="", values=(ii, "7", addurl, aa))
tree.insert("", i, text="", values=(ii, "8", addurl, aa))
tree.insert("", i, text="", values=(ii, "9", addurl, aa))
tree.insert("", i, text="", values=(ii, "10", addurl, aa))
tree.insert("", i, text="", values=(ii, "11", addurl, aa))
tree.insert("", i, text="", values=(ii, "12", addurl, aa))
tree.insert("", i, text="", values=(ii, "13", addurl, aa))
tree.insert("", i, text="", values=(ii, "14", addurl, aa))
tree.insert("", i, text="", values=(ii, "15", addurl, aa))
'''

"""
    定义滚动条控件
    orient为滚动条的方向，vertical--纵向，horizontal--横向
    command=tree.yview 将滚动条绑定到treeview控件的Y轴
"""
# scroll_ty = Scrollbar(root, orient=VERTICAL, command=tree.yview)
# scroll_ty.grid(row=1, column=3, sticky=N+S)
# tree['yscrollcommand']=scroll_ty.set   #tree.configure(yscrollcommand=vbar.set)  二个等价的

# ----vertical scrollbar------------
vbar = Scrollbar(root, orient=VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=vbar.set)
vbar.grid(row=1, column=3, sticky=NS)  # 比其他元素大一个，sticky=(N,S) 使控件上下方向拉伸，并保持横向居中

# ----horizontal scrollbar----------
hbar = Scrollbar(root, orient=HORIZONTAL, command=tree.xview)
tree.configure(xscrollcommand=hbar.set)
hbar.grid(row=2, column=0, columnspan=3, sticky=EW)  # sticky=(W,E) 使控件左右方向拉伸，并保持上下居中，和treeview保持一致的格式

Button(root, text="发版系统查询", command=test).grid(row=3, column=0)
Button(root, text="任务查询", command=test).grid(row=3, column=1)
Button(root, text="缺陷查询", command=test).grid(row=3, column=2)

root.mainloop()  # 显示窗口  mainloop 消息循环