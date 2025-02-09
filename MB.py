import sys
import os
import random
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *

class BrowserTab(QWebEngineView):
    def __init__(self, parent=None, download_folder=None, main_window=None):
        super().__init__(parent)
        self.setUrl(QUrl("http://www.google.com/"))
        self.download_folder = download_folder  # Сохраняем ссылку на папку загрузок
        self.main_window = main_window  # Сохраняем ссылку на MainWindow
        self.page().profile().downloadRequested.connect(self._downloadRequested)

    def _downloadRequested(self, item):
        download_path = os.path.join(self.download_folder, item.suggestedFileName())  # Используем download_folder
        item.setPath(download_path)
        item.accept()  # Начинаем загрузку
        self.main_window.downloads.append((item.suggestedFileName(), download_path))  # Добавляем в список загрузок

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mainfolder = os.path.dirname(__file__)
        self.download_folder = os.path.join(self.mainfolder, "Downloads")
        os.makedirs(self.download_folder, exist_ok=True)
        self.img_folder = os.path.join(self.mainfolder, "icons")
        
        if "-r" in sys.argv:
            self.setWindowTitle(''.join(random.choices('BLIUVFBHBEIVUHBVDIUHGSOIYBGUBPIUBVGPIUHGIPUGPIHUGFHIPUGHPIGUHBPIGHHHBFHJIGOIHJHIHIJFHBJUIjuhblijhublibhjulihjubliGILGOYFYFVihbgdlijsvbgisuhgiHIIGIUGIB16546546sx5ntr65465nh4658d4th464n64x6fd4gnhf68gtnh6f8x4684dtr8468td4n684fdxngt684dx6f84n684td6nj8n6t8f86t468f68n4f6n4f64n546f4t6584nt84t68n4t68486f4nf6ntgf84t', k=random.randint(2000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000, 78258888888877777777777777777777777777777777777777383838383838383838383838383838383838383838383838383838383838383838383838383838383838383838383838383838383838383838383838383838383838383838383838383838383838383838383838383838383838383831366666666666666666666666666666614361436143614361436143631436143614361436143614361436134314366666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666))))
        else:
            self.setWindowTitle("MiniBrowser by ytika 1.1")
        
        self.setGeometry(150, 50, 900, 600)
        self.setWindowIcon(QIcon(os.path.join(self.img_folder, "globe-green.png")))
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.update_urlbar)
        self.setCentralWidget(self.tabs)
        
        self.create_new_tab()
        
        self.downloads = []

        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(16, 16))
        self.addToolBar(navtb)

        back_btn = QAction(QIcon(os.path.join(self.img_folder, "back.png")), "Back", self)
        back_btn.triggered.connect(lambda: self.current_browser().back())
        navtb.addAction(back_btn)

        forward_btn = QAction(QIcon(os.path.join(self.img_folder, "forward.png")), "Forward", self)
        forward_btn.triggered.connect(lambda: self.current_browser().forward())
        navtb.addAction(forward_btn)

        home_btn = QAction(QIcon(os.path.join(self.img_folder, "home.png")), "Home", self)
        home_btn.triggered.connect(lambda: self.current_browser().setUrl(QUrl("http://www.google.com/")))
        navtb.addAction(home_btn)

        reload_btn = QAction(QIcon(os.path.join(self.img_folder, "reload.png")), "Reload", self)
        reload_btn.triggered.connect(lambda: self.current_browser().reload())
        navtb.addAction(reload_btn)

        navtb.addSeparator()

        new_tab_btn = QAction(QIcon(os.path.join(self.img_folder, "new_tab.png")), "New Tab", self)
        new_tab_btn.triggered.connect(self.create_new_tab)
        navtb.addAction(new_tab_btn)

        self.downloads_btn = QAction(QIcon(os.path.join(self.img_folder, "download.png")), "Downloads", self)
        self.downloads_btn.triggered.connect(self.show_downloads)
        navtb.addAction(self.downloads_btn)

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_url)
        navtb.addWidget(self.urlbar)

    def create_new_tab(self, url=QUrl("http://www.google.com/")):
        if url == False:
            url = QUrl("http://www.google.com/")

        print(f"URL передан в create_new_tab: {url} (тип: {type(url)})")
        
        # Проверка на тип переданного URL
        if isinstance(url, QUrl) or isinstance(url, str):
            if isinstance(url, str):
                url = QUrl(url)  # Преобразуем строку в QUrl
            browser = BrowserTab(self, self.download_folder, self)  # Передаем ссылку на MainWindow
            browser.setUrl(url)
            index = self.tabs.addTab(browser, "New Tab")
            self.tabs.setCurrentIndex(index)
            browser.titleChanged.connect(lambda title, browser=browser: self.update_tab_title(title, browser))
            browser.urlChanged.connect(self.update_urlbar)
        else:
            print(f"Invalid URL type provided. Получен тип: {type(url)}")

    def current_browser(self):
        return self.tabs.currentWidget()

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def show_downloads(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Загрузки")
        layout = QVBoxLayout()

        table = QTableWidget()
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Файл", "Открыть"])
        table.setRowCount(len(self.downloads))

        for row, (name, path) in enumerate(self.downloads):
            table.setItem(row, 0, QTableWidgetItem(name))
            open_btn = QPushButton("Открыть")
            open_btn.clicked.connect(lambda _, p=path: self.open_file(p))
            table.setCellWidget(row, 1, open_btn)

        table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(table)
        dialog.setLayout(layout)
        dialog.exec_()

    def open_file(self, path):
        if os.path.exists(path):
            os.startfile(path)

    def update_urlbar(self, index=None):
        if hasattr(self, "urlbar"):
            browser = self.current_browser()
            if browser:
                self.urlbar.setText(browser.url().toString())
            else:
                self.urlbar.clear()

    def navigate_url(self):
        url = QUrl(self.urlbar.text())
        if url.scheme() == "":  # Если схема не указана, добавляем HTTP
            url.setScheme('http')
        if self.current_browser():
            self.current_browser().setUrl(url)

    def update_tab_title(self, title, browser):
        index = self.tabs.indexOf(browser)
        if index != -1:
            self.tabs.setTabText(index, title[:15] + "...")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())

