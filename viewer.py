from OCC.Display.backend import load_backend
load_backend('pyqt5')

from OCC.Display.qtDisplay import qtViewer3d
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from OCC.Core.Quantity import Quantity_NOC_GRAY, Quantity_NOC_LIGHTSTEELBLUE

class OCCViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.display = qtViewer3d(self)
        # الوصول إلى الكائن الداخلي للعرض
        viewer = self.display._display.Viewer
        view = self.display._display.View

        # عرض الشبكة
        viewer.DisplayGrid()

        # تصغير المحاور الثلاثية
        viewer.SetTrihedronSize(0.05)

        # تغيير لون الشبكة والمحاور
        from OCC.Core.Quantity import Quantity_NOC_GRAY, Quantity_NOC_LIGHTSTEELBLUE
        viewer.SetGridColor(Quantity_NOC_GRAY)
        viewer.SetTrihedronColor(Quantity_NOC_LIGHTSTEELBLUE)

        # إعادة رسم العرض
        view.MustBeResized()
        view.Redraw()

        # ✅ عرض الشبكة
        self.display.Viewer.DisplayGrid()

        # ✅ تصغير المحاور الثلاثية
        self.display.Viewer.SetTrihedronSize(0.05)

        # ✅ تغيير لون الشبكة والمحاور
        self.display.Viewer.SetGridColor(Quantity_NOC_GRAY)
        self.display.Viewer.SetTrihedronColor(Quantity_NOC_LIGHTSTEELBLUE)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.display)
        self.setLayout(layout)