from PySide6.QtWidgets import QPushButton

class CustomButton(QPushButton):
    def __init__(
        self,
        text,
        font_size=18,
        padding=4,
        text_colour="black",
        border_width=1,
        border_colour="#666666",
        border_radius=3,
        bg_colour="#FF8A00",
        pressed_text_colour="black",
        pressed_bg_colour="white"
    ):
        super().__init__(text)
        self.font_size = font_size
        self.padding = padding
        self.text_colour = text_colour
        self.border_width = border_width
        self.border_colour = border_colour
        self.border_radius = border_radius
        self.bg_colour = bg_colour
        self.pressed_text_colour = pressed_text_colour
        self.pressed_bg_colour = pressed_bg_colour
        self._setStyle()


    def _setStyle(self):
        """ Set custom button style """
        self.setStyleSheet(f"""
            QPushButton {{
                font-size: {self.font_size}px;
                padding: {self.padding}px;
                color: {self.text_colour};
                border: {self.border_width}px solid {self.border_colour}; 
                border-radius: {self.border_radius}px;
                background: {self.bg_colour}
            }}                
            QPushButton::pressed {{
                color: {self.pressed_text_colour};
                background: {self.pressed_bg_colour}
            }}
        """
        )
        return