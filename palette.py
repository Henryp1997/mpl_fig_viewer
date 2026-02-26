def set_light_palette(window_bg="#F3F3F3"):
    """
    Set light mode palette for all elements.
    This prevents windows light/dark mode from styling
    text and window elements and helps keep a consistent
    look across all windows styles
    """
    from PySide6.QtGui import QPalette, QColor

    default_palette = {
        "WindowText"     : "#000000",
        "Button"         : "#FFFFFF",
        "Light"          : "#FFFFFF",
        "Midlight"       : "#FFFFFF",
        "Dark"           : "#787878",
        "Mid"            : "#A0A0A0",
        "Text"           : "#000000",
        "BrightText"     : "#0067C0",
        "ButtonText"     : "#000000",
        "Base"           : "#FFFFFF",
        "Window"         : window_bg,
        "Shadow"         : "#000000",
        "Highlight"      : "#0067C0",
        "HighlightedText": "#FFFFFF",
        "Link"           : "#003E92",
        "LinkVisited"    : "#001A68",
        "AlternateBase"  : "#000000",
        "NoRole"         : "#000000",
        "ToolTipBase"    : "#F3F3F3",
        "ToolTipText"    : "#000000",
        "PlaceholderText": "#000000"
    }

    palette = QPalette()
    for role, colour in default_palette.items():
        if hasattr(QPalette, role):
            palette.setColor(getattr(QPalette, role), QColor(colour))

    return palette
