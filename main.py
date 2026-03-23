import sys
import warnings
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import os

warnings.filterwarnings("ignore", category=DeprecationWarning)

class JBLAnimation(QWidget):
    update_battery_signal = pyqtSignal(int, int, int, bool, int, int, bool, bool)
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.update_battery_signal.connect(self.update_battery_ui)
        
    def setup_ui(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(420, 500)
        
        self.card = QWidget(self)
        self.card.setObjectName("card")
        self.card.setStyleSheet("""
            QWidget#card {
                background-color: #ffffff;
                border-radius: 32px;
                border: 1px solid rgba(0, 0, 0, 0.1);
            }
        """)
        self.card.setGeometry(0, 0, self.width(), self.height())
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 50))
        shadow.setOffset(0, 4)
        self.card.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(self.card)
        layout.setContentsMargins(25, 30, 25, 30)
        layout.setSpacing(15)
        
        images_widget = QWidget()
        images_layout = QHBoxLayout(images_widget)
        images_layout.setSpacing(20)
        
        self.left_widget = self.create_ear_widget("left")
        self.case_widget = self.create_case_widget()
        self.right_widget = self.create_ear_widget("right")
        
        images_layout.addWidget(self.left_widget)
        images_layout.addWidget(self.case_widget)
        images_layout.addWidget(self.right_widget)
        images_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(images_widget)
        
        self.device_name = QLabel("JBL Wave Beam 2")
        self.device_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.device_name.setStyleSheet("font-size: 18px; font-weight: 600; color: #1c1c1e;")
        layout.addWidget(self.device_name)
        
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #34c759; font-size: 13px; font-weight: 500;")
        layout.addWidget(self.status_label)
        
        self.charging_info = QLabel("")
        self.charging_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.charging_info.setStyleSheet("color: #8e8e93; font-size: 11px;")
        layout.addWidget(self.charging_info)
        
    def create_ear_widget(self, side):
        widget = QWidget()
        widget.setFixedSize(100, 130)
        layout = QVBoxLayout(widget)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        label = QLabel()
        label.setFixedSize(80, 80)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        if side == "left":
            self.left_label = label
            self.load_image(self.left_label, "ear_left.png", 80)
        else:
            self.right_label = label
            self.load_image(self.right_label, "ear_right.png", 80)
        
        layout.addWidget(label)
        
        indicator = QWidget()
        indicator.setFixedSize(60, 3)
        indicator.setStyleSheet("background-color: #e5e5ea; border-radius: 1.5px;")
        
        fill = QWidget(indicator)
        fill.setGeometry(0, 0, 0, 3)
        fill.setStyleSheet("background-color: #34c759; border-radius: 1.5px;")
        
        layout.addWidget(indicator, alignment=Qt.AlignmentFlag.AlignCenter)
        
        percent_label = QLabel("0%")
        percent_label.setStyleSheet("color: #8e8e93; font-size: 11px; font-weight: 500;")
        percent_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(percent_label)
        
        if side == "left":
            self.left_indicator = indicator
            self.left_fill = fill
            self.left_percent = percent_label
        else:
            self.right_indicator = indicator
            self.right_fill = fill
            self.right_percent = percent_label
        
        return widget
    
    def create_case_widget(self):
        widget = QWidget()
        widget.setFixedSize(120, 150)
        layout = QVBoxLayout(widget)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.case_label = QLabel()
        self.case_label.setFixedSize(100, 100)
        self.case_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.load_image(self.case_label, "case.png", 100)
        layout.addWidget(self.case_label)
        
        self.case_indicator = QWidget()
        self.case_indicator.setFixedSize(70, 3)
        self.case_indicator.setStyleSheet("background-color: #e5e5ea; border-radius: 1.5px;")
        
        self.case_fill = QWidget(self.case_indicator)
        self.case_fill.setGeometry(0, 0, 0, 3)
        self.case_fill.setStyleSheet("background-color: #34c759; border-radius: 1.5px;")
        
        layout.addWidget(self.case_indicator, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.case_percent = QLabel("0%")
        self.case_percent.setStyleSheet("color: #8e8e93; font-size: 11px; font-weight: 500;")
        self.case_percent.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.case_percent)
        
        return widget
    
    def load_image(self, label, path, size):
        try:
            if os.path.exists(path):
                pixmap = QPixmap(path)
                if not pixmap.isNull():
                    scaled = pixmap.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
                    label.setPixmap(scaled)
                else:
                    label.setText("🎧")
                    label.setStyleSheet("font-size: 40px;")
            else:
                label.setText("🎧")
                label.setStyleSheet("font-size: 40px;")
        except:
            label.setText("🎧")
            label.setStyleSheet("font-size: 40px;")
    
    def update_battery_ui(self, left, right, case, case_charging, left_in_case, right_in_case, left_percent_change, right_percent_change):
        """Обновляет индикаторы"""
        
        # Левый наушник
        if left_in_case:
            # В кейсе = заряжается
            effect = QGraphicsOpacityEffect()
            effect.setOpacity(0.5)
            self.left_label.setGraphicsEffect(effect)
            # Синяя полоска при зарядке
            width = int(60 * left / 100)
            self.left_fill.setGeometry(0, 0, width, 3)
            self.left_fill.setStyleSheet("background-color: #007aff; border-radius: 1.5px;")
        else:
            # Вне кейса
            self.left_label.setGraphicsEffect(None)
            width = int(60 * left / 100)
            self.left_fill.setGeometry(0, 0, width, 3)
            self.update_indicator_color(self.left_fill, left)
        
        self.left_percent.setText(f"{left}%")
        
        # Правый наушник
        if right_in_case:
            effect = QGraphicsOpacityEffect()
            effect.setOpacity(0.5)
            self.right_label.setGraphicsEffect(effect)
            width = int(60 * right / 100)
            self.right_fill.setGeometry(0, 0, width, 3)
            self.right_fill.setStyleSheet("background-color: #007aff; border-radius: 1.5px;")
        else:
            self.right_label.setGraphicsEffect(None)
            width = int(60 * right / 100)
            self.right_fill.setGeometry(0, 0, width, 3)
            self.update_indicator_color(self.right_fill, right)
        
        self.right_percent.setText(f"{right}%")
        
        # Кейс
        width = int(70 * case / 100)
        self.case_fill.setGeometry(0, 0, width, 3)
        if case_charging:
            self.case_fill.setStyleSheet("background-color: #007aff; border-radius: 1.5px;")
        else:
            self.update_indicator_color(self.case_fill, case)
        self.case_percent.setText(f"{case}%")
        
        # Статус
        if left_in_case or right_in_case:
            self.status_label.setText("⚡ Charging")
            self.charging_info.setText("Earbuds in case")
        elif case_charging:
            self.status_label.setText("⚡ Case charging")
            self.charging_info.setText("USB-C connected")
        else:
            self.status_label.setText("Connected")
            self.charging_info.setText("")
    
    def update_indicator_color(self, fill, percent):
        if percent >= 100:
            fill.setStyleSheet("background-color: #e5ff00; border-radius: 1.5px;")
        elif percent >= 70:
            fill.setStyleSheet("background-color: #34c759; border-radius: 1.5px;")
        elif percent >= 30:
            fill.setStyleSheet("background-color: #ffcc00; border-radius: 1.5px;")
        else:
            fill.setStyleSheet("background-color: #ff3b30; border-radius: 1.5px;")
    
    def show_animation(self):
        self.show()
        
        screen = QApplication.primaryScreen()
        available = screen.availableGeometry()
        target_y = available.bottom() - self.height() - 15
        start_y = screen.geometry().bottom()
        
        self.move(available.center().x() - self.width() // 2, start_y)
        self.setWindowOpacity(0)
        
        self.move_anim = QPropertyAnimation(self, b"pos")
        self.move_anim.setDuration(400)
        self.move_anim.setStartValue(QPoint(self.x(), start_y))
        self.move_anim.setEndValue(QPoint(self.x(), target_y))
        self.move_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        self.opacity_anim = QPropertyAnimation(self, b"windowOpacity")
        self.opacity_anim.setDuration(300)
        self.opacity_anim.setStartValue(0)
        self.opacity_anim.setEndValue(1)
        
        self.move_anim.start()
        self.opacity_anim.start()
    
    def fade_out(self):
        self.fade_anim = QPropertyAnimation(self, b"windowOpacity")
        self.fade_anim.setDuration(300)
        self.fade_anim.setStartValue(self.windowOpacity())
        self.fade_anim.setEndValue(0)
        self.fade_anim.finished.connect(self.hide)
        self.fade_anim.start()


class DevWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.animation = JBLAnimation()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("JBL Wave Beam 2 - Battery Monitor")
        self.setFixedSize(400, 550)
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f7;
                font-family: -apple-system, BlinkMacSystemFont;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #e5e5ea;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QSlider {
                height: 20px;
            }
            QSlider::groove:horizontal {
                height: 4px;
                background: #e5e5ea;
                border-radius: 2px;
            }
            QSlider::handle:horizontal {
                background: #34c759;
                width: 16px;
                height: 16px;
                margin: -6px 0;
                border-radius: 8px;
            }
            QPushButton {
                background: #34c759;
                border: none;
                border-radius: 8px;
                color: white;
                font-weight: 600;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #2fb04f;
            }
            QCheckBox {
                spacing: 8px;
            }
            QLabel {
                color: #1c1c1e;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        title = QLabel("🎧 JBL Wave Beam 2")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #1c1c1e;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Левый наушник
        left_group = QGroupBox("Левый наушник")
        left_layout = QVBoxLayout()
        
        self.left_slider = QSlider(Qt.Orientation.Horizontal)
        self.left_slider.setRange(0, 100)
        self.left_slider.setValue(87)
        self.left_slider.valueChanged.connect(self.update_preview)
        left_layout.addWidget(QLabel("Заряд:"))
        left_layout.addWidget(self.left_slider)
        
        self.left_in_case = QCheckBox("В кейсе (заряжается)")
        self.left_in_case.setChecked(True)
        self.left_in_case.toggled.connect(self.update_preview)
        left_layout.addWidget(self.left_in_case)
        
        left_group.setLayout(left_layout)
        layout.addWidget(left_group)
        
        # Правый наушник
        right_group = QGroupBox("Правый наушник")
        right_layout = QVBoxLayout()
        
        self.right_slider = QSlider(Qt.Orientation.Horizontal)
        self.right_slider.setRange(0, 100)
        self.right_slider.setValue(87)
        self.right_slider.valueChanged.connect(self.update_preview)
        right_layout.addWidget(QLabel("Заряд:"))
        right_layout.addWidget(self.right_slider)
        
        self.right_in_case = QCheckBox("В кейсе (заряжается)")
        self.right_in_case.setChecked(True)
        self.right_in_case.toggled.connect(self.update_preview)
        right_layout.addWidget(self.right_in_case)
        
        right_group.setLayout(right_layout)
        layout.addWidget(right_group)
        
        # Кейс
        case_group = QGroupBox("Кейс")
        case_layout = QVBoxLayout()
        
        self.case_slider = QSlider(Qt.Orientation.Horizontal)
        self.case_slider.setRange(0, 100)
        self.case_slider.setValue(64)
        self.case_slider.valueChanged.connect(self.update_preview)
        case_layout.addWidget(QLabel("Заряд кейса:"))
        case_layout.addWidget(self.case_slider)
        
        self.case_charging = QCheckBox("Кейс на зарядке (USB-C)")
        self.case_charging.toggled.connect(self.update_preview)
        case_layout.addWidget(self.case_charging)
        
        case_group.setLayout(case_layout)
        layout.addWidget(case_group)
        
        # Управление
        control_group = QGroupBox("Управление")
        control_layout = QVBoxLayout()
        
        self.auto_close = QCheckBox("Автоматическое закрытие (5 сек)")
        self.auto_close.setChecked(True)
        control_layout.addWidget(self.auto_close)
        
        btn_show = QPushButton("▶ ПОКАЗАТЬ АНИМАЦИЮ")
        btn_show.clicked.connect(self.show_animation)
        btn_show.setStyleSheet("font-size: 16px; padding: 12px;")
        control_layout.addWidget(btn_show)
        
        btn_close = QPushButton("✕ Закрыть окно")
        btn_close.clicked.connect(self.close_animation)
        control_layout.addWidget(btn_close)
        
        control_group.setLayout(control_layout)
        layout.addWidget(control_group)
        
        info = QLabel("💡 Наушники в кейсе автоматически заряжаются\nКейс на USB-C заряжается от розетки")
        info.setStyleSheet("color: #8e8e93; font-size: 11px;")
        info.setWordWrap(True)
        layout.addWidget(info)
        
        layout.addStretch()
        self.setLayout(layout)
        
        self.update_preview()
    
    def update_preview(self):
        left = self.left_slider.value()
        right = self.right_slider.value()
        case = self.case_slider.value()
        
        case_charging = self.case_charging.isChecked()
        left_in_case = self.left_in_case.isChecked()
        right_in_case = self.right_in_case.isChecked()
        
        # Для демо - имитируем изменение процентов при зарядке
        left_percent_change = 0
        right_percent_change = 0
        
        self.animation.update_battery_signal.emit(
            left, right, case, case_charging,
            left_in_case, right_in_case,
            left_percent_change, right_percent_change
        )
    
    def show_animation(self):
        self.update_preview()
        self.animation.show_animation()
        
        if self.auto_close.isChecked():
            QTimer.singleShot(5000, self.animation.fade_out)
    
    def close_animation(self):
        self.animation.fade_out()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DevWindow()
    window.show()
    sys.exit(app.exec())
