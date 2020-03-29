import sys
from PyQt5 import Qsci
from PyQt5 import Qt, QtCore, QtGui, QtWidgets
from ui.editor.lexer import Lexer


class Editor(Qsci.QsciScintilla):
    def __init__(self, parent=None):
        super(Editor, self).__init__(parent=parent)
        # 默认字体
        self.font = QtGui.QFont("Monospace", 12)

        # 词法解析器
        self.lexer = None

        # 标志内容是否发生改变
        self.text_change = False

        self.init_ui()
        self.init_lexer()
        self.init_signal()

    def init_ui(self):
        # 设置编码格式为utf-8
        self.setUtf8(True)
        # 设置以'\n'换行
        self.setEolMode(self.SC_EOL_LF)
        # 设置自动换行
        self.setWrapMode(self.WrapWord)
        # 设置默认字体
        self.setFont(self.font)

        # 设置tab键功能
        self.setTabWidth(4)  # Tab等于4个空格
        self.setIndentationsUseTabs(True)   # 行首缩进采用Tab键，反向缩进是Shift+Tab
        self.setIndentationWidth(4)  # 行首缩进宽度为4个空格
        self.setIndentationGuides(True)  # 显示虚线垂直线的方式来指示缩进
        self.setAutoIndent(True)  # 插入新行时，自动缩进将光标推送到与前一个相同的缩进级别

        # 设置光标
        self.setCaretWidth(2)   # 光标宽度（以像素为单位），0表示不显示光标
        self.setCaretForegroundColor(QtGui.QColor("darkCyan"))  # 光标颜色
        self.setCaretLineVisible(True)  # 高亮显示光标所在行
        self.setCaretLineBackgroundColor(QtGui.QColor('#FFCFCF'))  # 光标所在行的底色

        # 设置页边，有3种Margin：0-行号; 1-改动标识; 2-代码折叠
        self.setMarginsFont(self.font)  # 行号字体
        self.setMarginLineNumbers(0, True)  # 设置标号为0的页边显示行号
        self.setMarginWidth(0, '000')  # 行号宽度
        # self.setMarginBackgroundColor() # 设置页边背景颜色，这个api不会用

        # 设置自动补全
        # self.setAutoCompletionSource(Qsci.QsciScintilla.AcsAll)  # 对于所有Ascii码补全
        # self.setAutoCompletionCaseSensitivity(False)  # 取消自动补全大小写敏感
        # self.setAutoCompletionThreshold(1)  # 输入1个字符，就出现自动补全提示

        # 设置窗口大小
        self.setFixedSize(1024, 760)
        # 设置文档窗口的标题
        self.setWindowTitle("MyEditor")

    def init_lexer(self):
        # 语法高亮显示
        self.lexer = Qsci.QsciLexerPascal(self)
        self.setLexer(self.lexer)

    def init_signal(self):
        # 连接文本改动信号
        self.textChanged.connect(self.textChangedAction)

    def textChangedAction(self):
        self.text_change = True
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    editor = Editor()
    editor.show()

    sys.exit(app.exec_())