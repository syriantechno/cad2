from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QComboBox, QDoubleSpinBox,
    QPushButton, QLineEdit, QFormLayout, QWidget,
    QStackedWidget, QLabel, QHBoxLayout, QFrame, QFileDialog, QMessageBox,
    QScrollArea, QGridLayout
)

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QPoint

from dxf_tools import  load_dxf_file
from pathlib import Path
import shutil
from tools.database import ProfileDB
import json, os
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QSpinBox, QDoubleSpinBox, QLineEdit, QComboBox, QLabel, QPushButton, QFormLayout
try:
    from OCC.Display.qtDisplay import qtViewer3d
except Exception:
    qtViewer3d = None  # يسمح بتحميل الملف حتى بدون بيئة OCC أثناء التطوير


class DraggableDialog(QDialog):
    """نافذة عائمة قابلة للسحب بدون شريط عنوان"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_dragging = False
        self._drag_pos = QPoint()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._is_dragging = True
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._is_dragging:
            self.move(event.globalPos() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._is_dragging = False




def create_tool_window(parent):
    """
    نافذة عائمة متعددة الصفحات (Extrude / Profile / Manager)
    تعيد: dialog, show_page
    """

    import json, os

    def load_tool_types():
        try:
            with open("data/tool_types.json", "r") as f:
                return json.load(f)
        except Exception as e:
            print("Failed to load tool types:", e)
            return {}

    tool_types = load_tool_types()

    def open_add_type_dialog():
        dialog = AddToolTypeDialog(tool_types, parent)
        if dialog.exec_():  # إذا المستخدم ضغط "Save" داخل النافذة
            # تحديث القائمة بعد الإضافة
            type_combo.clear()
            type_combo.addItems(tool_types.keys())
            type_combo.setCurrentText(dialog.name_input.text())
            update_tool_image(dialog.name_input.text())

    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QPixmap

    dialog = DraggableDialog(parent)
    dialog.setObjectName("ToolFloatingWindow")
    dialog.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    dialog.setFixedWidth(360)

    dialog.setStyleSheet("""
        QDialog#ToolFloatingWindow {
            background-color: #f2f2f2;
            border: 1px solid #b4b4b4;
            border-radius: 8px;
        }
        QLabel {
            font-size: 13px;
            color: #333;
        }
        QComboBox, QDoubleSpinBox, QLineEdit {
            min-height: 28px;
            font-size: 13px;
            border: 1px solid #ccc;
            border-radius: 4px;
            background: white;
        }
        QComboBox:focus, QDoubleSpinBox:focus, QLineEdit:focus {
            border: 1px solid #0078d4;
        }
        QPushButton {
            min-height: 30px;
            min-width: 100px;
            font-size: 13px;
            border-radius: 4px;
        }
        QPushButton#ApplyBtn {
            background-color: #0078d4;
            color: white;
        }
        QPushButton#ApplyBtn:hover { background-color: #005ea2; }
        QPushButton#CancelBtn {
            background-color: #e0e0e0;
            color: black;
        }
        QPushButton#CancelBtn:hover { background-color: #cacaca; }
        QFrame#line { background:#dcdcdc; height:1px; }
    """)

    # ====== Layout ======
    main_layout = QVBoxLayout(dialog)
    main_layout.setContentsMargins(10, 10, 10, 10)
    main_layout.setSpacing(8)

    # ====== Header ======
    header = QLabel("Tool Options")
    header.setStyleSheet("font-size: 14px; font-weight: bold; margin-bottom: 4px;")
    main_layout.addWidget(header)

    line = QFrame()
    line.setObjectName("line")
    line.setFrameShape(QFrame.HLine)
    line.setFrameShadow(QFrame.Sunken)
    main_layout.addWidget(line)

    # ====== Stack ======
    stacked = QStackedWidget(dialog)
    main_layout.addWidget(stacked)

    # ==================== Extrude Page ====================
    extrude_page = QWidget()
    extrude_layout = QFormLayout(extrude_page)
    extrude_layout.setLabelAlignment(Qt.AlignLeft)
    extrude_layout.setFormAlignment(Qt.AlignTop)

    axis_combo = QComboBox()
    axis_combo.addItems(["X", "Y", "Z"])
    distance_spin = QDoubleSpinBox()
    distance_spin.setRange(1, 9999)
    distance_spin.setValue(100)

    extrude_layout.addRow("Axis:", axis_combo)
    extrude_layout.addRow("Distance (mm):", distance_spin)
    stacked.addWidget(extrude_page)

    # ==================== Profile Page ====================
    profile_page = QWidget()
    pform = QFormLayout(profile_page)
    pform.setLabelAlignment(Qt.AlignLeft)
    pform.setFormAlignment(Qt.AlignTop)
    pform.setHorizontalSpacing(12)
    pform.setVerticalSpacing(8)

    p_name = QLineEdit()
    p_code = QLineEdit()
    p_dims = QLineEdit()
    p_notes = QLineEdit()

    dxf_path_edit = QLineEdit()
    dxf_path_edit.setReadOnly(True)
    choose_btn = QPushButton("Choose DXF")

    # عارض صغير للمعاينة
    # عارض مصغر للمعاينة (بحجم واضح وثابت)
    if qtViewer3d is not None:
        preview_container = QWidget()
        preview_container.setMinimumHeight(250)  # 👈 ارتفاع مناسب
        preview_container.setMaximumHeight(300)  # 👈 لا يزيد عن هذا
        preview_layout = QVBoxLayout(preview_container)
        preview_layout.setContentsMargins(0, 6, 0, 6)
        viewer = qtViewer3d(preview_container)
        viewer.setMinimumSize(320, 240)  # 👈 حجم أولي واضح
        preview_layout.addWidget(viewer)
        small_display = viewer._display  # سنستخدمه للحفظ كصورة أيضًا
        from PyQt5.QtCore import QTimer
        from tools.viewer_utils import setup_viewer_colors

        # تأخير تهيئة مظهر العارض المصغّر
        QTimer.singleShot(100, lambda: setup_viewer_colors(small_display))

        # ===== إعدادات مظهر العارض المصغر (Preview) =====
        # إعداد خلفية العارض الرئيسي وحدود الرسم
        from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
        from OCC.Core.Prs3d import Prs3d_LineAspect
        from OCC.Core.Aspect import Aspect_TOL_SOLID

        def setup_viewer_colors(display):
            """يضبط خلفية بيضاء وحدود سوداء لأي عارض OCC."""
            white = Quantity_Color(1.0, 1.0, 1.0, Quantity_TOC_RGB)
            black = Quantity_Color(0.0, 0.0, 0.0, Quantity_TOC_RGB)

            # خلفية بيضاء
            view = display.View
            view.SetBgGradientColors(white, white, True)
            view.SetBgGradientStyle(0)
            view.MustBeResized()

            # تفعيل رسم الحدود باللون الأسود
            drawer = display.Context.DefaultDrawer()
            drawer.SetFaceBoundaryDraw(True)
            line_aspect = Prs3d_LineAspect(black, Aspect_TOL_SOLID, 1.0)
            drawer.SetFaceBoundaryAspect(line_aspect)

            # إعادة تحديث العارض
            display.Context.UpdateCurrentViewer()
            view.Redraw()

        setup_viewer_colors(small_display)




    else:
        preview_container = QLabel("OCC Preview not available in this environment.")
        small_display = None



    pform.addRow("Name:", p_name)
    pform.addRow("Code:", p_code)
    pform.addRow("Dimensions:", p_dims)
    pform.addRow("Notes:", p_notes)
    pform.addRow("DXF File:", dxf_path_edit)
    pform.addRow("", choose_btn)
    pform.addRow(QLabel("Preview:"), preview_container)

    stacked.addWidget(profile_page)

    # ==================== Profiles Manager Page (NEW LAYOUT) ====================
    from PyQt5.QtWidgets import QListWidget, QListWidgetItem

    manager_page = QWidget()
    manager_layout = QHBoxLayout(manager_page)
    manager_layout.setContentsMargins(8, 8, 8, 8)
    manager_layout.setSpacing(12)




    # ===== Left: Names list =====
    profile_list = QListWidget()
    profile_list.setMinimumWidth(120)
    manager_layout.addWidget(profile_list, 1)

    # ===== Right: Details panel =====
    detail_panel = QVBoxLayout()
    detail_panel.setSpacing(6)
    manager_layout.addLayout(detail_panel, 2)



    preview_label = QLabel()
    preview_label.setFixedSize(200, 200)
    preview_label.setAlignment(Qt.AlignCenter)
    preview_label.setStyleSheet("border: 1px solid #ccc; background: #fafafa;")
    detail_panel.addWidget(preview_label)

    info_label = QLabel()
    info_label.setWordWrap(True)
    info_label.setText("<i>Select a profile to view details.</i>")
    detail_panel.addWidget(info_label)

    ok_button = QPushButton("OK / Load")
    ok_button.setEnabled(False)
    detail_panel.addWidget(ok_button)

    stacked.addWidget(manager_page)

    # ==================== Tools Manager Page ====================

    tools_page = QWidget()
    tools_layout = QVBoxLayout(tools_page)

    header_label = QLabel("🛠 Tool Manager")
    header_label.setStyleSheet("font-weight: bold; font-size: 14px;")
    tools_layout.addWidget(header_label)

    form_layout = QFormLayout()

    name_input = QLineEdit()
    diameter_input = QDoubleSpinBox();
    diameter_input.setSuffix(" mm");
    diameter_input.setMaximum(100)
    length_input = QDoubleSpinBox();
    length_input.setSuffix(" mm");
    length_input.setMaximum(200)
    type_combo = QComboBox()
    type_combo.setEditable(True)
    type_combo.addItems(tool_types.keys())

    add_type_btn = QPushButton("➕")
    add_type_btn.setFixedWidth(30)

    type_row = QHBoxLayout()
    type_row.addWidget(type_combo)
    type_row.addWidget(add_type_btn)

    form_layout.addRow("Type:", type_row)

    rpm_input = QSpinBox();
    rpm_input.setMaximum(40000)
    steps_input = QSpinBox();
    steps_input.setMaximum(100)

    image_label = QLabel("No image");
    image_label.setFixedSize(120, 120);
    image_label.setAlignment(Qt.AlignCenter)
    image_label.setStyleSheet("border: 1px solid gray;")

    form_layout.addRow("Tool Name:", name_input)
    form_layout.addRow("Diameter:", diameter_input)
    form_layout.addRow("Length:", length_input)
    form_layout.addRow("Type:", type_combo)
    form_layout.addRow("Default RPM:", rpm_input)
    form_layout.addRow("Default Steps:", steps_input)
    form_layout.addRow("Preview:", image_label)

    tools_layout.addLayout(form_layout)

    save_button = QPushButton("💾 Save Tool")
    tools_layout.addWidget(save_button)

    stacked.addWidget(tools_page)

    # ====== Bottom Buttons ======
    bottom_layout = QHBoxLayout()
    bottom_layout.addStretch()
    cancel_btn = QPushButton("Cancel");  cancel_btn.setObjectName("CancelBtn")
    apply_btn = QPushButton("Apply");    apply_btn.setObjectName("ApplyBtn")
    bottom_layout.addWidget(cancel_btn)
    bottom_layout.addWidget(apply_btn)
    main_layout.addLayout(bottom_layout)

    cancel_btn.clicked.connect(dialog.hide)

    # ====== DB ======
    db = ProfileDB()

    # ====== Handlers ======
    selected_shape = {"shape": None, "src": None}

    def on_choose_dxf():
        file_name, _ = QFileDialog.getOpenFileName(dialog, "Select DXF", "", "DXF Files (*.dxf)")
        if not file_name:
            return
        dxf_path_edit.setText(file_name)
        # حلّل DXF واعرضه في العارض المصغّر
        try:
            from dxf_tools import load_dxf_file
            shp = load_dxf_file(file_name)
        except Exception as ex:
            QMessageBox.warning(dialog, "DXF", f"Failed to import dxf_tools:\n{ex}")
            return
        if shp is None:
            QMessageBox.warning(dialog, "DXF", "Failed to parse DXF file.")
            return
        selected_shape["shape"] = shp
        selected_shape["src"] = file_name
        try:
            if small_display is not None:
                small_display.EraseAll()
                small_display.DisplayShape(shp, update=True)
                small_display.FitAll()
        except Exception as e:
            QMessageBox.warning(dialog, "Preview", f"Failed to display preview:\n{e}")

    choose_btn.clicked.connect(on_choose_dxf)

    # ---------- Profiles Manager helpers ----------
    from PyQt5.QtWidgets import QListWidgetItem
    from PyQt5.QtCore import Qt

    def refresh_profiles_list():
        print("🟡 refresh_profiles_list() called")

        try:
            profiles = db.list_profiles()
            print("DEBUG profiles =", profiles)

            profile_list.clear()

            if not profiles:
                profile_list.addItem("⚠️ لا توجد بروفايلات محفوظة")
                profile_list.setEnabled(False)
                return

            profile_list.setEnabled(True)

            for row in profiles:
                try:
                    if len(row) < 9:
                        print(f"⚠️ Skipping invalid row: {row}")
                        continue

                    pid, name, code, dims, notes, dxf_path, brep_path, img_path, created = row

                    item = QListWidgetItem(name)
                    item.setData(Qt.UserRole, {
                        "name": name,
                        "dxf_path": dxf_path or ""
                    })
                    profile_list.addItem(item)

                except Exception as inner_e:
                    print(f"❌ Error while adding profile row: {inner_e}")

            print("✅ profile_list count:", profile_list.count())

        except Exception as e:
            print(f"❌ refresh_profiles_list() failed: {e}")

    from pathlib import Path
    from PyQt5.QtGui import QPixmap
    from PyQt5.QtCore import Qt

    def on_profile_selected():
        current_row = profile_list.currentRow()
        if current_row < 0 or current_row >= len(profiles):
            print("⚠️ Invalid profile selection")
            return

        data = profiles[current_row]
        print(f"✅ Selected profile: {data}")

        # --- عرض الصورة ---
        img_path = data[7]
        if img_path and img_path.lower() != "none" and Path(img_path).exists():
            pixmap = QPixmap(img_path)
            profile_image_label.setPixmap(
                pixmap.scaled(
                    profile_image_label.width(),
                    profile_image_label.height(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )
        else:
            profile_image_label.clear()
            print(f"⚠️ No valid image for: {data[1]}")

        # --- عرض النصوص ---
        name_label.setText(f"Name: {data[1]}")
        code_label.setText(f"Code: {data[2]}")
        size_label.setText(f"Size: {data[3]}")
        desc_label.setText(f"Desc: {data[4]}")

    profile_list.currentItemChanged.connect(lambda current, prev: on_profile_selected())

    # ================== زر Apply ==================
    def handle_apply():
        current_page = stacked.currentIndex()

        # 0️⃣ Extrude page → استدعاء دالة الواجهة الرئيسية
        if current_page == 0:
            try:
                parent.extrude_clicked_from_window()

                # 🟢 بعد تنفيذ عملية Extrude، نضيفها إلى اللوحة
                profile_name = getattr(parent, "active_profile_name", None)
                distance_val = getattr(parent, "last_extrude_distance", None)
                if profile_name and distance_val and hasattr(parent, "op_browser"):
                    parent.op_browser.add_extrude(profile_name, distance_val)

                dialog.hide()
            except Exception as e:
                QMessageBox.critical(dialog, "Extrude Error", str(e))
            return

        # 1️⃣ Profile page → حفظ البروفايل في القاعدة وإنشاء الأصول
        elif current_page == 1:
            name = p_name.text().strip()
            if not name:
                QMessageBox.information(dialog, "Profile", "Please enter profile Name.")
                return
            if not dxf_path_edit.text():
                QMessageBox.information(dialog, "Profile", "Please choose a DXF file.")
                return
            try:
                # تحميل الشكل
                shape = load_dxf_file(dxf_path_edit.text())
                if shape is None or shape.IsNull():
                    raise RuntimeError("Invalid DXF shape.")

                # عرض الشكل على العارض الصغير
                if small_display is not None:
                    small_display.EraseAll()
                    small_display.DisplayShape(shape, update=True)
                    small_display.FitAll()

                # إعداد المسارات
                profile_dir = Path("profiles") / name
                profile_dir.mkdir(parents=True, exist_ok=True)
                dxf_dst = profile_dir / f"{name}.dxf"
                img_path = profile_dir / f"{name}.png"

                # أخذ صورة من العارض
                from tools.profile_tools import _dump_display_png
                _dump_display_png(small_display, shape, img_path)

                # نسخ ملف DXF كما هو
                shutil.copy2(dxf_path_edit.text(), dxf_dst)

                # حفظ في قاعدة البيانات
                db.add_profile(
                    name=name,
                    code=p_code.text().strip(),
                    dimensions=p_dims.text().strip(),
                    notes=p_notes.text().strip(),
                    dxf_path=str(dxf_dst),
                    brep_path="",
                    image_path=str(img_path)
                )

                QMessageBox.information(dialog, "Saved", "Profile saved successfully.")

                # 🟡 بعد الحفظ، أضف البروفايل إلى اللوحة
                if hasattr(parent, "op_browser"):
                    parent.op_browser.add_profile(name)

                dialog.hide()
            except Exception as e:
                QMessageBox.critical(dialog, "Error", f"Failed to save profile:\n{e}")
                return

    def on_ok_clicked():
        item = profile_list.currentItem()
        if not item:
            print("⚠️ No profile selected.")
            return

        data = item.data(Qt.UserRole)
        if not data:
            print("⚠️ No data for selected item.")
            return

        dxf_path = data.get("dxf_path")
        name = data.get("name", "Unknown")

        if not dxf_path or not Path(dxf_path).exists():
            QMessageBox.warning(dialog, "Load Error", f"DXF file not found:\n{dxf_path}")
            return

        print(f"🟡 Loading profile: {name} from {dxf_path}")

        try:
            shape = load_dxf_file(Path(dxf_path))
            if shape is None or shape.IsNull():
                raise RuntimeError("❌ DXF parsing returned no shape.")

            main_window = dialog.parent()
            if not hasattr(main_window, "display") or main_window.display is None:
                raise RuntimeError("❌ Main display not initialized.")

            main_window.display.EraseAll()
            main_window.display.DisplayShape(shape, update=True)
            main_window.loaded_shape = shape
            main_window.display.FitAll()

            if hasattr(main_window, "op_browser"):
                main_window.op_browser.add_profile(name)

            print(f"🟢 Loaded successfully → {name}")
            dialog.hide()

        except Exception as e:
            print(f"❌ Error while loading: {e}")
            QMessageBox.critical(dialog, "Load Error", str(e))


    ok_button.clicked.connect(on_ok_clicked)

    apply_btn.clicked.connect(handle_apply)

    def show_page(index: int):
        stacked.setCurrentIndex(index)
        if index == 2:
            QTimer.singleShot(50, refresh_profiles_list)  # ← تأخير بسيط يضمن أن الـ UI جاهز
            header.setText("Profiles Manager")
        elif index == 1:
            header.setText("Profile")
        elif index == 3:
            header.setText("Tools Manager")
        else:
            header.setText("Extrude")
        dialog.show()
        dialog.raise_()

    class AddToolTypeDialog(QDialog):
        def __init__(self, tool_types, parent=None):
            super().__init__(parent)
            self.setWindowTitle("Add New Tool Type")
            self.setFixedSize(300, 250)
            self.tool_types = tool_types
            self.image_path = ""

            layout = QVBoxLayout(self)

            self.name_input = QLineEdit()
            self.name_input.setPlaceholderText("Tool type name")
            layout.addWidget(self.name_input)

            self.image_label = QLabel("No image")
            self.image_label.setFixedSize(120, 120)
            self.image_label.setAlignment(Qt.AlignCenter)
            self.image_label.setStyleSheet("border: 1px solid gray;")
            layout.addWidget(self.image_label)

            choose_btn = QPushButton("Choose Image")
            choose_btn.clicked.connect(self.choose_image)
            layout.addWidget(choose_btn)

            save_btn = QPushButton("Save Type")
            save_btn.clicked.connect(self.save_type)
            layout.addWidget(save_btn)

        def choose_image(self):
            base_dir = os.path.dirname(__file__)
            image_dir = os.path.join(base_dir, "..", "images")
            path, _ = QFileDialog.getOpenFileName(self, "Choose image", image_dir)
            if path:
                self.image_path = os.path.relpath(path, os.path.join(base_dir, ".."))
                pixmap = QPixmap(path).scaled(120, 120, Qt.KeepAspectRatio)
                self.image_label.setPixmap(pixmap)

        def save_type(self):
            name = self.name_input.text().strip()
            if name and self.image_path:
                self.tool_types[name] = self.image_path
                with open("data/tool_types.json", "w") as f:
                    json.dump(self.tool_types, f, indent=2)
                self.accept()

    return dialog, show_page