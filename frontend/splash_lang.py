# frontend/splash_lang.py

from PySide2.QtWidgets import QSplashScreen
from PySide2.QtGui import QPixmap, QPainter, QFont, QColor
from PySide2.QtCore import Qt, QTimer, QRect

class SplashInicial(QSplashScreen):
    def __init__(self):
        pixmap = QPixmap(600, 300)
        pixmap.fill(Qt.black)
        super().__init__(pixmap)
        self.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)

        self.counter = 0
        self.max_counter = 60
        self.opacity = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(30)

    def update_animation(self):
        self.counter += 2
        self.opacity = min(255, int(255 * (self.counter / self.max_counter)))
        self.repaint()
        if self.counter >= self.max_counter:
            self.timer.stop()

    def drawContents(self, painter):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.pixmap().rect(), Qt.black)
        glow = QColor(0, 255, 150, self.opacity)

        font = QFont("Consolas", 20, QFont.Bold)
        painter.setFont(font)
        painter.setPen(glow)
        painter.drawText(QRect(0, 100, self.pixmap().width(), 50), Qt.AlignCenter, "ShadowPhish")
        sub_font = QFont("Consolas", 12)
        painter.setFont(sub_font)
        painter.setPen(QColor(180, 255, 220, self.opacity))
        painter.drawText(QRect(0, 160, self.pixmap().width(), 30), Qt.AlignCenter, "Loading Interface...")
