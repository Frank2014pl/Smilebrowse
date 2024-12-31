import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import *
import os

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.browser = QWebEngineView()

        # Load the local HTML file
        self.browser.setUrl(QUrl.fromLocalFile(os.path.abspath('homepage.html')))

        self.setCentralWidget(self.browser)
        self.showMaximized()
        self.browser.urlChanged.connect(self.update_urlbar)
        self.browser.loadFinished.connect(self.update_title)

        # Load and set the custom app icon
        self.setWindowIcon(QIcon('icon_512.ico'))

        navbar = QToolBar()
        self.addToolBar(navbar)
        back_btn = QAction('Back', self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)
        forward_btn = QAction('Forward', self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)
        reload_btn = QAction('Reload', self)
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)
        home_btn = QAction('Home', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)
        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.urlbar)
        
        # Menu for selecting the search engine
        self.search_engine_menu = QMenu("Search Engine", self)
        self.search_engine_menu.addAction("Bing", lambda: self.change_search_engine('bing'))
        self.search_engine_menu.addAction("Google", lambda: self.change_search_engine('google'))
        self.search_engine_menu.addAction("DuckDuckGo", lambda: self.change_search_engine('duckduckgo'))
        
        menu_bar = self.menuBar()
        menu_bar.addMenu(self.search_engine_menu)

    def navigate_home(self):
        # Load the local HTML file as the homepage
        self.browser.setUrl(QUrl.fromLocalFile(os.path.abspath('homepage.html')))

    def navigate_to_url(self):
        url = self.urlbar.text()
        self.browser.setUrl(QUrl(url))

    def update_urlbar(self, q):
        self.urlbar.setText(q.toString())

    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle(title)
    
    def change_search_engine(self, engine):
        # Update the search engine dropdown value in the HTML
        script = f"document.getElementById('search-engine').value = '{engine}'; updateSearchForm();"
        self.browser.page().runJavaScript(script)

app = QApplication(sys.argv)
QApplication.setApplicationName("My Browser")
window = Browser()
app.exec_()
