# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

# https://docs.python.org/3/library/logging.html
# https://docs.python.org/3/howto/logging-cookbook.html
# https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output
# https://stackoverflow.com/questions/42936810/python-logging-module-set-formatter-dynamically
# https://doc.qt.io/qt-6/qtquick-debugging.html
# https://raymii.org/s/articles/Disable_logging_in_QT_and_QML.html

import os
import sys
import time
import pathlib
import inspect
import logging

from PySide6.QtCore import QObject, Signal, Property, QtMsgType, QUrl, QSettings


LOGGER_LEVELS = {
    'disabled': 40,
    'error': 30,    # logging.CRITICAL, logging.ERROR, QtMsgType.QtSystemMsg, QtMsgType.QtCriticalMsg, QtMsgType.QtFatalMsg
    'info': 20,     # logging.INFO, logging.WARNING, QtMsgType.QtInfoMsg, QtMsgType.QtWarningMsg
    'debug': 10     # logging.NOTSET, logging.DEBUG, QtMsgType.QtDebugMsg
}


class Logger:

    def __init__(self):
        self._count = 0
        self._level = self._getLevelFromSettings()
        self._getLevelFromSettings()
        #self._timestamp = QTime.currentTime().toString("hh:mm:ss.zzz")
        self._startTime = time.time()

        #self._consoleFormat = logging.Formatter('{asctime}.{msecs:03.0f} {message}', datefmt='%H:%M:%S', style='{')
        self._consoleFormat = logging.Formatter('{message}', datefmt='%H:%M:%S', style='{')
        self._consoleHandler = logging.StreamHandler()
        self._consoleHandler.setFormatter(self._consoleFormat)

        self._logger = logging.getLogger()
        self._logger.setLevel(logging.NOTSET)
        self._logger.addHandler(self._consoleHandler)

    def debug(self, msg):
        level = 'debug'
        self._pyMessageHandler(level, msg)

    def info(self, msg):
        level = 'info'
        self._pyMessageHandler(level, msg)

    def error(self, msg):
        level = 'error'
        self._pyMessageHandler(level, msg)

    def qmlMessageHandler(self, msgType, context, message):
        level = Logger.qtMsgTypeToCustomLevel(msgType)
        if LOGGER_LEVELS[level] < LOGGER_LEVELS[self._level]:
            return
        category = 'qml'
        funcName = context.function
        filePath = QUrl(context.file).toLocalFile()
        if filePath == '':
            filePath = None
        lineNo = context.line
        msg = self._formattedConsoleMsg(message, level, category, funcName, filePath, lineNo)
        self._logger.debug(msg)

    def _pyMessageHandler(self, level, msg):
        if LOGGER_LEVELS[level] < LOGGER_LEVELS[self._level]:
            return
        category = 'py'
        caller = inspect.getframeinfo(sys._getframe(2))
        funcName = caller.function
        filePath = os.path.relpath(caller.filename)
        lineNo = caller.lineno
        msg = self._formattedConsoleMsg(msg, level, category, funcName, filePath, lineNo)
        self._logger.debug(msg)

    def _getLevelFromSettings(self):
        # NEED FIX: Duplication from main.py
        appName = 'EasyExample'
        homeDirPath = pathlib.Path.home()
        settingsIniFileName = 'settings.ini'
        settingsIniFilePath = str(homeDirPath.joinpath(f'.{appName}', settingsIniFileName))
        settings = QSettings(settingsIniFilePath, QSettings.IniFormat)
        level = settings.value("Preferences.Develop/loggingLevel", 'debug')
        level = level.lower()
        return level

    def _timing(self):
        endTime = time.time()
        timing = endTime - self._startTime
        self._startTime = endTime
        if timing < 0.001:
            return ' ' * 8
        elif timing < 60:
            return f'{timing:7.3f}s'
        elif timing < 3600:
            timing /= 60
            return f'{timing:7.3f}m'
        else:
            timing /= 3600
            return f'{timing:7.3f}h'

    def _formattedConsoleMsg(self, msg, level, category, funcName, filePath, lineNo):
        self._count += 1
        if funcName is None:
            funcName = ''
        sourceUrl = ''
        try:
            cwd = os.getcwd()
            parent = os.path.join(cwd, '..')
            start = os.path.abspath(parent)
            relativePath = os.path.relpath(filePath, start)
            fileUrl = f'file://{relativePath}'
            sourceUrl = f'{fileUrl}:{lineNo}'
        except:
            pass
        return f'{self._count:>5d} {self._timing()} {category:>4} {level:<7} {msg:<80.80} {funcName:<34.34} {sourceUrl}'

    @staticmethod
    def qtMsgTypeToCustomLevel(msgType):
        return {
            QtMsgType.QtDebugMsg: 'debug',
            QtMsgType.QtInfoMsg: 'info',
            QtMsgType.QtWarningMsg: 'info',
            QtMsgType.QtCriticalMsg: 'error',
            QtMsgType.QtSystemMsg: 'error',
            QtMsgType.QtFatalMsg: 'error'
        }[msgType]


console = Logger()


class LoggerLevelHandler(QObject):
    levelChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._level = 'debug'

    # QML accessible properties

    @Property(str, notify=levelChanged)
    def level(self):
        return self._level

    @level.setter
    def level(self, newValue):
        newValue = newValue.lower()
        if self._level == newValue:
            return
        self._level = newValue
        self.levelChanged.emit()
        console._level = self._level
