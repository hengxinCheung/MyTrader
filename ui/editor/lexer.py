import re
from PyQt5 import Qsci
from PyQt5 import QtGui
from mytrader.mylang import constants
from mytrader.mylang import builtins


class Lexer(Qsci.QsciLexerCustom):
    styles = {
        "Default": 0,
        "Comment": 1,
        "Number": 2,
        "String": 3,
        "Reserved": 4,
        "Function": 5,
        "Identifier": 6,
    }
    reserved = constants.reserved
    function = dir(builtins)

    def __init__(self, parent):
        super(Lexer, self).__init__(parent=parent)

        # 设置默认属性
        self.setDefaultColor(QtGui.QColor("#000000"))
        self.setDefaultFont(QtGui.QFont("Courier", 14))
        # 初始化词素的颜色
        self.init_colors()

        # 编译标识符的正则表达式
        self.id_regexp = re.compile(r"^[a_zA-Z].*$")

    def init_colors(self):
        self.setColor(QtGui.QColor("#000000"), self.styles["Default"])
        self.setColor(QtGui.QColor("#778899"), self.styles["Comment"])
        self.setColor(QtGui.QColor("#CD5C5C"), self.styles["Number"])
        self.setColor(QtGui.QColor("#CD2626"), self.styles["String"])
        self.setColor(QtGui.QColor("#FF8C00"), self.styles["Function"])
        self.setColor(QtGui.QColor("#9400D3"), self.styles["Identifier"])

    def language(self):
        return "MyLang"

    def description(self, style):
        if style < len(self.styles):
            description = "Custom lexer for the MyLang programming languages"
        else:
            description = ""
        return description

    def styleText(self, start, end):
        # 开始染色
        self.startStyling(start)
        # 获取染色部分的文本
        text = self.parent().text()[start:end]
        # 定义分隔符
        splitter = re.compile(r"(\{\.|\.\}|//|\'|\"\"\"|\n|\s+|\w+|\W)")
        # 获取词素
        tokens = [(token, len(bytearray(token, "utf-8"))) for token in splitter.findall(text)]
        # 标识符
        string_begin_flag = False
        comment_begin_flag = False
        # 用一个循环来染色
        for i, token in enumerate(tokens):
            # 如果是注释开始
            if comment_begin_flag:
                if token[0] == "\n":    # 换行标志注释结束
                    comment_begin_flag = False
                self.setStyling(token[1], self.styles["Comment"])
                continue
            # 如果是字符串开始
            if string_begin_flag:
                if token[0] == "\"" or token[0] == "\'":    # 字符串结束
                    string_begin_flag = False
                self.setStyling(token[1], self.styles["String"])
                continue
            if token[0] == "//":
                style = "Comment"
                comment_begin_flag = True
            elif token[0] == "\"" or token[0] == "\'":
                style = "String"
                string_begin_flag = True
            elif token[0].isdigit():
                style = "Number"
            elif token[0] in self.function:
                style = "Function"
            elif self.id_regexp.match(token[0]):
                style = "Identifier"
            else:
                style = "Default"
            self.setStyling(token[1], self.styles[style])
