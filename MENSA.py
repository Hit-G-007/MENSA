import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, 
    QMessageBox, QProgressBar, QListWidget, QInputDialog, QTableWidget, QTableWidgetItem,
    QHeaderView, QFormLayout, QStackedWidget
)
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QFont, QPixmap, QIcon, QColor, QBrush
import mysql.connector
import matplotlib.pyplot as plt

class LoadingScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MENSA')
        self.setFixedSize(600, 400)
        self.setWindowIcon(QIcon("title_logo.png"))
        self.setStyleSheet("background-color: #176276;")
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        logo = QLabel(self)
        pixmap = QPixmap("load_logo.png")
        logo.setPixmap(pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio))
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        '''self.app_name = QLabel("MENSA")
        self.app_name.setFont(QFont('Century Gothic', 40))
        self.app_name.setStyleSheet("color: white;")
        self.app_name.setAlignment(Qt.AlignmentFlag.AlignCenter)'''
        
        self.loading_bar = QProgressBar()
        self.loading_bar.setStyleSheet("QProgressBar {background-color: white; border-radius: 10px; text-align: center; color: white}"
                                       "QProgressBar::chunk {background-color: #176276;}")
        self.loading_bar.setRange(0, 100)
        self.loading_bar.setValue(0)

        layout.addWidget(logo)
        '''layout.addWidget(self.app_name)'''
        layout.addWidget(self.loading_bar)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(50)

    def update_progress(self):
        value = self.loading_bar.value() + 1
        self.loading_bar.setValue(value)
        if value >= 100:
            self.timer.stop()
            self.close()
            self.open_login_window()

    def open_login_window(self):
        self.login_window = LoginWindow()
        self.login_window.show()

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MENSA')
        self.setFixedSize(600, 500)
        self.setWindowIcon(QIcon("title_logo.png"))
        self.setStyleSheet("background-color: white;")
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        logo = QLabel(self)
        pixmap = QPixmap("log_logo.png")
        logo.setPixmap(pixmap.scaled(350, 350, Qt.AspectRatioMode.KeepAspectRatio))
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        '''app_name = QLabel("MENSA")
        app_name.setFont(QFont('Century Gothic', 24))
        app_name.setStyleSheet("color: navy;")
        app_name.setAlignment(Qt.AlignmentFlag.AlignCenter)'''
        
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("USERNAME")
        self.username_input.setFont(QFont('Century Gothic', 14))
        self.username_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("PASSWORD")
        self.password_input.setFont(QFont('Century Gothic', 14))
        self.password_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        login_button = QPushButton("Login", self)
        login_button.setFont(QFont('Century Gothic', 16))
        login_button.setStyleSheet("background-color: #176276; color: white;")
        login_button.clicked.connect(self.handle_login)

        layout.addWidget(logo)
        '''layout.addWidget(app_name)'''
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        self.connecting_window = ConnectingWindow(username, password)
        self.connecting_window.show()
        self.close()

class ConnectingWindow(QWidget):
    def __init__(self, username, password):
        super().__init__()
        self.setWindowTitle('MENSA')
        self.setFixedSize(600, 400)
        self.setWindowIcon(QIcon("title_logo.png"))
        self.setStyleSheet("background-color: #176276;")
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.status_label = QLabel("Connecting to MySQL Database....")
        self.status_label.setFont(QFont('Century Gothic', 25))
        self.status_label.setStyleSheet("color: white;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.status_label)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.check_connection(username, password))
        self.timer.start(2000)

    def check_connection(self, username, password):
        self.timer.stop()
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user=username,
                password=password
            )
            self.status_label.setText("Connection Successful")
            QTimer.singleShot(2000, self.open_main_app)
        except mysql.connector.Error as err:
            self.status_label.setText("Unable to connect with the \nMySQL Database Server.\nPlease re-check your \nlogin credentials")
            QTimer.singleShot(2000, self.open_login_window)

    def open_login_window(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    def open_main_app(self):
        self.main_app = MainApp(self.connection)
        self.main_app.show()
        self.close()

class MainApp(QMainWindow):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.setWindowTitle('MENSA - MySQL Enhanced for Navigational Speed and Administration')
        self.setWindowIcon(QIcon("title_logo.png"))
        self.setStyleSheet("background-color: white;")
        self.showMaximized()
        self.initUI()

    def initUI(self):
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.db_arena = DatabaseArena(self.connection, self)
        self.central_widget.addWidget(self.db_arena)

        self.create_menu()

    def create_menu(self):
        self.menu = self.menuBar()
        self.menu.setStyleSheet("background-color: navy; color: white; font: 12pt 'Century Gothic';")

        logout_action = self.menu.addAction("Logout")
        logout_action.triggered.connect(self.logout)
        
        refresh_action = self.menu.addAction("Refresh")
        refresh_action.triggered.connect(self.refresh)
        
        help_action = self.menu.addAction("Help")
        
        reach_us_menu = self.menu.addMenu("Reach Us")
        reach_us_action = reach_us_menu.addAction("Reach Us")
        reach_us_action.triggered.connect(self.open_reach_us)
        
        feedback_action = reach_us_menu.addAction("Feedback")
        feedback_action.triggered.connect(self.open_feedback)
        
    def logout(self):
        reply = QMessageBox.question(self, 'Logout', 'Are you sure you want to logout?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.close()
            self.login_window = LoginWindow()
            self.login_window.show()

    def refresh(self):
        self.db_arena.update_databases()

    def open_reach_us(self):
        import webbrowser
        webbrowser.open("https://sites.google.com/view/hytaeschsdexterity/work")

    def open_feedback(self):
        import webbrowser
        webbrowser.open("https://forms.gle/fnHgC6gdZDQfvFeH6")

    def switch_widget(self, widget):
        self.central_widget.setCurrentWidget(widget)

class DatabaseArena(QWidget):
    def __init__(self, connection, main_window):
        super().__init__()
        self.connection = connection
        self.main_window = main_window
        self.setStyleSheet("background-color: white;")
        layout = QVBoxLayout()
        self.setLayout(layout)

        header = QLabel("DATABASES")
        header.setFont(QFont('Century Gothic', 24))
        header.setStyleSheet("color: navy;")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.tool_bar = DatabaseToolBar(self.connection, self)

        self.database_list = QListWidget()
        self.database_list.setFont(QFont('Century Gothic', 14))
        self.database_list.itemDoubleClicked.connect(self.open_tables_arena)

        layout.addWidget(header)
        layout.addWidget(self.tool_bar)
        layout.addWidget(self.database_list)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.update_databases()

    def update_databases(self):
        self.database_list.clear()
        databases = self.fetch_databases()
        for db in databases:
            self.database_list.addItem(db[0])

    def fetch_databases(self):
        cursor = self.connection.cursor()
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        cursor.close()
        return databases

    def open_tables_arena(self, item):
        self.tables_arena = TablesArena(self.connection, item.text(), self.main_window)
        self.main_window.central_widget.addWidget(self.tables_arena)
        self.main_window.switch_widget(self.tables_arena)

class TablesArena(QWidget):
    def __init__(self, connection, database_name, main_window):
        super().__init__()
        self.connection = connection
        self.database_name = database_name
        self.main_window = main_window
        self.setWindowTitle(f'Tables - {database_name}')
        self.setStyleSheet("background-color: white;")
        layout = QVBoxLayout()
        self.setLayout(layout)

        header = QLabel(f"Tables in {database_name}")
        header.setFont(QFont('Century Gothic', 24))
        header.setStyleSheet("color: navy;")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.tool_bar = TablesToolBar(self.connection, self)

        self.table_list = QListWidget()
        self.table_list.setFont(QFont('Century Gothic', 14))
        self.table_list.itemDoubleClicked.connect(self.open_table_viewer)

        layout.addWidget(header)
        layout.addWidget(self.tool_bar)
        layout.addWidget(self.table_list)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.update_tables()

    def update_tables(self):
        self.table_list.clear()
        tables = self.fetch_tables()
        for table in tables:
            self.table_list.addItem(table[0])

    def fetch_tables(self):
        cursor = self.connection.cursor()
        cursor.execute(f"USE {self.database_name}")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        cursor.close()
        return tables

    def open_table_viewer(self, item):
        self.table_viewer = TableViewer(self.connection, self.database_name, item.text(), self.main_window)
        self.main_window.central_widget.addWidget(self.table_viewer)
        self.main_window.switch_widget(self.table_viewer)

class TableViewer(QWidget):
    def __init__(self, connection, database_name, table_name, main_window):
        super().__init__()
        self.connection = connection
        self.database_name = database_name
        self.table_name = table_name
        self.main_window = main_window
        self.setWindowTitle(f'{table_name} - {database_name}')
        self.setStyleSheet("background-color: white;")
        layout = QVBoxLayout()
        self.setLayout(layout)

        header = QLabel(f"{table_name} in {database_name}")
        header.setFont(QFont('Century Gothic', 24))
        header.setStyleSheet("color: navy;")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.tool_bar = TableContentToolBar(self.connection, self)

        self.table_widget = QTableWidget()
        self.table_widget.setFont(QFont('Century Gothic', 12))

        layout.addWidget(header)
        layout.addWidget(self.tool_bar)
        layout.addWidget(self.table_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.update_table()

    def update_table(self):
        data = self.fetch_table_data()
        if data:
            headers = data[0].keys()
            self.table_widget.setColumnCount(len(headers))
            self.table_widget.setHorizontalHeaderLabels(headers)
            self.table_widget.setRowCount(len(data))
            for row_idx, row_data in enumerate(data):
                for col_idx, col_data in enumerate(row_data.values()):
                    self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
            self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def fetch_table_data(self):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(f"USE {self.database_name}")
        cursor.execute(f"SELECT * FROM {self.table_name}")
        data = cursor.fetchall()
        cursor.close()
        return data

class DatabaseToolBar(QWidget):
    def __init__(self, connection, parent):
        super().__init__()
        self.connection = connection
        self.parent = parent
        self.setStyleSheet("background-color: white; border: 1px solid navy;")
        layout = QHBoxLayout()
        self.setLayout(layout)

        create_db_btn = QPushButton("Create Database")
        create_db_btn.setFont(QFont('Century Gothic', 14))
        create_db_btn.setStyleSheet("background-color: #2d388a; color: #00aeef;")
        create_db_btn.clicked.connect(self.create_database)

        rename_db_btn = QPushButton("Rename Database")
        rename_db_btn.setFont(QFont('Century Gothic', 14))
        rename_db_btn.setStyleSheet("background-color: #2d388a; color: #00aeef;")
        rename_db_btn.clicked.connect(self.rename_database)
        
        delete_db_btn = QPushButton("Delete Database")
        delete_db_btn.setFont(QFont('Century Gothic', 14))
        delete_db_btn.setStyleSheet("background-color: #2d388a; color: #00aeef;")
        delete_db_btn.clicked.connect(self.delete_database)

        go_back_btn = QPushButton("Go Back")
        go_back_btn.setFont(QFont('Century Gothic', 14))
        go_back_btn.setStyleSheet("background-color: #2d388a; color: #00aeef;")
        go_back_btn.clicked.connect(self.go_back)

        layout.addWidget(create_db_btn)
        layout.addWidget(rename_db_btn)
        layout.addWidget(delete_db_btn)
        layout.addWidget(go_back_btn)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    def create_database(self):
        text, ok = QInputDialog.getText(self, 'Create Database', 'Enter database name:')
        if ok and text:
            cursor = self.connection.cursor()
            cursor.execute(f"CREATE DATABASE {text}")
            self.connection.commit()
            cursor.close()
            self.parent.update_databases()

    def rename_database(self):
        current_db = self.parent.database_list.currentItem()
        if current_db:
            new_name, ok = QInputDialog.getText(self, 'Rename Database', 'Enter new database name:')
            if ok and new_name:
                cursor = self.connection.cursor()
                cursor.execute(f"RENAME DATABASE {current_db.text()} TO {new_name}")
                self.connection.commit()
                cursor.close()
                self.parent.update_databases()

    def delete_database(self):
        current_db = self.parent.database_list.currentItem()
        if current_db:
            reply = QMessageBox.question(self, 'Delete Database', f'Are you sure you want to delete {current_db.text()}?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                cursor = self.connection.cursor()
                cursor.execute(f"DROP DATABASE {current_db.text()}")
                self.connection.commit()
                cursor.close()
                self.parent.update_databases()

    def go_back(self):
        self.parent.main_window.switch_widget(self.parent.main_window.db_arena)

class TablesToolBar(QWidget):
    def __init__(self, connection, parent):
        super().__init__()
        self.connection = connection
        self.parent = parent
        self.setStyleSheet("background-color: white; border: 1px solid navy;")
        layout = QHBoxLayout()
        self.setLayout(layout)

        merge_table_btn = QPushButton("Merge Table")
        merge_table_btn.setFont(QFont('Century Gothic', 14))
        merge_table_btn.setStyleSheet("background-color: #2d388a; color: #00aeef;")
        merge_table_btn.clicked.connect(self.merge_table)

        rename_table_btn = QPushButton("Rename Table")
        rename_table_btn.setFont(QFont('Century Gothic', 14))
        rename_table_btn.setStyleSheet("background-color: #2d388a; color: #00aeef;")
        rename_table_btn.clicked.connect(self.rename_table)
        
        delete_table_btn = QPushButton("Delete Table")
        delete_table_btn.setFont(QFont('Century Gothic', 14))
        delete_table_btn.setStyleSheet("background-color: #2d388a; color: #00aeef;")
        delete_table_btn.clicked.connect(self.delete_table)

        go_back_btn = QPushButton("Go Back")
        go_back_btn.setFont(QFont('Century Gothic', 14))
        go_back_btn.setStyleSheet("background-color: #2d388a; color: #00aeef;")
        go_back_btn.clicked.connect(self.go_back)

        layout.addWidget(merge_table_btn)
        layout.addWidget(rename_table_btn)
        layout.addWidget(delete_table_btn)
        layout.addWidget(go_back_btn)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    def merge_table(self):
        # Implementation for merging tables
        pass

    def rename_table(self):
        if self.parent.table_list.currentItem():
            self.table_form = TableForm(self.connection, self.parent.database_name, 'rename', self.parent.table_list.currentItem().text())
            self.table_form.show()

    def delete_table(self):
        if self.parent.table_list.currentItem():
            table_name = self.parent.table_list.currentItem().text()
            reply = QMessageBox.question(self, 'Delete Table', f'Are you sure you want to delete {table_name}?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                cursor = self.connection.cursor()
                cursor.execute(f"USE {self.parent.database_name}")
                cursor.execute(f"DROP TABLE {table_name}")
                self.connection.commit()
                cursor.close()
                self.parent.update_tables()

    def go_back(self):
        self.parent.main_window.switch_widget(self.parent.main_window.db_arena)

class TableContentToolBar(QWidget):
    def __init__(self, connection, parent):
        super().__init__()
        self.connection = connection
        self.parent = parent
        self.setStyleSheet("background-color: white; border: 1px solid navy;")
        layout = QHBoxLayout()
        self.setLayout(layout)

        resize_btn = QPushButton("Resize")
        resize_btn.setFont(QFont('Century Gothic', 14))
        resize_btn.setStyleSheet("background-color: #2d388a; color: #00aeef;")
        resize_btn.clicked.connect(self.resize_columns)

        rename_column_btn = QPushButton("Rename Column")
        rename_column_btn.setFont(QFont('Century Gothic', 14))
        rename_column_btn.setStyleSheet("background-color: #2d388a; color: #00aeef;")
        rename_column_btn.clicked.connect(self.rename_column)
        
        visualize_table_btn = QPushButton("Visualize Table")
        visualize_table_btn.setFont(QFont('Century Gothic', 14))
        visualize_table_btn.setStyleSheet("background-color: #2d388a; color: #00aeef;")
        visualize_table_btn.clicked.connect(self.visualize_table)

        go_back_btn = QPushButton("Go Back")
        go_back_btn.setFont(QFont('Century Gothic', 14))
        go_back_btn.setStyleSheet("background-color: #2d388a; color: #00aeef;")
        go_back_btn.clicked.connect(self.go_back)

        layout.addWidget(resize_btn)
        layout.addWidget(rename_column_btn)
        layout.addWidget(visualize_table_btn)
        layout.addWidget(go_back_btn)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    def resize_columns(self):
        # Implementation for resizing columns
        pass

    def rename_column(self):
        # Implementation for renaming columns
        pass

    def visualize_table(self):
        reply = QMessageBox.question(self, 'Visualize Table', 'Do you want to visualize the entire table?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(f"USE {self.parent.database_name}")
            cursor.execute(f"SELECT * FROM {self.parent.table_name}")
            data = cursor.fetchall()
            cursor.close()

            if data:
                keys = data[0].keys()
                values = list(zip(*[d.values() for d in data]))

                plt.figure(figsize=(10, 6))
                for i, key in enumerate(keys):
                    plt.subplot(len(keys), 1, i + 1)
                    plt.hist(values[i], bins=20, color='blue', edgecolor='k', alpha=0.7)
                    plt.title(key)
                plt.tight_layout()
                plt.show()

    def go_back(self):
        self.parent.main_window.switch_widget(self.parent.main_window.db_arena)

class TableForm(QWidget):
    def __init__(self, connection, database_name, action, table_name=None):
        super().__init__()
        self.connection = connection
        self.database_name = database_name
        self.action = action
        self.table_name = table_name
        self.setWindowTitle(f'{action.capitalize()} Table - {database_name}')
        self.setFixedSize(400, 300)
        self.setStyleSheet("background-color: white;")
        layout = QVBoxLayout()
        self.setLayout(layout)

        form_layout = QFormLayout()
        self.table_name_input = QLineEdit()
        if action == 'rename' and table_name:
            self.table_name_input.setText(table_name)
        form_layout.addRow(QLabel('Table Name:'), self.table_name_input)

        self.columns_input = QLineEdit()
        form_layout.addRow(QLabel('Columns (name type, name type):'), self.columns_input)

        self.submit_btn = QPushButton('Submit')
        self.submit_btn.setFont(QFont('Century Gothic', 14))
        self.submit_btn.setStyleSheet("background-color: #2d388a; color: #00aeef;")
        self.submit_btn.clicked.connect(self.handle_submit)

        layout.addLayout(form_layout)
        layout.addWidget(self.submit_btn)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    def handle_submit(self):
        table_name = self.table_name_input.text()
        columns = self.columns_input.text()
        cursor = self.connection.cursor()
        cursor.execute(f"USE {self.database_name}")
        if self.action == 'create':
            cursor.execute(f"CREATE TABLE {table_name} ({columns})")
        elif self.action == 'rename' and self.table_name:
            cursor.execute(f"ALTER TABLE {self.table_name} RENAME TO {table_name}")
        self.connection.commit()
        cursor.close()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    loading_screen = LoadingScreen()
    loading_screen.show()
    sys.exit(app.exec())
