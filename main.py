from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, 
                             QHBoxLayout, QPushButton, QAction,
                             QFileDialog, QVBoxLayout, QSlider, 
                             QStyle)
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QUrl
import os

import sys

class MyMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent) 
    
        self.layouts_create()
        self.main_widgets_create()
        self.layouts_append_elements()
        self.main_function()
        self.menu_and_action_create()
        self.main_button_create()
        self.volume_slider_create()
        self.position_slider_create()
        
    def volume_slider_create(self):
        self.volume_slider = QSlider(Qt.Vertical)
        self.volume_slider.sliderMoved.connect(self.change_volume)
        self.volume_slider.setValue(50)
        self.video_layout.addWidget(self.volume_slider)
        
    def position_slider_create(self):
        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.setValue(0)
        self.position_slider.sliderMoved.connect(self.change_position)
        self.slider_layout.addWidget(self.position_slider)
        
    def menu_and_action_create(self):
        self.menu = self.menuBar()
        self.fileMenu = self.menu.addMenu('&File')
        
        self.openAction = QAction(QIcon('open.png'), '&Open', self)        
        self.openAction.setShortcut('Ctrl+O')
        self.openAction.setStatusTip('Open movie')
        self.openAction.triggered.connect(self.openFile)
        
        self.fileMenu.addAction(self.openAction)
        
    def main_button_create(self):
        self.playOrNOt = False
        
        self.play_button = QPushButton()
        self.next_item = QPushButton()
        self.preview_button = QPushButton()
        
        self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.next_item.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekForward))
        self.preview_button.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekBackward))
        
        self.play_button.clicked.connect(self.play)
        self.next_item.clicked.connect(self.next_element)
        self.preview_button.clicked.connect(self.preview_element)
        
        self.playlist_layout.addWidget(self.preview_button)
        self.playlist_layout.addWidget(self.play_button)
        self.playlist_layout.addWidget(self.next_item)
        
    def layouts_create(self):
        self.main_layout = QVBoxLayout()
        self.video_layout = QHBoxLayout()
        self.slider_layout = QHBoxLayout()
        self.playlist_layout = QHBoxLayout()
        
    def layouts_append_elements(self):
        self.video_layout.addWidget(self.video_player)
        
        self.main_layout.addLayout(self.video_layout)
        self.main_layout.addLayout(self.slider_layout)
        self.main_layout.addLayout(self.playlist_layout)
        
        self.wid.setLayout(self.main_layout)
        
    def main_widgets_create(self):
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.video_player = QVideoWidget()
        self.wid = QWidget(self)
        self.setCentralWidget(self.wid)
        
    def main_function(self):
        self.mediaPlayer.durationChanged.connect(self.dur_changed) 
        self.mediaPlayer.setVideoOutput(self.video_player)
        
    def extension_filter(self, filename):
        extension = filename.split('.')[-1]
        if extension in ['mp4', 'avi', 'vmw', 'mpegps', 'mov', '3gpp', 'mpeg-4', 'mkv']:
            return filename
            
    def openFile(self):
        filename, ok = QFileDialog.getOpenFileName(self)
        if filename != '':
            self.file = self.extension_filter(filename)
           
        if self.file != None:
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.file)))
            
    def play(self):
        if self.playOrNOt:
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
            self.mediaPlayer.pause()
            self.playOrNOt = False
        else:
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
            self.mediaPlayer.play()
            self.playOrNOt = True
    
    def next_element(self):
        folder = self.file.split('/')[1:-1]
        folder = '/'.join(folder)
        
        filenames = os.listdir('/' + folder)
        
        filenames = list(filter(self.extension_filter, filenames))
        need_file = self.file.split('/')[-1]
        full_path = self.file.split('/')[0:-1]
        full_path = '/'.join(full_path)
        for _ in range(len(filenames)):
            if filenames[_] == need_file:
                self.position_slider.setValue(0)
                if _ == len(filenames):
                    if self.playOrNOt:
                        self.play()
                        self.file = full_path + '/' + filenames[0]
                        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.file)))
                else:
                    self.play()
                    self.file = full_path + '/' + filenames[_ + 1]
                    self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.file)))
    
    def preview_element(self):
        folder = self.file.split('/')[1:-1]
        folder = '/'.join(folder)
        
        filenames = os.listdir('/' + folder)
        
        filenames = list(filter(self.extension_filter, filenames))
        need_file = self.file.split('/')[-1]
        full_path = self.file.split('/')[0:-1]
        full_path = '/'.join(full_path)
        for _ in range(len(filenames)):
            if filenames[_] == need_file:
                self.position_slider.setValue(0)
                if _ == 0:
                    if self.playOrNOt:
                        self.play()
                        self.file = full_path + '/' + filenames[len(filenames)]
                        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.file)))
                else:
                    self.play()
                    self.file = full_path + '/' + filenames[_ - 1]
                    self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.file)))
    
    def dur_changed(self, duration):
        self.position_slider.setRange(0, duration)
    
    def change_volume(self, value):
        self.mediaPlayer.setVolume(value)
        
    def change_position(self, value):
        self.mediaPlayer.setPosition(value)
            

app = QApplication([])
foo = MyMainWindow()

foo.show()
foo.resize(640, 480)
sys.exit(app.exec_())

