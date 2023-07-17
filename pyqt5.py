import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, \
    QPushButton, QHeaderView, QCheckBox, QLineEdit, QHBoxLayout
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from tinydb import TinyDB, Query

import bit_browser_request
import init_data
import main


# todo 没有解决map问题，还是通过json转map，可以转换成直接通过数据库获取id
# 没有解决分批获取比特浏览器的数据问题


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        db = TinyDB('data.json')

        layout = self.init_windows()

        json_data = sorted(db.all(), key=lambda item: item['seq'])

        # 关闭数据库连接
        db.close()

        map_data = self.json_to_map(json_data)

        self.table.setRowCount(len(json_data))

        for row, item in enumerate(json_data):
            id_item = QTableWidgetItem(item['id'])
            seq_item = QTableWidgetItem(str(item['seq']))
            password_item = QTableWidgetItem(item.get('metamask', ''))

            checkbox_item = QTableWidgetItem()
            checkbox_item.setFlags(checkbox_item.flags() | QtCore.Qt.ItemFlag.ItemIsUserCheckable)
            checkbox_item.setCheckState(QtCore.Qt.CheckState.Unchecked)

            seq_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.table.setItem(row, 0, checkbox_item)
            self.table.setItem(row, 1, seq_item)
            self.table.setItem(row, 2, id_item)
            self.table.setItem(row, 3, password_item)

            # 禁用编辑
            seq_item.setFlags(seq_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            id_item.setFlags(id_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)

            # 创建按钮
            button = QPushButton("点击打开")
            # 设置按钮样式
            button.setStyleSheet("background-color: lightblue;")
            # 连接点击事件的槽函数
            button.clicked.connect(lambda checked, seq=item['seq']: self.open_single_browser(seq))
            # 将按钮添加到表格中
            self.table.setCellWidget(row, 4, button)

        # 设置表格自适应大小
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

        # 设置表头为自适应模式
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)  # 设置选择列宽度为固定大小
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)  # 设置浏览器序列列宽度为自动拉伸
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # 设置浏览器ID列宽度为自动拉伸
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)  # 设置小狐狸密码列宽度为自动拉伸
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)  # 设置Action列宽度为固定大小

        # 设置列宽度
        self.table.setColumnWidth(0, 30)  # 设置选择列宽度
        self.table.setColumnWidth(1, 70)  # 设置选择列宽度
        self.table.setColumnWidth(4, 150)  # 设置Action列宽度

        # 并将表格添加到布局中
        layout.addWidget(self.table)

        # 创建中心窗口部件并设置布局
        central_widget = QWidget()
        central_widget.setLayout(layout)

        # 将中心窗口部件设置为主窗口的中心部件
        self.setCentralWidget(central_widget)

        # 创建全选复选框
        self.select_all_checkbox = QCheckBox("全选")
        self.select_all_checkbox.setTristate(False)
        self.select_all_checkbox.stateChanged.connect(self.toggle_select_all)
        layout.addWidget(self.select_all_checkbox)

        # 创建输入框和按钮布局
        input_layout = QHBoxLayout()

        # 创建标签
        label = QLabel("本次需要打开的网站：(可打开多个网站使用,分割)")
        input_layout.addWidget(label)

        # 创建输入框
        self.input_box = QLineEdit()
        input_layout.addWidget(self.input_box)

        # 将输入框和按钮布局添加到主布局中
        layout.addLayout(input_layout)

        # 创建按钮用于批量打开
        self.output_button = QPushButton("批量打开")
        self.output_button.clicked.connect(self.open_multiple_browsers)
        self.output_button.setStyleSheet("background-color: lightblue;")
        layout.addWidget(self.output_button)

    def init_windows(self):
        # 设置窗口标题
        self.setWindowTitle("批量打开指纹浏览器")
        # 获取屏幕的宽度和高度
        screen_width = QApplication.primaryScreen().size().width()
        screen_height = QApplication.primaryScreen().size().height()
        # 计算窗口的坐标位置
        window_width = 900
        window_height = 450
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        # 创建布局
        layout = QVBoxLayout()
        # 创建按钮用于批量打开
        self.output_button = QPushButton("数据初始化")
        self.output_button.clicked.connect(lambda: self.init_data())
        layout.addWidget(self.output_button)

        # 创建按钮用于保存数据
        self.save_button = QPushButton("保存数据")
        self.save_button.clicked.connect(self.save_data)
        self.save_button.setStyleSheet("background-color: lightblue;")
        layout.addWidget(self.save_button)

        # 设置窗口的大小和位置
        self.setGeometry(x, y, window_width, window_height)
        # 创建表格
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["选择", "浏览器序列", "浏览器ID", "小狐狸密码", "Action"])
        return layout

    def open_single_browser(self, seq):
        print(f"正在打开序号为: {seq}，的浏览器，请稍等！")
        input_value = self.input_box.text()

        # 创建 TinyDB 实例并加载数据文件
        db = TinyDB('data.json')
        # 创建查询条件
        query = Query()
        result = db.search(query.seq == seq)
        # 打印查询结果
        print(result)
        # 关闭数据库连接
        db.close()
        for item in result:
            main.main(item, input_value)

    def toggle_select_all(self, state):
        check_state = Qt.CheckState.Checked if state else Qt.CheckState.Unchecked
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item is not None:
                checkbox_item = QTableWidgetItem()
                checkbox_item.setCheckState(check_state)
                self.table.setItem(row, 0, checkbox_item)

    def open_multiple_browsers(self):
        selected_seqs = []
        for row in range(self.table.rowCount()):
            checkbox_item = self.table.item(row, 0)
            seq_item = self.table.item(row, 1)
            if checkbox_item.checkState() == QtCore.Qt.CheckState.Checked:
                selected_seqs.append(seq_item.text())

        print("正在批量打开浏览器:", selected_seqs)
        for num in selected_seqs:
            self.open_single_browser(int(num))

    def save_data(self):
        data = []
        for row in range(self.table.rowCount()):
            seq_item = self.table.item(row, 1)
            id_item = self.table.item(row, 2)
            password_item = self.table.item(row, 3)
            if seq_item and id_item and password_item:
                seq = int(seq_item.text())
                id = id_item.text()
                password = password_item.text()
                data.append({'seq': seq, 'id': id, 'metamask': password})

        db = TinyDB('data.json')
        db.truncate()
        db.insert_multiple(data)
        db.close()
        print("数据已保存到data.json文件。")

    def json_to_map(self, data):
        result = {}

        for item in data:
            seq = item['seq']
            id = item['id']
            password = item['metamask']
            result[seq] = {'id': id, 'password': password}
            # 返回数据

        return result

    def init_data(db):
        # 插入数据
        ori_data = bit_browser_request.browser_list()
        datajson = ori_data['data']['list']

        # 指定要筛选的字段
        fieldnames = ['id', 'seq']

        # 查询数据
        User = Query()

        # 对于每个字典，筛选出指定字段的键值对，构造新的字典
        for item in datajson:
            filtered_item = {key: item[key] for key in fieldnames}

            # 添加新的键，并将其值设置为空
            filtered_item['metamask'] = None

            # 查询是否已存在相同的seq
            existing_doc = db.get(User.seq == item['seq'])

            if existing_doc is None:
                # 不存在相同的seq，则插入文档
                db.insert(filtered_item)
            else:
                # 存在相同的seq，则不更新文档
                print(f"Document with seq {item['seq']} already exists, skipping update.")

        all_data = db.all()
        # 打印查询结果
        for document in all_data:
            print(document)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
