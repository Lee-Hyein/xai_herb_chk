from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QDialog


class ImageConfirmationWindow(QDialog):

    def __init__(self, parent=None):
        super(ImageConfirmationWindow, self).__init__(parent)
        self.classification_result = None

        # 모델 선택 버튼
        self.sanjo_button = QPushButton("산조인류 분류", self)
        self.sanjo_button.clicked.connect(self.sanjo_classification_clicked)

        self.bangpung_button = QPushButton("방풍류 분류", self)
        self.bangpung_button.clicked.connect(self.bangpung_classification_clicked)

        # Create a vertical layout for buttons
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.sanjo_button)
        button_layout.addSpacing(50)  # Adjust the spacing as needed
        button_layout.addWidget(self.bangpung_button)

        # Set up the main layout
        layout = QVBoxLayout(self)
        layout.addLayout(button_layout)

        self.setWindowTitle("모델 선택")
        self.setGeometry(850, 350, 400, 300)

    def sanjo_classification_clicked(self):
        print("산조인류 분류 버튼을 클릭했습니다.")
        # Write to file
        file_path = "sanjo.txt"
        with open(file_path, "w") as file:
            file.write("   산조인류 모델로 분석 중입니다.")
        self.close()

    def bangpung_classification_clicked(self):
        print("방풍류 분류 버튼을 클릭했습니다.")
        # Write to file
        file_path = "bangpung.txt"
        with open(file_path, "w") as file:
            file.write("    방풍류 모델로 분석 중입니다.")
        self.close()