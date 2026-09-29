try:
    from PyQt6.QtWidgets import (
        QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QSizePolicy
    )
    from PyQt6.QtGui import (
        QPainter, QColor, QPen, QBrush, QFont, QLinearGradient, QRadialGradient, QPainterPath
    )
    from PyQt6.QtCore import Qt, QRectF, pyqtSignal, QSize
except ImportError:
    from PySide6.QtWidgets import (
        QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QSizePolicy
    )
    from PySide6.QtGui import (
        QPainter, QColor, QPen, QBrush, QFont, QLinearGradient, QRadialGradient, QPainterPath
    )
    from PySide6.QtCore import Qt, QRectF, Signal as pyqtSignal, QSize


class CircularHealthGauge(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.percentage = 100
        self.health_text = "Ottimo"
        self.health_color_hex = "#27AE60"
        self.setMinimumSize(185, 185)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def set_health(self, percentage: int, health_text: str, color_hex: str):
        self.percentage = max(0, min(100, percentage))
        self.health_text = health_text
        self.health_color_hex = color_hex
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)

        w = self.width()
        h = self.height()

        margin = 22.0
        size = min(w, h) - margin * 2.0
        if size < 60:
            size = 60

        cx = w / 2.0
        cy = (h / 2.0) - 10.0

        rect = QRectF(cx - size / 2.0, cy - size / 2.0, size, size)
        stroke_width = max(8.0, size * 0.08)

        outer_bezel = QPen(QColor("#B0C4D8"), stroke_width + 2, Qt.PenStyle.SolidLine)
        painter.setPen(outer_bezel)
        painter.drawArc(rect, 0, 360 * 16)

        bg_pen = QPen(QColor("#D6E1EC"), stroke_width, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawArc(rect, 0, 360 * 16)

        angle_span = int(- (self.percentage / 100.0) * 360.0 * 16)
        fg_color = QColor(self.health_color_hex)
        fg_pen = QPen(fg_color, stroke_width, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        painter.setPen(fg_pen)

        painter.drawArc(rect, 90 * 16, angle_span)

        inner_size = size - stroke_width * 2 - 6
        if inner_size > 20:
            inner_rect = QRectF(cx - inner_size / 2.0, cy - inner_size / 2.0, inner_size, inner_size)
            gradient = QRadialGradient(cx - inner_size * 0.15, cy - inner_size * 0.2, inner_size / 1.5)
            gradient.setColorAt(0, QColor("#FFFFFF"))
            gradient.setColorAt(0.6, QColor("#F0F5FA"))
            gradient.setColorAt(1, QColor("#D8E4F0"))

            painter.setPen(QPen(QColor("#9EB4C8"), 1))
            painter.setBrush(QBrush(gradient))
            painter.drawEllipse(inner_rect)

        painter.setPen(QColor("#0F2942"))
        font = QFont(self.font())
        font.setPointSize(int(size * 0.17))
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(
            QRectF(cx - size / 2.0, cy - size * 0.22, size, size * 0.35),
            Qt.AlignmentFlag.AlignCenter,
            f"{self.percentage}%"
        )

        painter.setPen(QColor("#486581"))
        font_sub = QFont(self.font())
        font_sub.setPointSize(int(max(8, size * 0.065)))
        font_sub.setBold(True)
        painter.setFont(font_sub)
        painter.drawText(
            QRectF(cx - size / 2.0, cy + size * 0.08, size, size * 0.2),
            Qt.AlignmentFlag.AlignCenter,
            "VITA RESIDUA"
        )

        badge_w = min(120.0, size * 0.72)
        badge_h = 22.0
        badge_rect = QRectF(cx - badge_w / 2.0, cy + size * 0.28, badge_w, badge_h)

        badge_grad = QLinearGradient(badge_rect.topLeft(), badge_rect.bottomLeft())
        base_col = QColor(self.health_color_hex)
        badge_grad.setColorAt(0, base_col.lighter(130))
        badge_grad.setColorAt(1, base_col.darker(110))

        painter.setPen(QPen(base_col.darker(130), 1))
        painter.setBrush(QBrush(badge_grad))
        painter.drawRoundedRect(badge_rect, 4, 4)

        painter.setPen(QColor("#FFFFFF"))
        font_badge = QFont(self.font())
        font_badge.setPointSize(9)
        font_badge.setBold(True)
        painter.setFont(font_badge)
        painter.drawText(badge_rect, Qt.AlignmentFlag.AlignCenter, self.health_text.upper())


class TemperatureBadge(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("InnerCard")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(12, 8, 12, 8)
        self.layout.setSpacing(3)

        header_layout = QHBoxLayout()
        self.lbl_title = QLabel("TEMPERATURA OPERATIVA")
        self.lbl_title.setObjectName("CardTitle")
        header_layout.addWidget(self.lbl_title)
        header_layout.addStretch()

        self.lbl_status = QLabel("NORMALE")
        self.lbl_status.setStyleSheet(
            "font-size: 10px; font-weight: bold; color: #047857; "
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #D1FAE5, stop:1 #A7F3D0); "
            "border: 1px solid #6EE7B7; border-radius: 3px; padding: 2px 6px;"
        )
        header_layout.addWidget(self.lbl_status)
        self.layout.addLayout(header_layout)

        val_layout = QHBoxLayout()
        self.lbl_icon = QLabel("🌡️")
        self.lbl_icon.setStyleSheet("font-size: 20px;")
        val_layout.addWidget(self.lbl_icon)

        self.lbl_val = QLabel("38 °C")
        self.lbl_val.setStyleSheet("font-size: 22px; font-weight: bold; color: #1E3A5F;")
        val_layout.addWidget(self.lbl_val)
        val_layout.addStretch()
        self.layout.addLayout(val_layout)

        self.lbl_detail = QLabel("Temperatura ottimale per SSD/HDD (< 50°C)")
        self.lbl_detail.setObjectName("MetricSubtext")
        self.layout.addWidget(self.lbl_detail)

    def set_temperature(self, temp_c: int | None):
        if temp_c is None:
            self.lbl_val.setText("N/D")
            self.lbl_status.setText("SCONOSCIUTA")
            self.lbl_status.setStyleSheet("color: #486581; background: #E2E8F0; border: 1px solid #CBD5E1; border-radius: 3px; padding: 2px 6px;")
            self.lbl_detail.setText("Sensore di temperatura non disponibile")
            return

        self.lbl_val.setText(f"{temp_c} °C")
        if temp_c < 45:
            self.lbl_status.setText("OTTIMALE")
            self.lbl_status.setStyleSheet("font-size: 10px; font-weight: bold; color: #047857; background: #D1FAE5; border: 1px solid #6EE7B7; border-radius: 3px; padding: 2px 6px;")
            self.lbl_detail.setText("Temperatura ottima e sicura per il disco")
        elif temp_c < 55:
            self.lbl_status.setText("NORMALE")
            self.lbl_status.setStyleSheet("font-size: 10px; font-weight: bold; color: #0369A1; background: #E0F2FE; border: 1px solid #7DD3FC; border-radius: 3px; padding: 2px 6px;")
            self.lbl_detail.setText("Temperatura operativa nella norma")
        elif temp_c < 65:
            self.lbl_status.setText("ATTENZIONE")
            self.lbl_status.setStyleSheet("font-size: 10px; font-weight: bold; color: #B45309; background: #FEF3C7; border: 1px solid #FCD34D; border-radius: 3px; padding: 2px 6px;")
            self.lbl_detail.setText("Temperatura elevata. Assicurare aerazione.")
        else:
            self.lbl_status.setText("CRITICO")
            self.lbl_status.setStyleSheet("font-size: 10px; font-weight: bold; color: #B91C1C; background: #FEE2E2; border: 1px solid #FCA5A5; border-radius: 3px; padding: 2px 6px;")
            self.lbl_detail.setText("Surriscaldamento! Rischio throttling/danno.")


class MetricCard(QFrame):
    def __init__(self, title: str, icon: str = "💾", parent=None):
        super().__init__(parent)
        self.setObjectName("InnerCard")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 8, 10, 8)
        self.layout.setSpacing(2)

        top_layout = QHBoxLayout()
        self.lbl_icon = QLabel(icon)
        self.lbl_icon.setStyleSheet("font-size: 14px;")
        top_layout.addWidget(self.lbl_icon)

        self.lbl_title = QLabel(title.upper())
        self.lbl_title.setObjectName("CardTitle")
        top_layout.addWidget(self.lbl_title)
        top_layout.addStretch()
        self.layout.addLayout(top_layout)

        self.lbl_val = QLabel("N/D")
        self.lbl_val.setObjectName("MetricValue")
        self.layout.addWidget(self.lbl_val)

        self.lbl_sub = QLabel("")
        self.lbl_sub.setObjectName("MetricSubtext")
        self.layout.addWidget(self.lbl_sub)

    def set_data(self, value: str, subtext: str = ""):
        self.lbl_val.setText(value)
        self.lbl_sub.setText(subtext)
        self.lbl_sub.setVisible(bool(subtext))


class DiskTabButton(QPushButton):
    clicked_disk = pyqtSignal(str)

    def __init__(self, device_path: str, model: str, life_pct: int, temp: int | None, color_hex: str, parent=None):
        super().__init__(parent)
        self.device_path = device_path
        self.setObjectName("DiskTabButton")
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumSize(210, 46)
        self.setFixedHeight(48)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(8)

        is_nvme = "nvme" in device_path.lower()
        icon_str = "⚡" if is_nvme else "💾"
        lbl_icon = QLabel(icon_str)
        lbl_icon.setStyleSheet("font-size: 18px;")
        lbl_icon.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        layout.addWidget(lbl_icon)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(1)
        text_layout.setContentsMargins(0, 0, 0, 0)

        lbl_path = QLabel(device_path)
        lbl_path.setStyleSheet("font-weight: bold; font-size: 12px; color: #1E3A5F;")
        lbl_path.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        text_layout.addWidget(lbl_path)

        short_model = model[:18] + "..." if len(model) > 18 else model
        lbl_model = QLabel(short_model)
        lbl_model.setStyleSheet("font-size: 10px; color: #486581;")
        lbl_model.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        text_layout.addWidget(lbl_model)
        layout.addLayout(text_layout)

        layout.addStretch()

        badge_layout = QVBoxLayout()
        badge_layout.setSpacing(2)
        badge_layout.setContentsMargins(0, 0, 0, 0)

        lbl_health = QLabel(f"{life_pct}%")
        lbl_health.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_health.setStyleSheet(
            f"font-weight: bold; font-size: 10px; color: #FFFFFF; "
            f"background-color: {color_hex}; border: 1px solid {color_hex}; "
            f"border-radius: 3px; padding: 1px 4px; min-width: 32px;"
        )
        lbl_health.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        badge_layout.addWidget(lbl_health)

        if temp is not None:
            lbl_temp = QLabel(f"{temp}°C")
            lbl_temp.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_temp.setStyleSheet(
                "font-weight: bold; font-size: 10px; color: #0369A1; "
                "background-color: #E0F2FE; border: 1px solid #7DD3FC; "
                "border-radius: 3px; padding: 1px 4px; min-width: 32px;"
            )
            lbl_temp.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
            badge_layout.addWidget(lbl_temp)

        layout.addLayout(badge_layout)

        self.clicked.connect(lambda: self.clicked_disk.emit(self.device_path))
