#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from PyQt4.QtCore import QProcess
from PyQt4.QtGui import QWidget, QVBoxLayout, QPushButton, QApplication, QLineEdit

# Compruebo que tenga tmux
import distutils.spawn

if not distutils.spawn.find_executable("tmux"):
    raise Warning("tmux no está instalado!")


class embeddedTerminal(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self._processes = []
        self.banned_words = ['exit', 'prohibido']
        self.resize(800, 600)
        self.terminal = QWidget(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.terminal)
        self.kill_tmux()
        
        # self._start_process('tmux', ['new', '-s', 'npy'])
        # self._start_process('tmux', ['detach-client', '-s', 'npy'])

        # self._start_process('xterm',
        #                     ['-geometry', '640x480+0+0', '-into', str(self.terminal.winId()),
        #                      '-e', 'tmux', 'new', '-s', 'npy'])

        self._start_process('xterm', ['-fa', 'Monospace', '-fs', '14', '-geometry', '640x480+0+0', '-into', str(self.terminal.winId()),
                            '-e', 'tmux', 'new', '-s', 'npy'])
        self.textBox = QLineEdit(self)
        self.button = QPushButton('run-in-terminal')
        self.textBox.returnPressed.connect(self.button.click)
        layout.addWidget(self.textBox)
        layout.addWidget(self.button)
        self.textBox.setFocus()
        self.button.clicked.connect(
            lambda: self.run_command(self.textBox.text()))
        self.button.setAutoDefault(True)

    def _start_process(self, prog, args):
        child = QProcess()
        self._processes.append(child)
        child.start(prog, args)

    def run_command(self, command):
        if command not in self.banned_words:
            self._start_process(
                'tmux', ['send-keys', '-t', 'npy:0', command, 'Enter'])
        self.textBox.clear()

    def closeEvent(self, event):
        self.kill_tmux()
        event.accept()

    def kill_tmux(self):
        self._start_process('tmux', ['kill-server'])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = embeddedTerminal()
    main.show()
    sys.exit(app.exec_())


# para tmux
# archivo en /home/usuario/tmux.conf
# set-option -g mouse on