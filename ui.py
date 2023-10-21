import sys
from PyQt6.QtWidgets import QMessageBox, QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QDialog, QDialogButtonBox
from PyQt6.QtCore import Qt, pyqtSignal
from uncertainty_analysis import getInput

class EditableLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()

class EditLabelDialog(QDialog):
    def __init__(self, initial_text, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Label Text")
        self.layout = QVBoxLayout()

        self.label = QLabel("New Label Text:")
        self.textbox = QLineEdit()
        self.textbox.setText(initial_text)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.textbox)
        self.layout.addWidget(self.button_box)

        self.setLayout(self.layout)

    def get_new_label_text(self):
        return self.textbox.text()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Uncertainty Analysis App")
        self.setGeometry(100, 100, 800, 200)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.side_layout = QHBoxLayout()
        self.left_panel = QWidget()
        self.left_layout = QVBoxLayout()
        self.left_panel.setLayout(self.left_layout)

        self.line_layout_left = QVBoxLayout()
        self.left_layout.addLayout(self.line_layout_left)

        self.right_panel = QWidget()
        self.right_layout = QVBoxLayout()
        self.right_panel.setLayout(self.right_layout)

        self.line_layout_right = QVBoxLayout()
        self.right_layout.addLayout(self.line_layout_right)

        self.button_left = QPushButton("Add new variable", self)
        self.button_left.clicked.connect(self.add_new_line_left)

        self.button_right = QPushButton("Add new function", self)
        self.button_right.clicked.connect(self.add_new_line_right)

        self.left_layout.addWidget(self.button_left)
        self.right_layout.addWidget(self.button_right)

        self.side_layout.addWidget(self.left_panel)
        self.side_layout.addWidget(self.right_panel)


        self.layout.addLayout(self.side_layout)
        self.sigfig_layout = QHBoxLayout()
        self.sigfig_label = QLabel("Significant Figure:", self)
        self.sigfig_textbox = QLineEdit(self)
        self.sigfig_layout.addStretch(1)
        self.sigfig_layout.addWidget(self.sigfig_label)
        self.sigfig_layout.addWidget(self.sigfig_textbox)
        self.sigfig_textbox.setFixedWidth(50)
        self.layout.addLayout(self.sigfig_layout)

        self.calculate_button = QPushButton("Calculate", self)
        self.calculate_button.clicked.connect(self.calculate)
        self.layout.addWidget(self.calculate_button)

        self.central_widget.setLayout(self.layout)

        self.left_labels = []
        self.right_labels = []  # Keep track of the labels on the right side

    def get_left_side_text(self):
        text_values = []
        for i in range(self.line_layout_left.count()):
            widget = self.line_layout_left.itemAt(i).layout()
            if widget:
                text_box = widget.itemAt(1).widget()
                if isinstance(text_box, QLineEdit):
                    text_values.append(text_box.text())
        return text_values

    def get_right_side_text(self):
        text_values = []
        for i in range(self.line_layout_right.count()):
            widget = self.line_layout_right.itemAt(i).layout()
            if widget:
                text_box = widget.itemAt(1).widget()
                if isinstance(text_box, QLineEdit):
                    text_values.append(text_box.text())
        return text_values

    def add_new_line_left(self):
        new_label_left = EditableLabel("x["+str(self.line_layout_left.count())+"]=", self)
        new_label_left.setCursor(Qt.CursorShape.PointingHandCursor)  # Add a pointing hand cursor to indicate it's clickable
        new_textbox_left = QLineEdit(self)

        index = self.line_layout_left.count()
        new_label_left.clicked.connect(lambda: self.edit_label_text(new_label_left, index))

        new_line_layout_left = QHBoxLayout()
        new_line_layout_left.addWidget(new_label_left)
        new_line_layout_left.addWidget(new_textbox_left)

        self.left_labels.append(new_label_left)
        self.line_layout_left.addLayout(new_line_layout_left)

    def add_new_line_right(self):
        new_label_right = EditableLabel("F_"+str(self.line_layout_right.count())+"=", self)
        new_label_right.setCursor(Qt.CursorShape.PointingHandCursor)  # Add a pointing hand cursor to indicate it's clickable
        new_textbox_right = QLineEdit(self)
        new_right_label = QLabel("=", self)  # Initial label value is "="

        new_label_right.clicked.connect(lambda: self.edit_label_text(new_label_right))

        new_line_layout_right = QHBoxLayout()
        new_line_layout_right.addWidget(new_label_right)
        new_line_layout_right.addWidget(new_textbox_right)
        new_line_layout_right.addWidget(new_right_label)  # Add the label

        self.right_labels.append(new_right_label)  # Add the label to the list
        self.line_layout_right.addLayout(new_line_layout_right)

    def edit_label_text(self, label, index):
        label_text = label.text()
        dialog = EditLabelDialog(label_text[:-1])
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_label_text = dialog.get_new_label_text() + '='
            label.setText(new_label_text)

    def get_var_and_unc(self, text):
        var = []
        unc = []

        for s in text:
            v, u = s.split("+-")
            var.append(float(v))
            unc.append(float(u))

        return var, unc
    
    def string_replace(self, name, func):
        sign = "+-*/()"
        sign_pos = [-1]

        for i in range(len(func)):
            if (func[i] in sign):
                sign_pos.append(i)

        sign_pos.append(len(func))

        inc = 0

        for i in range(len(sign_pos) - 1):
            x = sign_pos[i] + 1 + inc
            y = sign_pos[i+1] - 1 + inc

            if (x <= y):
                if (func[x:y+1] in name):
                    inc += len(name[func[x:y+1]]) - len(func[x:y+1])
                    func = func[:x] + name[func[x:y+1]] + func[y+1:]
                

        return func

    def get_symbols(self):
        symbols = {}

        for i in range(self.line_layout_left.count()):
            label = self.left_labels[i].text()
            
            symbols[label[:-1]] = "x[" + str(i) + "]"
            
        return symbols
    
    def show_error_message(self, message):
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Icon.Critical)
        error_box.setWindowTitle("Error")
        error_box.setText(message)
        error_box.exec()

    def calculate(self):
        left_side_text = self.get_left_side_text()
        right_side_text = self.get_right_side_text()
        
        sigfig_value = self.sigfig_textbox.text()

        try:
            int(sigfig_value)
        except:
            self.show_error_message("Signature figure is not in the right format")

        symbols = self.get_symbols()
        try:
            var, unc = self.get_var_and_unc(left_side_text)
        except:
            self.show_error_message("Your variables are not in the right format")

        for i, text in enumerate(right_side_text):
            try:
                right_label = self.right_labels[i]

                right_label.setText("="+getInput(var, unc, self.string_replace(symbols, text), sigfig_value))
            except:
                self.show_error_message("Your function " + str(i) + " is not in the right format")


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
