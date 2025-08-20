import json
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QColorDialog, QFileDialog
from PyQt5.QtGui import QColor

class MatrixControlWidget(QtWidgets.QWidget):
    def __init__(self, neopixel_control, parent=None):
        super().__init__(parent)
        uic.loadUi('_ui/NeoPixel_Matrix_Control.ui', self)

        self.neopixel_control = neopixel_control
        self.selected_color = QColor(255, 255, 255)

        self._create_pixel_grid()
        self._connect_signals()
        self._populate_animations()
        self.update_selected_color_label()

    def _create_pixel_grid(self):
        self.pixel_buttons = []
        for y in range(16):
            row_buttons = []
            for x in range(16):
                btn = QtWidgets.QPushButton()
                btn.setFixedSize(30, 30)
                btn.setStyleSheet("background-color: black")
                btn.clicked.connect(lambda _, x=x, y=y: self.on_pixel_clicked(x, y))
                self.pixel_grid_layout.addWidget(btn, y, x)
                row_buttons.append(btn)
            self.pixel_buttons.append(row_buttons)

    def _connect_signals(self):
        self.color_picker_button.clicked.connect(self.on_color_picker_clicked)
        self.save_pattern_button.clicked.connect(self.on_save_pattern_clicked)
        self.load_pattern_button.clicked.connect(self.on_load_pattern_clicked)
        self.apply_pattern_button.clicked.connect(self.on_apply_pattern_clicked)
        self.run_animation_button.clicked.connect(self.on_run_animation_clicked)

    def _populate_animations(self):
        for name in self.neopixel_control.animations.keys():
            self.animation_combobox.addItem(name.capitalize())

    def on_pixel_clicked(self, x, y):
        color = (self.selected_color.red(), self.selected_color.green(), self.selected_color.blue())
        self.neopixel_control.set_pixel(x, y, color)
        self.pixel_buttons[y][x].setStyleSheet(f"background-color: {self.selected_color.name()}")

    def on_color_picker_clicked(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.selected_color = color
            self.update_selected_color_label()

    def update_selected_color_label(self):
        self.selected_color_label.setText(f"Selected Color: {self.selected_color.name()}")
        self.selected_color_label.setStyleSheet(f"color: {self.selected_color.name()}")


    def on_save_pattern_clicked(self):
        pattern = self.neopixel_control.get_pattern()
        filepath, _ = QFileDialog.getSaveFileName(self, "Save Pattern", "", "JSON Files (*.json)")
        if filepath:
            with open(filepath, 'w') as f:
                json.dump(pattern, f)

    def on_load_pattern_clicked(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Load Pattern", "", "JSON Files (*.json)")
        if filepath:
            with open(filepath, 'r') as f:
                pattern = json.load(f)
            self.neopixel_control.load_pattern(pattern)
            self.update_grid_from_pattern(pattern)

    def on_apply_pattern_clicked(self):
        # In simulation mode, this doesn't do much, but in a real application,
        # it would send the pattern to the hardware.
        self.neopixel_control.load_pattern(self.neopixel_control.get_pattern())
        print("SIM: Applying pattern to hardware")

    def on_run_animation_clicked(self):
        animation_name = self.animation_combobox.currentText().lower()
        self.neopixel_control.run_animation(animation_name)
        # We would need a timer to call neopixel_control.animate() repeatedly
        print(f"SIM: Running animation: {animation_name}")


    def update_grid_from_pattern(self, pattern):
        for y, row in enumerate(pattern):
            for x, color in enumerate(row):
                qcolor = QColor(*color)
                self.pixel_buttons[y][x].setStyleSheet(f"background-color: {qcolor.name()}")
