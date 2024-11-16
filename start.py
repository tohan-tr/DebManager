from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QProgressBar, QFileDialog, QStackedWidget, QFrame, QMessageBox
)
from PyQt5.QtCore import QThread, pyqtSignal
import subprocess
import os
import sys
import json

class InstallThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool)

    def __init__(self, deb_file_path):
        super().__init__()
        self.deb_file_path = deb_file_path

    def run(self):
        try:
            process = subprocess.Popen(["sudo", "dpkg", "-i", self.deb_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            for step in range(101):
                self.progress.emit(step)
                QThread.msleep(50)
            process.wait()
            self.finished.emit(process.returncode == 0)
        except Exception:
            self.finished.emit(False)

class DebInstallerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.check_root_access()
        self.setWindowTitle("DebManager")
        self.setFixedSize(700, 400)

        self.initUI()
        self.install_thread = None
        self.deb_file_path = None
        self.installed_app_path = "/path/to/your/application"

    def check_root_access(self):
        if os.geteuid() != 0:
            QMessageBox.critical(self, "Root Yetkisi Gerekli", 
                                 "Bu uygulama root yetkisi gerektiriyor.\nLütfen root olup tekrar çalıştırın.")
            sys.exit()

    def initUI(self):
        menubar = self.menuBar()
        title_action = menubar.addAction("DebManager")
        title_action.setEnabled(False)

        main_layout = QHBoxLayout()
        menu_layout = QVBoxLayout()
        self.content_stack = QStackedWidget()

        menu_frame = QFrame()
        menu_frame.setLayout(menu_layout)

        buttons = {
            "Ana Sayfa": self.show_home,
            "Hakkında": self.show_about,
        }

        for text, action in buttons.items():
            button = QPushButton(text)
            button.clicked.connect(action)
            menu_layout.addWidget(button)

        exit_button = QPushButton("Çıkış")
        exit_button.clicked.connect(self.close)
        menu_layout.addStretch()
        menu_layout.addWidget(exit_button)

        self.home_widget = QWidget()
        self.downloads_widget = QWidget()
        self.about_widget = QWidget()

        self.init_home()
        self.init_downloads()
        self.init_about()

        self.content_stack.addWidget(self.home_widget)
        self.content_stack.addWidget(self.downloads_widget)
        self.content_stack.addWidget(self.about_widget)

        main_layout.addWidget(menu_frame, 1)
        main_layout.addWidget(self.content_stack, 3)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        self.show_home()

    def show_home(self):
        self.content_stack.setCurrentWidget(self.home_widget)

    def show_downloads(self):
        self.content_stack.setCurrentWidget(self.downloads_widget)

    def show_about(self):
        self.content_stack.setCurrentWidget(self.about_widget)

    def init_home(self):
        layout = QVBoxLayout()
        self.deb_file_label = QLabel("Seçilen Dosya: Yok")
        layout.addWidget(self.deb_file_label)

        select_button = QPushButton("Dosya Seç")
        select_button.clicked.connect(self.load_file)

        self.load_button = QPushButton("Yükle")
        self.load_button.setDisabled(True)
        self.load_button.clicked.connect(self.start_installation)

        layout.addWidget(select_button)
        layout.addWidget(self.load_button)
        self.home_widget.setLayout(layout)

    def init_downloads(self):
        layout = QVBoxLayout()
        self.progress_label = QLabel("Yükleme Durumu")
        self.progress_bar = QProgressBar()

        self.open_button = QPushButton("Uygulamayı Aç")
        self.open_button.setDisabled(True)
        self.open_button.clicked.connect(self.open_application)

        layout.addWidget(self.progress_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.open_button)
        self.downloads_widget.setLayout(layout)

    def init_about(self):
        layout = QVBoxLayout()
        settings = self.load_settings()

        version_label = QLabel(f"Sürüm: {settings['version']}")
        update_label = QLabel("Güncelleme Tarihi: 24/10/2024")
        size_label = QLabel("İndirme Boyutu: 6.7 KİB")
        os_label = QLabel("Gerekli İşletim Sistemi: Linux")
        provider_label = QLabel("Sunan: TOHAN")
        release_label = QLabel("Çıkış Tarihi: 24/10/2024")

        layout.addWidget(version_label)
        layout.addWidget(update_label)
        layout.addWidget(size_label)
        layout.addWidget(os_label)
        layout.addWidget(provider_label)
        layout.addWidget(release_label)
        self.about_widget.setLayout(layout)

    def load_file(self):
        self.deb_file_path, _ = QFileDialog.getOpenFileName(self, "Deb Dosyası Seç", "", "Deb Dosyaları (*.deb)")
        if self.deb_file_path:
            self.deb_file_label.setText(f"Seçilen Dosya: {self.deb_file_path}")
            self.load_button.setEnabled(True)

    def start_installation(self):
        self.load_button.setDisabled(True)
        self.progress_bar.setValue(0)
        self.install_thread = InstallThread(self.deb_file_path)
        self.install_thread.progress.connect(self.update_progress)
        self.install_thread.finished.connect(self.installation_finished)
        self.install_thread.start()
        self.show_downloads()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def installation_finished(self, success):
        if success:
            QMessageBox.information(self, "Başarılı", "Kurulum başarılı!")
            self.open_button.setEnabled(True)
        else:
            QMessageBox.critical(self, "Hata", "Kurulum sırasında bir hata oluştu.")

    def open_application(self):
        os.startfile(self.installed_app_path)

    def load_settings(self):
        settings_file = "settings.json"
        if os.path.exists(settings_file):
            with open(settings_file, "r") as f:
                return json.load(f)
        return {"version": "1.0.0"}

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DebInstallerApp()
    window.show()
    sys.exit(app.exec_())
