from PyQt5 import Qsci
from PyQt5 import QtGui


class Lexer(Qsci.QsciLexerCustom):
    Default = 0  # 默认
    Comment = 1  # 注释
    Number = 2  # 数字
    String = 3  # 字符串
    Bool = 4  # 布尔值
    Reserved = 5  # 保留字
    Function = 6  # 函数名
    Identifier = 7  # 标识符

    def __init__(self, parent):
        super(Lexer, self).__init__(parent=parent)

    def description(self, style):
        if style == self.Default:
            return "Default"
        elif style == self.Comment:
            return "Comment"
        elif style == self.Number:
            return "Number"
        elif style == self.String:
            return "String"
        elif style == self.Reserved:
            return "Reserved"
        elif style == self.Function:
            return "Function"
        elif style == self.Identifier:
            return "Identifier"

    def defaultColor(self, style):
        if style == self.Default:
            return QtGui.QColor("#000000")
        elif style == self.Comment:
            return QtGui.QColor("#778899")
        elif style == self.Number:
            return QtGui.QColor("#CD5C5C")
        elif style == self.String:
            return QtGui.QColor("#CD2626")
        elif style == self.Reserved:
            return QtGui.QColor("#FF8C00")
        elif style == self.Function:
            return QtGui.QColor("#87CEFA")
        elif style == self.Identifier:
            return QtGui.QColor("#9400D3")

    def styleText(self, start, end):
        # 得到编辑器
        editor = self.editor()
        # 如果编辑器未初始化则返回
        if editor is None:
            return

        # scintilla是基于bytes而工作的，而不是characters
        # 如果源码中含有非ascii码字符会导致多字节编码而导致位置不准确
        # scintilla works with encoded bytes, not decoded characters.
        # this matters if the source contains non-ascii characters and
        # a multi-byte encoding is used (e.g. utf-8)
        source = ''  # 初始化源码字符串为空字符串
        if end > editor.length():  # 如果结束下标大于源码长度
            end = editor.length()  # 把结束下标置成源码长度，为什么不减1?
        if end > start:
            # if sys.hexversion >= 0x02060000:
            # faster when styling big files, but needs python 2.6
            source = bytearray(end - start)  # 把源码编码成byte数组
            editor.SendScintilla(editor.SCI_GETTEXTRANGE, start, end, source)
        # else:
        #     source = unicode(editor.text()
        #                     ).encode('utf-8')[start:end]
        if not source:
            return

        # the line index will also be needed to implement folding
        index = editor.SendScintilla(editor.SCI_LINEFROMPOSITION, start)
        if index > 0:
            # the previous state may be needed for multi-line styling
            pos = editor.SendScintilla(editor.SCI_GETLINEENDPOSITION, index - 1)
            state = editor.SendScintilla(editor.SCI_GETSTYLEAT, pos)
        else:
            state = self.Default

        # 0x1f = 31
        self.startStyling(start, 0x1f)

        # scintilla always asks to style whole lines
        for line in source.splitlines(True):
            length = len(line)
            if line.startswith(b"//"):
                state = self.Comment
                self.setStyling(length, state)
            else:
                token = ""
                for pos, byte in enumerate(line):
                    if byte == b" ":
                        state = self.Default
                        self.setStyling(1, state)
                        print(token)
                        token = ""
                    token += str(byte, encoding="utf-8")
            # folding implementation goes here
            index += 1
