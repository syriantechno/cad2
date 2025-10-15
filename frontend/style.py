TOPBAR_STYLE = """
QTabWidget::pane {
    border: 0;
    background: #EAEAEA;
}

QTabBar::tab {
    background: #EAEAEA;
    color: #000000;
    padding: 0px 5px;
    margin: 0px;
    border-radius: 0px;
    font-size: 13px;
    min-width: 60px;
    min-height: 32px;
}

QTabBar::tab:selected {
    border-bottom: 2px solid #3A84FF;
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
    border-bottom: 2px solid transparent;
    padding: 0px;
    margin: 0px;
    font-size: 12px;
    min-height: 48px;
    min-width: 64px;
    qproperty-iconSize: 36px;
}

QToolButton:hover, QToolButton:pressed {
    background-color: transparent;
}

QToolButton:checked {
    border-bottom: 2px solid #3A84FF;
}

QWidget {
    background-color: #EAEAEA;
}
"""
DOCK_STYLE = """
QDockWidget {
    background-color: #EAEAEA;
    titlebar-close-icon: url(frontend/icons/close.png);
    titlebar-normal-icon: url(frontend/icons/float.png);
    font-size: 14px;
    font-weight: bold;
}

QWidget {
    background-color: #EAEAEA;
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

