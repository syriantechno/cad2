TOPBAR_STYLE = """
QTabWidget::pane {
    border: 0;
    background: #E0E0E0;
}

QTabBar::tab {
    background: transparent;
    color: #000000;
    padding: 5px 10px;
    margin: 0px;
    border-radius: 0px;
    font-size: 14px;
    min-width: 60px;
    min-height: 40px;
}

QTabBar::tab:selected {
    border-bottom: 3px solid #3A84FF;
    background-color: transparent;
    color: #000000;
}

QTabBar::tab:hover {
    background-color: transparent;
}

QToolButton {
    background-color: transparent;
    color: #000000;
    border: none;
    border-bottom: 3px solid transparent; /* خط أسفل الشفافة افتراضيًا */
    padding: 4px;
    margin: 2px;
    font-size: 12px;
    min-height: 40px;
    min-width: 44px;
}

QToolButton:hover, QToolButton:pressed {
    background-color: transparent; /* إزالة أي تأثير هوفر أو ضغط */
}

QToolButton:checked {
    border-bottom: 3px solid #3A84FF; /* خط أزرق عند التحديد */
}

QWidget {
    background-color: #F5F5F5;
}
"""
DOCK_STYLE = """
QDockWidget {
    background-color: #E0E0E0;
    titlebar-close-icon: url(frontend/icons/close.png);
    titlebar-normal-icon: url(frontend/icons/float.png);
    font-size: 14px;
    font-weight: bold;
}

QWidget {
    background-color: #F5F5F5;
}

QLabel {
    font-size: 12px;
}

QComboBox, QDoubleSpinBox, QPushButton {
    background-color: #FFFFFF;
    border: 1px solid #C0C0C0;
    border-radius: 4px;
    padding: 4px;
    font-size: 12px;
}

QPushButton {
    background-color: #3A84FF;
    color: #FFFFFF;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #346BCC;
}
"""
EXTRUDE_WINDOW_STYLE = """
QWidget#container {
    background-color: #F3F3F3;
    border-radius: 10px;
}

QComboBox, QDoubleSpinBox {
    background-color: #FFFFFF;
    border: 1px solid #C0C0C0;
    border-radius: 5px;
    padding: 6px;
    font-size: 14px;
    min-height: 22px;
    min-width: 140px;
}

QComboBox::drop-down {
    width: 25px;
}

QPushButton#applyBtn {
    background-color: #0078D4;
    color: white;
    font-size: 14px;
    font-weight: bold;
    padding: 6px;
    border-radius: 5px;
    min-height: 22px;
}
QPushButton#applyBtn:hover {
    background-color: #005a9e;
}

QPushButton#cancelBtn {
    background-color: #E0E0E0;
    color: #333;
    font-size: 13px;
    border-radius: 5px;
    padding: 5px;
    min-height: 25px;
}
QPushButton#cancelBtn:hover {
    background-color: #C8C8C8;
}
"""

