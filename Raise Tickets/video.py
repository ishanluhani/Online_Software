import sys
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QSlider, QLabel, QFileDialog

class AdvancedVideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Advanced Video Player")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("video_icon.png"))

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.media_player = QMediaPlayer(self)
        self.video_widget = QVideoWidget()
        self.media_player.setVideoOutput(self.video_widget)
        self.layout.addWidget(self.video_widget)

        self.controls_layout = QVBoxLayout()
        self.play_button = QPushButton("Play")
        self.pause_button = QPushButton("Pause")
        self.stop_button = QPushButton("Stop")
        self.seek_slider = QSlider(Qt.Horizontal)
        self.seek_label = QLabel("Seek:")

        self.controls_layout.addWidget(self.play_button)
        self.controls_layout.addWidget(self.pause_button)
        self.controls_layout.addWidget(self.stop_button)
        self.controls_layout.addWidget(self.seek_label)
        self.controls_layout.addWidget(self.seek_slider)
        self.layout.addLayout(self.controls_layout)

        self.play_button.clicked.connect(self.play_video)
        self.pause_button.clicked.connect(self.pause_video)
        self.stop_button.clicked.connect(self.stop_video)
        self.seek_slider.sliderMoved.connect(self.seek_video)
        print(self.media_player.position())

        self.menu_bar = self.menuBar()
        self.file_menu = self.menu_bar.addMenu("File")
        self.open_action = self.file_menu.addAction("Open Video")
        self.open_action.triggered.connect(self.open_video)

    def play_video(self):
        self.media_player.play()

    def pause_video(self):
        self.media_player.pause()

    def stop_video(self):
        self.media_player.stop()

    def seek_video(self, position):
        self.media_player.setPosition(position)

    def open_video(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open Video File", "", "Video Files (*.mp4 *.avi *.mkv *.mov)")
        if file_path:
            video_url = QUrl.fromLocalFile(file_path)
            video_content = QMediaContent(video_url)
            self.media_player.setMedia(video_content)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = AdvancedVideoPlayer()
    player.show()
    sys.exit(app.exec_())
