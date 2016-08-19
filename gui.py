# -*- coding: utf-8 -*-

__author__ = 'whyjay'
import functools
import re
import sys
import imp
import codecs
from PyQt4 import QtGui, QtCore
from run import *

CONVERT = 0
DEEMBED = 1

class WidgetMain(QtGui.QMainWindow):
    tmp_inputs = None

    def __init__(self):
        super(WidgetMain, self).__init__()

        self.in_dir = "./input"
        self.out_dir = "./output"

        self.parser = imp.load_source('parser', 'parser.py').Parser()
        self.converter = imp.load_source('converter', 'converter.py').Converter()
        self.de_embeder = imp.load_source('de_embeder', 'de_embeder.py').DeEmbeder()
        self.init_ui()

    # init
    def init_ui(self):
        page = QtGui.QWidget()

        # window geometry
        self.resize(480, 420)
        self.center()
        self.setWindowTitle(self.qs('modeler'))

        page.help = QtGui.QTextEdit(self)
        page.help.setReadOnly(True)
        page.help.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        page.help.setText(self.qs("\n"
                                  " * How to Use *\n\n"
                                  " 1) How to convert file format\n "
                                  "     - Put file into 'input' folder \n "
                                  "     - Click 'Convert' button and write the file name \n"
                                  "         ex) 'filename.s2p' or 'filename.mdif'\n"
                                  "     - Converted file will be created in 'output' folder \n\n"
                                  " 2) How to de-embed\n"
                                  "     - Put 2 csv files and a s2p file into 'input' folder\n"
                                  "     - Click 'De-embed' button and write file names\n"
                                  "         ex) 'file1.csv file2.s2p file3.csv'\n"
                                  "     - De-embeded file will be created in 'output' folder\n"))
        page.help.setFont(QtGui.QFont("SansSerif", 13))
        page.help.resize(480, 340)
        page.help.setAlignment(QtCore.Qt.AlignCenter)

        # Convert button
        page.cbtn = QtGui.QPushButton('Convert s2p <-> mdif', self)
        page.cbtn.setFont(QtGui.QFont("SansSerif", 13))
        page.cbtn.clicked.connect(functools.partial(
            self.dl_which_file, CONVERT
        ))
        page.cbtn.resize(page.cbtn.sizeHint())
        page.cbtn.move(30, 370)

        # De-embed button
        page.dbtn = QtGui.QPushButton('De-embed s2p file', self)
        page.dbtn.setFont(QtGui.QFont("SansSerif", 13))
        page.dbtn.clicked.connect(functools.partial(
            self.dl_which_file, DEEMBED
        ))
        page.dbtn.resize(page.dbtn.sizeHint())
        page.dbtn.move(290, 370)

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    #  dialogs
    def dl_which_file(self, which):
        titles = {
            CONVERT: 'Convert file format',
            DEEMBED: 'De-embed s2p file',
        }
        hints = {
            CONVERT: "Write the name of file which you want to convert\n\n"
                     "ex) 'filename.s2p' or 'filename.mdif'\n",
            DEEMBED: "Write the names of files that you want to de-embed\n\n"
                     "ex) 'left_pad_name.csv file_name.s2p right_pad_name.csv'\n"
        }

        text, ok = QtGui.QInputDialog.getText(self,
                                              titles.get(which),
                                              hints.get(which))
        if ok:
            inputs = [n.strip() for n in re.split("[ ,\-:]", str(text))]

            if which == DEEMBED and len(inputs) == 3:
                if self.valid_d(inputs):
                    result_dic = self.de_embeder.de_embed(*map(self.parser.parse, inputs))
                    result_str = self.converter.dic2s2p(result_dic)
                    new_name = "./output/de_embeded_{}.s2p".format(result_dic["name"])

                    with codecs.open(new_name, encoding='utf-8', mode='w') as fp:
                        fp.write(result_str)

            elif which == CONVERT and len(inputs) == 1:
                filename = inputs[0]
                if self.valid_c(filename):
                    dic = self.parser.parse(filename)
                    self.converter.convert(dic)
                    t = "s2p"
                    if dic["type"] == "s2p":
                        t = "mdif"
            else:
                help_message()

    def qs(self, s):
        return QtCore.QString(unicode(s, 'utf-8'))

    def valid_c(self, filename):
        # file format should be s2p or mdif
        if filename.split(".")[-1] != "s2p" and filename.split(".")[-1] != "mdif":
            print "File format error : input file should have s2p or mdif format"
            return 0
        # file existence check
        if not check_existence(filename):
            return 0
        return 1

    def valid_d(self, filenames):
        # file format should be csv, s2p, csv
        if filenames[0].split(".")[-1] != "csv" or \
                        filenames[1].split(".")[-1] != "s2p" or \
                        filenames[2].split(".")[-1] != "csv":
            print "File format error : 3 input files should have csv, s2p and csv format (in order)."
            return 0
        # file existence check
        for i in range(3):
            if not check_existence(filenames[i]):
                return 0
        return 1

def main():
    app = QtGui.QApplication(sys.argv)
    h = WidgetMain()
    h.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
