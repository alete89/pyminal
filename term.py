#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from PyQt4.QtCore import QProcess
from PyQt4.QtGui import QWidget, QVBoxLayout, QPushButton, QApplication, QLineEdit


class embeddedTerminal(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self._processes = []
        self.resize(800, 600)
        self.terminal = QWidget(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.terminal)
        self._start_process('xterm',
                            ['-geometry', '640x480+0+0', '-into', str(self.terminal.winId()), '-e',
                             'tmux', 'new', '-s', 'ale']
                            )
        self.textBox = QLineEdit(self)
        self.button = QPushButton('run-in-terminal')
        layout.addWidget(self.textBox)
        layout.addWidget(self.button)
        self.textBox.setFocus()
        self.button.clicked.connect(lambda ignore: self.run_command(self.textBox.text()))

    def _start_process(self, prog, args):
        child = QProcess()
        self._processes.append(child)
        child.start(prog, args)

    def run_command(self, command):
        self._start_process('tmux', ['send-keys', '-t', 'ale:0', command, 'Enter'])
        self.textBox.clear()

    def closeEvent(self, event):
        self.kill_tmux()
        event.accept()

    def kill_tmux(self):
        self._start_process('tmux', ['kill-session', '-t', 'ale'])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = embeddedTerminal()
    main.show()
    sys.exit(app.exec_())
