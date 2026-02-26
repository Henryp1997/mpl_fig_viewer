from pathlib import Path
import cx_Freeze
import shutil

HERE = Path(__file__).parent

assets_path = HERE / "assets"
executables = [
    cx_Freeze.Executable(
        str(HERE / "mpl_fig_viewer.py"),
        base="Win32GUI",
        target_name="pyFigViewer.exe",
        icon=str(assets_path / "plot_icon.ico")
    )
]

cx_Freeze.setup(
    name="pyFigViewer",
    executables=executables,
    options={
        "build_exe": {
            "zip_exclude_packages": ["numpy", "matplotlib", "PySide6", "shiboken6"], # Keep these out of library.zip
            "zip_include_packages": ["encodings"], # Keep zip small
            "include_msvcr": True, # Maybe needed for Windows
            "include_files": [
                # Copy assets folder to build folder
                (str(assets_path / "blank.pkl"), "blank.pkl"),
                (str(assets_path / "plot_icon.ico"), "plot_icon.ico"),
            ],
        }
    }
)
