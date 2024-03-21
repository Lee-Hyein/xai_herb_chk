import os
import cv2
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QStackedWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QIcon, QPixmap, QImage
from ImageConfirmationWindow2 import ImageConfirmationWindow

import qdarktheme

class FirstPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 가로 레이아웃 생성
        hbox = QHBoxLayout()

        # 레이블 추가
        self.label = QLabel('한(생)약재 관능 검사 보조 XAI 프로그램')
        font = self.label.font()
        font.setPointSize(32)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hbox.addWidget(self.label)

        # 수직 레이아웃에 가로 레이아웃 추가
        layout.addLayout(hbox)
        #layout.addSpacing(100)  # 간격을 추가하여 hbox와 label_layout 사이의 간격을 늘립니다.
        
        # 버튼 추가
        label_layout = QVBoxLayout()
        self.label2 = QLabel('과제명: 인공지능 XAI 등을 활용한 한약(생약)재 관능검사 보조기술 개발 연구')
        font = self.label2.font()
        font.setPointSize(15)
        #font.setBold(True)
        self.label2.setFont(font)
        self.label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_layout.addWidget(self.label2)

        label_layout.addSpacing(200)

        label_text = "실시간 한약재 분석 프로그램입니다.\n\n시작을 원하시면 <시작> 버튼을 눌러주세요."
        label_1 = QLabel(label_text, self)
        label_1.setAlignment(Qt.AlignCenter)
        label_1.setStyleSheet("font-size: 30px; font-weight: bold; border: none;")  # 글자 크기와 굵기 설정
        label_layout.addWidget(label_1, alignment=Qt.AlignCenter)  # 가운데 정렬
        label_layout.addSpacing(50)

        self.button = QPushButton('시작')
        self.button.setFixedSize(200, 80)  # 버튼의 크기를 조정합니다.
        self.button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 25px;")  # 배경색과 글자색을 설정합니다.
        label_layout.addWidget(self.button, alignment=Qt.AlignCenter)
        
        self.logo = QLabel(self)
        self.logo.setPixmap(QPixmap("logo3.jpg").scaled(290, 100))

        label_layout.addWidget(self.logo)
        layout.addLayout(label_layout)
        self.setLayout(layout)

class SecondPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        layout = QHBoxLayout() #옆으로

        hbox = QHBoxLayout()
        hbox.setAlignment(Qt.AlignTop)

        # 홈 모양의 아이콘
        current_path = os.path.dirname(os.path.abspath(__file__))  # 현재 스크립트 파일의 경로
        icon_path = os.path.join(current_path, 'home_button.png')  # 이미지 파일의 경로
        pixmap = QPixmap(icon_path)
        pixmap = pixmap.scaled(70,70)  # 이미지를 70*70 크기로 조정합니다.
        self.home_button = QPushButton(QIcon(pixmap), '')
        self.home_button.setIconSize(self.home_button.sizeHint())  # 아이콘 크기 조정
        self.home_button.setFixedSize(80,80)  # 버튼의 크기를 조정합니다.
        hbox.addWidget(self.home_button)
        main_layout.addLayout(hbox)

        # Left layout
        left_layout = QVBoxLayout()

        self.video_label = QLabel()
        self.video_label.setFixedSize(430,400)  # 적절한 크기로 조절하세요.
        self.video_label.setScaledContents(True)  # 이미지 크기를 QLabel의 크기에 맞게 자동으로 조정
        left_layout.addWidget(self.video_label)
        left_layout.addSpacing(50)

        self.button_1 = QPushButton("촬  영", self)
        self.button_1.setFixedWidth(430)
        self.button_1.setFixedHeight(80)
        self.button_1.setStyleSheet("border-radius: 10px; background-color: #FFA500; color: black; font-size: 20pt; font-weight: bold;")
        self.button_1.clicked.connect(self.capture_button)
        left_layout.addWidget(self.button_1)

        layout.addLayout(left_layout)

        layout.addSpacing(100)  

        # Right layout
        right_layout = QVBoxLayout()

        self.image_label = QLabel()
        self.image_label.setFixedSize(430,400)
        self.image_label.setScaledContents(True)
        right_layout.addWidget(self.image_label)
        right_layout.addSpacing(50)

        self.button_2 = QPushButton("확  정", self)
        self.button_2.setFixedWidth(430)
        self.button_2.setFixedHeight(80)
        self.button_2.setStyleSheet("border-radius: 10px; background-color: #32CD32; color: black; font-size: 20pt; font-weight: bold;")
        self.button_2.clicked.connect(self.confirm_button)
        right_layout.addWidget(self.button_2)

        layout.addLayout(right_layout)

        main_layout.addLayout(layout)
        main_layout.addSpacing(150)

        # 카메라 캡처 시작
        self.capture = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.zoom_factor = 1  # 줌 배율 초기값
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  

        self.test_image = None 

        self.button = QPushButton('다음 페이지로')
        main_layout.addWidget(self.button)
        
        self.setLayout(main_layout)    

    def keyPressEvent(self, event):
        key = event.key()
        if isinstance(key, int):  # key가 int 타입인지 확인
            print("Key pressed:", key)
            if key == Qt.Key_Plus:
                self.zoom_factor = min(self.zoom_factor * 1.1, 4)
                print("Zoom factor:", self.zoom_factor)

            elif key == Qt.Key_Minus:
                self.zoom_factor = max(self.zoom_factor / 1.1, 1)
                print("Zoom factor:", self.zoom_factor)

    def zoom_frame(self, frame, zoom_factor):
        height, width = frame.shape[:2]
        centerX, centerY = int(width / 2), int(height / 2)

        # 줌 배율에 따른 새로운 너비와 높이 계산
        new_width = int(width / zoom_factor)
        new_height = int(height / zoom_factor)

        # 새로운 너비와 높이를 중심으로 프레임을 자릅니다
        left_x = max(centerX - new_width // 2, 0)
        right_x = min(centerX + new_width // 2, width)
        top_y = max(centerY - new_height // 2, 0)
        bottom_y = min(centerY + new_height // 2, height)

        cropped_frame = frame[top_y:bottom_y, left_x:right_x]

        # 자른 프레임을 원본 프레임 크기로 리사이즈
        return cv2.resize(cropped_frame, (width, height))
    
    def update_frame(self):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            if self.zoom_factor != 1:
                frame = self.zoom_frame(frame, self.zoom_factor)
            q_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(q_img))

    def capture_button(self, text):
        print("촬영 버튼을 클릭했습니다.")
            #이미지 전처리 함수

        ret, frame = self.capture.read()
        if ret:
            if self.zoom_factor != 1:
                frame = self.zoom_frame(frame, self.zoom_factor)
            self.test_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cv2.imwrite("image_rgb.jpg", frame)

            pixmap = QPixmap.fromImage(QImage(self.test_image, self.test_image.shape[1], self.test_image.shape[0], self.test_image.shape[1] * 3, QImage.Format_RGB888))
            self.image_label.setPixmap(pixmap)
            self.image_label.setScaledContents(True)             

    def confirm_button(self, text):
        print("확정 버튼을 클릭했습니다.")
        # Add your right button action here
        confirmation_window = ImageConfirmationWindow()
        confirmation_window.exec_()

        


class ThirdPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        hbox = QHBoxLayout()
        hbox.setAlignment(Qt.AlignTop)

        # 홈 모양의 아이콘
        current_path = os.path.dirname(os.path.abspath(__file__))  # 현재 스크립트 파일의 경로
        icon_path = os.path.join(current_path, 'home_button.png')  # 이미지 파일의 경로
        pixmap = QPixmap(icon_path)
        pixmap = pixmap.scaled(70,70)  # 이미지를 70*70 크기로 조정합니다.
        self.button = QPushButton(QIcon(pixmap), '')
        self.button.setIconSize(self.button.sizeHint())  # 아이콘 크기 조정
        self.button.setFixedSize(80,80)  # 버튼의 크기를 조정합니다.
        hbox.addWidget(self.button)
        layout.addLayout(hbox)
        #layout.addSpacing(30)

        # 버튼 추가
        button_layout = QHBoxLayout()
        
        self.prediction_button = QPushButton('예측')
        self.prediction_button.clicked.connect(self.showPrediction)
        button_layout.addWidget(self.prediction_button)

        self.analysis_button = QPushButton('분석')
        self.analysis_button.clicked.connect(self.showAnalysis)
        button_layout.addWidget(self.analysis_button)

        self.result_button = QPushButton('결과')
        self.result_button.clicked.connect(self.showResult)
        button_layout.addWidget(self.result_button)

        layout.addLayout(button_layout)

        # 예측, 분석, 결과 화면 추가
        self.prediction_page = QLabel('예측 화면')
        layout.addWidget(self.prediction_page)
        self.prediction_page.hide()  # 초기에는 숨겨둠

        self.analysis_page = QLabel('분석 화면')
        layout.addWidget(self.analysis_page)
        self.analysis_page.hide()  # 초기에는 숨겨둠

        self.result_page = QLabel('결과 화면')
        layout.addWidget(self.result_page)
        self.result_page.hide()  # 초기에는 숨겨둠

        self.setLayout(layout)
    
    def showPrediction(self):
        self.prediction_page.show()
        self.analysis_page.hide()
        self.result_page.hide()

    def showAnalysis(self):
        self.prediction_page.hide()
        self.analysis_page.show()
        self.result_page.hide()

    def showResult(self):
        self.prediction_page.hide()
        self.analysis_page.hide()
        self.result_page.show()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('한약재 분류 프로그램')
        self.setMinimumSize(1500,900)  # 창의 최소 크기를 설정합니다.
        self.setStyleSheet("background-color: white;")

        
        self.stackedWidget = QStackedWidget(self)

        self.page1 = FirstPage()
        self.page1.button.clicked.connect(self.showSecondPage)
        self.stackedWidget.addWidget(self.page1)

        self.page2 = SecondPage()
        self.page2.home_button.clicked.connect(self.showFirstPage)
        self.page2.button.clicked.connect(self.showThirdPage)
        self.stackedWidget.addWidget(self.page2)

        self.page3 = ThirdPage()
        self.page3.button.clicked.connect(self.showFirstPage)
        self.stackedWidget.addWidget(self.page3)

        layout = QVBoxLayout()
        layout.addWidget(self.stackedWidget)
        self.setLayout(layout)
    
    def showThirdPage(self):
        self.stackedWidget.setCurrentIndex(2)

    def showSecondPage(self):
        self.stackedWidget.setCurrentIndex(1)

    def showFirstPage(self):
        self.stackedWidget.setCurrentIndex(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    qdarktheme.setup_theme("light")
    # 사용할 한국어 폰트 선택
    korean_font = QFont("맑은 고딕")
    app.setFont(korean_font)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
