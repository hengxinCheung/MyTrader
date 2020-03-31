import sys
from PyQt5 import Qt, QtWidgets, QtCore, QtGui
from ui.editor.editor import Editor


class EditorBox(QtWidgets.QMainWindow):
    def __init__(self):
        super(EditorBox, self).__init__()

        self.init_ui()

    def init_ui(self):
        editor = Editor()
        self.setCentralWidget(editor)

        # #######
        # 工具栏
        # #######
        open_action = QtWidgets.QAction(QtGui.QIcon("images/file.png"), "打开文件", self)  # 创建一个打开文件动作
        open_action.setShortcut("Ctrl+O")  # 设置快捷按键
        open_action.setStatusTip("打开文件")  # 设置提示信息
        open_action.triggered.connect(self.open)  # 连接信号槽
        open_toolbar = self.addToolBar("Open")  # 添加到工具栏
        open_toolbar.addAction(open_action)

        save_action = QtWidgets.QAction(QtGui.QIcon("images/save.png"), "保存", self) # 创建一个保存动作
        save_action.setShortcut("Ctrl+S")   # 设置快捷按键
        save_action.setStatusTip("保存")   # 设置提示信息
        save_action.triggered.connect(self.save)    # 连接信号槽
        save_toolbar = self.addToolBar("Save")  # 添加到工具栏
        save_toolbar.addAction(save_action)

        compile_action = QtWidgets.QAction(QtGui.QIcon("images/compile.png"), "编译", self)  # 创建一个编译动作
        compile_action.setStatusTip("编译")  # 设置提示信息
        compile_action.setShortcut("F9")  # 设置快捷按键
        compile_action.triggered.connect(self.compile)  # 连接信号槽
        compile_toolbar = self.addToolBar("Compile")
        compile_toolbar.addAction(compile_action)

        run_action = QtWidgets.QAction(QtGui.QIcon("images/run.png"), "运行", self)  # 创建一个运行动作
        run_action.setStatusTip("运行")  # 设置提示信息
        run_action.setShortcut("F10")  # 设置快捷按键
        run_action.triggered.connect(self.run)  # 连接信号槽
        run_toolbar = self.addToolBar("Run")
        run_toolbar.addAction(run_action)

        # 状态栏
        self.statusBar().showMessage("@Author by HengxinCheung")

        self.setMinimumSize(760, 640)
        self.showMaximized()
        self.setWindowTitle("Editor for MyLang")
        self.show()

    def open(self):
        print("open")

    def save(self):
        print("save")

    def compile(self):
        print("compile")

    def run(self):
        print("run")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = EditorBox()
    sys.exit(app.exec_())