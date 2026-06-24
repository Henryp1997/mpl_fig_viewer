"""
mpl_fig_viewer.py

Mini app for viewing .eplot interactive matplotlib figure files

    - Author: HP, 2026
"""
import os
import sys
import ctypes
import pickle
from pathlib import Path

if getattr(sys, "frozen", False):
    os.environ["MATPLOTLIBDATA"] = os.path.join(
        os.path.dirname(sys.executable),
        "mpl-data",
    )

import matplotlib
matplotlib.use("QtAgg")
import matplotlib.text as mtext
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QGridLayout, QFrame, QFileDialog
)
from PySide6.QtGui import QIcon, Qt

if getattr(sys, "frozen", False):
    BASE = Path(sys.executable).resolve().parent
else:
    BASE = Path(__file__).parent

from custom_button import CustomButton
from palette import set_light_palette


class FigureViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Matplotlib interactive figure viewer")
        self.setWindowIcon(QIcon(str(BASE / "assets" / "plot_icon.ico")))
        self.dpi = self.window().screen().devicePixelRatio()

        # Font sizes
        self.fsizes = {i: int(i / self.dpi) for i in range(4, 17)}
        
        # Create main widget and layout
        main_widget = QWidget()
        self.main_layout = QGridLayout()

        # Create browse for files button
        self.browse_btn = CustomButton(
            "Browse for .eplot file...", self.fsizes[15], self.fsizes[6], "black", 1, "#666666", 3, "#C7C6FB", "black", "white"
        )
        self.browse_btn.clicked.connect(self._loadFigureFromFile)
        self.browse_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Add widgets to layout and resize
        self.main_layout.addWidget(self.browse_btn, 0, 0, alignment=Qt.AlignLeft)
        self.main_layout.setColumnStretch(0, 0) # Fixed button size
        main_widget.setLayout(self.main_layout)

        # Load blank figure if opened app directly, otherwise open clicked file
        # This also adds self.canv_frame and self.toolbar to the main layout
        file = BASE / "assets" / "blank.eplot"
        self.blank_file = file
        if len(sys.argv) > 1:
            file = sys.argv[1]
        self._loadFigureFromFile(None, file=file)

        self.setCentralWidget(main_widget)

    
    def _loadFigureFromFile(self, _, file=None):
        """
        Load pickled file of format .eplot or .pkl (legacy).
        TODO: move towards .eplot created via JSON instead of pickling
        """
        if file is None:
            file = QFileDialog.getOpenFileName(
                self, "Select .eplot or .pickle file", dir=r"C:\\", filter="Python figure (*.eplot *.pkl)"
            )[0]
            if not file or not Path(file).exists():
                return

        with open(file, "rb") as f:
            fig = pickle.load(f)
    
        # Fig may be saved with old matplotlib version and has missing attrs
        fig = self._patchFig(fig)

        # Remove old canvas widget
        if hasattr(self, "canvas"):
            old_canv = self.canvas
            self.canv_frame.layout().removeWidget(old_canv)
            old_canv.setParent(None)
            old_canv.deleteLater()
        else:
            self.canv_frame = QFrame()
            self.canv_frame.setLayout(QGridLayout())
            margin = 10 / self.dpi
            self.canv_frame.layout().setContentsMargins(margin, margin, margin, margin)
            self.background_colour = "white"
            self.canv_frame.setStyleSheet(
                f"""border-radius: {self.fsizes[4]}px; border: 1px solid #666666; background-color: {self.background_colour}"""
            )

        # Swap figure and create new canvas
        self.figure = fig
        self.canvas = FigureCanvas(self.figure)
        self.canv_frame.layout().addWidget(self.canvas)

        # Re-map existing toolbar to current canvas
        if hasattr(self, "toolbar"):
            self.toolbar.setParent(None)
            self.toolbar.deleteLater()
        self._createToolbar()
    
        # Add widgets to layout
        self.main_layout.addWidget(self.canv_frame, 1, 0)
        self.main_layout.addWidget(self.toolbar, 2, 0)

        # Resize layout
        w, h = self._getFigureSize(self.figure)
        self.resize(w, h)

        # Redraw canvas
        self.canvas.draw_idle()

        # Set window title to filename
        if file != self.blank_file:
            self.setWindowTitle(file)


    def _createToolbar(self):
        self.toolbar = NavigationToolbar(self.canvas, parent=self)
        self.toolbar.setMovable(False)
        self.toolbar.setStyleSheet(
            f"""
            QToolBar {{
                border-radius: {self.fsizes[4]}px;
                border: 1px solid #666666;
                background-color: {self.background_colour};
                padding: {self.fsizes[8]}px
            }}
            QToolbar > QWidget {{
                background: transparent;
                border: none
            }}
            """
        )


    def _getFigureSize(self, figure):
        fig_size = figure.get_size_inches()
        fig_dpi = figure.dpi
        width_px = fig_size[0] * fig_dpi
        height_px = fig_size[1] * fig_dpi
        return width_px, height_px


    def _patchFig(self, fig):
        """ Patch a figure saved in an older matplotlib version """
        for ax in fig._axstack.as_list():
            if not hasattr(ax, "_axis_names"):
                ax._axis_names = ("x", "y")

            if not hasattr(ax, "_axis_map"):
                ax._axis_map = {
                    "x": ax.xaxis,
                    "y": ax.yaxis,
                }

        # Patch all Text objects
        for obj in fig.findobj():
            if isinstance(obj, mtext.Text):
                if not hasattr(obj, "_features"):
                    obj._features = None
                
                if not hasattr(obj, "_language"):
                    obj._language = None

                fp = obj.get_fontproperties()
                for k, v in list(fp.__dict__.items()):
                    if isinstance(v, list):
                        setattr(fp, k, tuple(v))
                obj.set_fontproperties(fp)
        
        return fig


if __name__ == "__main__":
    app_id = "com.hp.mplfigureviewer"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    app = QApplication(sys.argv)
    palette = set_light_palette(window_bg="#E2E2E2")
    app.setPalette(palette)
    window = FigureViewer()
    window.show()
    sys.exit(app.exec())
