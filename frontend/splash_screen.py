from PySide2.QtWidgets import QSplashScreen
from PySide2.QtGui import QPixmap, QPainter, QFont, QColor
from PySide2.QtCore import Qt, QTimer, QRect, QTime
import random

class ShadowPhishSplash(QSplashScreen):
    def __init__(self):
        self.counter = 0
        self.max_counter = 100
        self.opacity = 0
        self.current_message = "Initializing..."

        self.messages = [
            "Initializing offensive modules...",
            "Loading graphical interface...",
            "Starting deepfake engine...",
            "Checking C2 connections...",
            "Loading phishing templates...",
            "Booting ShadowPhish toolkit..."
        ]

        self.pixmap = QPixmap(800, 400)
        self.pixmap.fill(Qt.black)
        super().__init__(self.pixmap)
        self.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)
        self.setMask(self.pixmap.mask())

        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(50)

        self.msg_timer = QTimer()
        self.msg_timer.timeout.connect(self.update_message)
        self.msg_timer.start(900)

        self.time = QTime()

    def update_message(self):
        self.current_message = random.choice(self.messages)

    def animate(self):
        self.counter += 2
        self.opacity = min(255, int(255 * (self.counter / self.max_counter)))
        self.repaint()

        if self.counter >= self.max_counter:
            self.timer.stop()
            self.msg_timer.stop()

    def drawContents(self, painter):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.pixmap.rect(), Qt.black)

        glow = QColor(0, 255, 150, self.opacity)

        # Title
        title_font = QFont("Consolas", 28, QFont.Bold)
        painter.setFont(title_font)
        painter.setPen(glow)
        painter.drawText(QRect(0, 100, self.pixmap.width(), 50), Qt.AlignCenter, "ShadowPhish")

        # Subtitle
        sub_font = QFont("Consolas", 14)
        painter.setFont(sub_font)
        painter.setPen(QColor(180, 255, 220, self.opacity))
        painter.drawText(QRect(0, 150, self.pixmap.width(), 30), Qt.AlignCenter, "APT Awareness Toolkit")

        # Current message
        msg_font = QFont("Consolas", 10)
        painter.setFont(msg_font)
        painter.setPen(QColor(100, 255, 180, self.opacity))
        painter.drawText(QRect(0, 220, self.pixmap.width(), 20), Qt.AlignCenter, self.current_message)

        # Hacker-style progress bar
        bar_width = int((self.counter / self.max_counter) * 600)
        bar_height = 12
        bar_x = (self.pixmap.width() - 600) // 2
        bar_y = 260
        painter.setBrush(QColor(0, 255, 150, 200))
        painter.drawRect(bar_x, bar_y, bar_width, bar_height)

        # Credits
        credit_font = QFont("Consolas", 9)
        painter.setFont(credit_font)
        painter.setPen(QColor(180, 180, 180, self.opacity))
        painter.drawText(QRect(10, self.pixmap.height() - 35, 300, 20), Qt.AlignLeft, "Developed by Joas A Santos")

        painter.drawText(QRect(self.pixmap.width() - 100, self.pixmap.height() - 35, 90, 20), Qt.AlignRight, "v1.0")
