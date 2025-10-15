import sys
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QDialog, QHBoxLayout, QVBoxLayout,
    QListWidget, QListWidgetItem, QLabel, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

# ============ دالة وهمية لتحميل DXF ============
# في مشروعك الحقيقي تستبدلها بـ from dxf_tools import load_dxf_file
def load_dxf_file(path):
    print(f"[MOCK] Loading DXF from: {path}")
    return True  # ترجع شكل افتراضي

# ============ قاعدة بيانات وهمية (للتجربة فقط) ============
# في مشروعك الحقيقي استبدلها بـ ProfileDB().list_profiles()
def get_mock_profiles():
    return [
        (1, "Door Frame", "DF-100", "100x50", "Main entrance", "samples/door.dxf", "", "samples/door.png", "2025-10-15"),
        (2, "Window Frame", "WF-200", "80x40", "Second floor", "samples/window.dxf", "", "samples/window.png", "2025-10-15"),
        (3, "Simple Profile", "SP-001", "50x50", "Test shape", "samples/simple.dxf", "", "", "2025-10-15"),
    ]

# ============ نافذة Profile Manager الجديدة ============
class ProfileManagerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Profile Manager (New)")
        self.setFixedSize(700, 500)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(10)

        # ----- القائمة -----
        self.profile_list = QListWidget()
        self.profile_list.setFixedWidth(220)
        self.profile_list.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.profile_list)

        # ----- التفاصيل -----
        right_layout = QVBoxLayout()
        right_layout.setSpacing(8)

        self.pm_image = QLabel("No Image")
        self.pm_image.setFixedSize(400, 250)
        self.pm_image.setAlignment(Qt.AlignCenter)
        self.pm_image.setStyleSheet("border: 1px solid gray; background: white;")
        right_layout.addWidget(self.pm_image)

        self.pm_info = QLabel("Select a profile to view details.")
        self.pm_info.setWordWrap(True)
        self.pm_info.setStyleSheet("font-size: 14px;")
        right_layout.addWidget(self.pm_info)

        self.pm_ok = QPushButton("✅ OK")
        self.pm_ok.setFixedWidth(120)
        right_layout.addWidget(self.pm_ok, 0, Qt.AlignLeft)

        layout.addLayout(right_layout)

        # ----- ربط الأحداث -----
        self.profile_list.currentItemChanged.connect(self.show_profile_details)
        self.pm_ok.clicked.connect(self.apply_selected_profile)

        # تحميل البيانات الوهمية
        self.load_profiles()

    # ----------------------------
    def load_profiles(self):
        """تحميل البروفايلات من القاعدة"""
        self.profile_list.clear()
        profiles = get_mock_profiles()
        for row in profiles:
            pid, name, code, dims, notes, dxf_path, brep_path, img_path, created = row
            item = QListWidgetItem(name or f"#{pid}")
            item.setData(Qt.UserRole, {
                "id": pid,
                "name": name,
                "code": code,
                "dims": dims,
                "notes": notes,
                "dxf_path": dxf_path,
                "img_path": img_path,
                "created": created
            })
            self.profile_list.addItem(item)

    # ----------------------------
    def show_profile_details(self, item):
        if not item:
            self.pm_image.setText("No Image")
            self.pm_info.setText("Select a profile to view details.")
            return

        data = item.data(Qt.UserRole)
        img_path = data.get("img_path")
        if img_path and Path(img_path).exists():
            pix = QPixmap(img_path)
            self.pm_image.setPixmap(
                pix.scaled(self.pm_image.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
        else:
            self.pm_image.clear()
            self.pm_image.setText("No Image")

        self.pm_info.setText(
            f"<b>Name:</b> {data['name']}<br>"
            f"<b>Code:</b> {data['code']}<br>"
            f"<b>Dimensions:</b> {data['dims']}<br>"
            f"<b>Notes:</b> {data['notes']}<br>"
            f"<b>DXF:</b> {data['dxf_path']}"
        )

    # ----------------------------
    def apply_selected_profile(self):
        item = self.profile_list.currentItem()
        if not item:
            QMessageBox.warning(self, "Select", "Please select a profile.")
            return

        data = item.data(Qt.UserRole)
        dxf_path = data.get("dxf_path")
        if not dxf_path or not Path(dxf_path).exists():
            QMessageBox.critical(self, "DXF", f"DXF file not found:\n{dxf_path}")
            return

        # تحميل DXF وعرضه (في حالتك الحقيقية سيكون في العارض الرئيسي)
        ok = load_dxf_file(dxf_path)
        if ok:
            print(f"[✅] Loaded profile from: {dxf_path}")
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "Failed to load DXF.")

# ============ التشغيل المستقل ============
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = ProfileManagerDialog()
    dlg.exec_()
