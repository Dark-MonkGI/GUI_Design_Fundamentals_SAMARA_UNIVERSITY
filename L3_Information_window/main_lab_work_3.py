import os
import sys
import PyQt6

import traceback

from PyQt6.QtCore import QThread
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenuBar, QStatusBar, QWidget, QPushButton, QLabel,  QComboBox, \
    QTabWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# WINDOW PARAMS
MIN_WINDOW_WIDTH = 1050
MIN_WINDOW_HEIGHT = 500
WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 750
WINDOW_TITLE = 'Airplanes'
DB_STATUS = 'Состояние подключения к БД: '
DB = os.path.join(os.path.dirname(__file__), 'AIR_DATA_BASE.db')

class AIRPLANES(Base):
    '''Конструктор класса таблица'''
    __tablename__ = 'airplanes'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    capacity = Column(String(50))
    distance = Column(String(50))
    year = Column(String(50))

    def init(self, id, name, capacity, distance, year):
        self.id = id
        self.name = name
        self.capacity = capacity
        self.distance = distance
        self.year = year

class QueryRunner(QThread):
    '''Запрос к БД'''
    def __init__(self, query, parent=None):
        super(QueryRunner, self).__init__(parent)
        self.query = query
        return 
    
    def run(self):
        self.query.exec()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle(WINDOW_TITLE)
        self.setMinimumWidth(MIN_WINDOW_WIDTH)
        self.setMinimumHeight(MIN_WINDOW_HEIGHT)
        self.setBaseSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Main Menu Widget
        self.main_menu = QMenuBar()
        self.setMenuBar(self.main_menu)
        # FILE SubMenu
        m = self.main_menu.addMenu("Файл")
        self.exit_action = m.addAction("Выход")
        # DB SubMenu
        m = self.main_menu.addMenu("База данных")
        self.set_connetcion_action = m.addAction("Подключиться")
        self.close_connetcion_action = m.addAction("Отключиться")
        self.close_connetcion_action.setEnabled(False)
        
        # Main Menu Action
        self.exit_action.triggered.connect(self.exit_app)
        self.set_connetcion_action.triggered.connect(self.connect_db)
        self.close_connetcion_action.triggered.connect(self.disconnect_db)

        # Main Window Widget 
        self.main_widget = QWidget()
        # Main Window Layouts
        self.grid_layout = QGridLayout()
        self.hbox_layout = QHBoxLayout()
        self.vbox_layout = QVBoxLayout()

        # Query Buttons
        self.query1_button = QPushButton()
        self.query3_button = QPushButton()
        self.query4_button = QPushButton()
        
        self.query1_button.setText("Получить названия самолетов")
        self.query3_button.setText("Получить значения distance")
        self.query4_button.setText("Получить значения capacity")

        self.query1_button.setEnabled(False)
        self.query3_button.setEnabled(False)
        self.query4_button.setEnabled(False)
    
        # Query Buttons Action
        self.query1_button.clicked.connect(self.get_name)
        self.query3_button.clicked.connect(self.get_dis)
        self.query4_button.clicked.connect(self.get_capacity)

        # Query Conmbo Box
        self.query2_combobox = QComboBox()
        self.query2_combobox.addItems([''])
        self.query2_combobox.setEnabled(False)

        # Query Conmbo Box Action
        self.query2_combobox.currentIndexChanged.connect(self.combobox_selection_change)

        # Tab Widget
        self.tab = QTabWidget()
        self.record_list = []

        self.is_construct = False

        self.tab_full_table = QTableWidget() 
        self.tab_full = 'Результат полной выборки &1'
        self.construct_table('FULL')

        self.tab_name_table = QTableWidget() 
        self.tab_name = 'Результат с названиями самолетов &2'
        self.construct_table('NAME')

        self.tab_model_table = QTableWidget()
        self.tab_model = 'Результат по моделям &3'
        self.construct_table('MODEL')
        
        self.tab_dis_table = QTableWidget()
        self.tab_dis = 'Максимальная дистанция &4'
        self.construct_table('DISTANCE')

        self.tab_capacity_table = QTableWidget()
        self.tab_capacity = 'Кол-во пассажиров &5'
        self.construct_table('CAPACITY')

        self.tab.setCurrentIndex(0)

        # Status Bar Widget
        self.db_state_label = QLabel()
        self.db_state_value = QLabel()
        self.status_bar = QStatusBar()
        self.status_bar.showMessage(DB_STATUS + 'Соединение отсутсвует')
    
        # Construct Layouts
        self.grid_layout.addWidget(self.query1_button, 0, 0)
        self.grid_layout.addWidget(self.query2_combobox, 0, 1)
        self.grid_layout.addWidget(self.query3_button, 1, 0)
        self.grid_layout.addWidget(self.query4_button, 1, 1)
        self.grid_layout.addWidget(self.query4_button, 1, 1)
        self.hbox_layout.addWidget(self.tab)
        
        self.vbox_layout.addItem(self.grid_layout)
        
        self.vbox_layout.addItem(self.hbox_layout)
        self.vbox_layout.addWidget(self.status_bar)

        self.main_widget.setLayout(self.vbox_layout)
        self.setCentralWidget(self.main_widget)

    def connect_db(self):
        self.is_construct = True
        self.set_connetcion_action.setEnabled(False)
        self.close_connetcion_action.setEnabled(True)
        self.query1_button.setEnabled(True)
        self.query2_combobox.setEnabled(True)
        self.query3_button.setEnabled(True)
        self.query4_button.setEnabled(True)
        self.engine = create_engine(f'sqlite:///' + DB , echo=False) 
        # Проверка существоания таблицы
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        try:
            self.record_list = self.session.query(AIRPLANES).all()
        except Exception:
            traceback.print_exc()
            return None

        items = []
        for r, data in enumerate(self.record_list):
            items += [data.name]
        
        self.query2_combobox.addItems(items)
        self.query2_combobox.setCurrentText('')
        self.query2_combobox.removeItem(self.query2_combobox.currentIndex())
        self.construct_table('FULL')
        self.is_construct = False
        self.status_bar.showMessage(DB_STATUS + 'Подключено')

    def disconnect_db(self):
        self.session.close()
        self.engine.dispose()
        self.status_bar.showMessage(DB_STATUS + 'Отсутсвует')
        self.set_connetcion_action.setEnabled(True)
        self.close_connetcion_action.setEnabled(False)
        self.query1_button.setEnabled(False)
        self.query2_combobox.setEnabled(False)
        self.query3_button.setEnabled(False)
        self.query4_button.setEnabled(False)

        while self.query2_combobox.count() > 0:
            self.query2_combobox.removeItem(0)

        self.query2_combobox.addItems([''])

        self.record_list = []
        self.construct_table('FULL')
        self.construct_table('NAME')
        self.construct_table('MODEL')
        self.construct_table('DISTANCE')
        self.construct_table('CAPACITY')
        
        self.tab.setCurrentIndex(0)

    def combobox_selection_change(self, i):
        if self.is_construct == False: 
            self.record_list = self.session.query(AIRPLANES).filter_by(name=self.query2_combobox.currentText()).all()
            self.construct_table('MODEL')

    def get_name(self):
        if self.is_construct == False: 
            self.record_list = self.session.query(AIRPLANES).all()
            self.construct_table('NAME')

    def get_dis(self):
        if self.is_construct == False: 
            self.record_list = self.session.query(AIRPLANES).all()
            self.construct_table('DISTANCE')

    def get_capacity(self):
        if self.is_construct == False: 
            self.record_list = self.session.query(AIRPLANES).all()
            self.construct_table('CAPACITY')

    def construct_table(self, type):
        header_row = []
        header_id = 0
        idx_tab = 0
        tab_description = ''

        if type == 'FULL':
            idx_tab = 0
            tab_description = self.tab_full
            headers = ['ID', 'NAME', 'CAPACITY', 'DISTANCE', 'YEAR']
            self.tab_full_table = QTableWidget()
            self.tab_full_table.setColumnCount(len(headers))

            for h in headers:
                header_row.append(self.tab_full_table.setHorizontalHeaderItem(header_id, QTableWidgetItem(h)))
                header_id += 1

            if len(self.record_list) > 0:
                for row_i, single_data in enumerate(self.record_list):
                    self.tab_full_table.setRowCount(self.tab_full_table.rowCount()+1)
                    self.tab_full_table.setRowHeight(self.tab_full_table.rowCount()-1, 30)
                    id = QTableWidgetItem(str(single_data.id))
                    self.tab_full_table.setItem(row_i, 0, id)
                    name = QTableWidgetItem(single_data.name)
                    self.tab_full_table.setItem(row_i, 1, name)
                    capacity = QTableWidgetItem(str(single_data.capacity))
                    self.tab_full_table.setItem(row_i, 2, capacity)
                    distance = QTableWidgetItem(single_data.distance)
                    self.tab_full_table.setItem(row_i, 3, distance)
                    year = QTableWidgetItem(str(single_data.year))
                    self.tab_full_table.setItem(row_i, 4, year)

            if len(self.record_list) > 0 or self.is_construct == False:
                self.tab.removeTab(idx_tab)
                self.tab.insertTab(idx_tab, self.tab_full_table, tab_description)
            else:
                self.tab.addTab(self.tab_full_table, self.tab_full)

            self.tab.setCurrentIndex(idx_tab)

        elif type == 'NAME':
            idx_tab = 1
            tab_description = self.tab_name
            headers = ['ID', 'NAME']            
            self.tab_name_table = QTableWidget()
            self.tab_name_table.setColumnCount(len(headers))
            for h in headers:
                header_row.append(self.tab_name_table.setHorizontalHeaderItem(header_id, QTableWidgetItem(h)))
                header_id += 1

            if len(self.record_list) > 0:
                for row_i, single_data in enumerate(self.record_list):
                    self.tab_name_table.setRowCount(self.tab_name_table.rowCount()+1)
                    self.tab_name_table.setRowHeight(self.tab_name_table.rowCount()-1, 30)
                    id = QTableWidgetItem(str(single_data.id))
                    self.tab_name_table.setItem(row_i, 0, id)
                    name = QTableWidgetItem(single_data.name)
                    self.tab_name_table.setItem(row_i, 1, name)

            if self.is_construct == False:
                self.tab.removeTab(idx_tab)
                self.tab.insertTab(idx_tab, self.tab_name_table, tab_description)
            else:
                self.tab.addTab(self.tab_name_table, self.tab_name)

            self.tab.setCurrentIndex(idx_tab)

        elif type == 'MODEL':
            idx_tab = 2
            tab_description = self.tab_model
            headers = ['ID', 'NAME', 'CAPACITY', 'DISTANCE', 'YEAR']
            self.tab_model_table = QTableWidget()
            self.tab_model_table.setColumnCount(len(headers))
            for h in headers:
                header_row.append(self.tab_model_table.setHorizontalHeaderItem(header_id, QTableWidgetItem(h)))
                header_id += 1
            
            if len(self.record_list) > 0:
                for row_i, single_data in enumerate(self.record_list):
                    self.tab_model_table.setRowCount(self.tab_model_table.rowCount() + 1)
                    self.tab_model_table.setRowHeight(self.tab_model_table.rowCount() - 1, 30)
                    id = QTableWidgetItem(str(single_data.id))
                    self.tab_model_table.setItem(row_i, 0, id)
                    name = QTableWidgetItem(single_data.name)
                    self.tab_model_table.setItem(row_i, 1, name)
                    capacity = QTableWidgetItem(str(single_data.capacity))
                    self.tab_model_table.setItem(row_i, 2, capacity)
                    distance = QTableWidgetItem(single_data.distance)
                    self.tab_model_table.setItem(row_i, 3, distance)
                    year = QTableWidgetItem(str(single_data.year))
                    self.tab_model_table.setItem(row_i, 4, year)

            if self.is_construct == False:
                self.tab.removeTab(idx_tab)
                self.tab.insertTab(idx_tab, self.tab_model_table, tab_description)
            else:
                self.tab.addTab(self.tab_model_table, self.tab_model)

            self.tab.setCurrentIndex(idx_tab)

        elif type == 'DISTANCE':
            idx_tab = 3
            tab_description = self.tab_dis
            headers = ['ID', 'NAME', 'DISTANCE']
            self.tab_dis_table = QTableWidget()
            self.tab_dis_table.setColumnCount(len(headers))
            for h in headers:
                header_row.append(self.tab_dis_table.setHorizontalHeaderItem(header_id, QTableWidgetItem(h)))
                header_id += 1

            if len(self.record_list) > 0:
                for row_i, single_data in enumerate(self.record_list):
                    self.tab_dis_table.setRowCount(self.tab_dis_table.rowCount() + 1)
                    self.tab_dis_table.setRowHeight(self.tab_dis_table.rowCount() - 1, 30)
                    id = QTableWidgetItem(str(single_data.id))
                    self.tab_dis_table.setItem(row_i, 0, id)
                    name = QTableWidgetItem(single_data.name)
                    self.tab_dis_table.setItem(row_i, 1, name)
                    distance = QTableWidgetItem(single_data.distance)
                    self.tab_dis_table.setItem(row_i, 2, distance)

            if self.is_construct == False:
                self.tab.removeTab(idx_tab)
                self.tab.insertTab(idx_tab, self.tab_dis_table, tab_description)
            else:
                self.tab.addTab(self.tab_dis_table, self.tab_dis)

            self.tab.setCurrentIndex(idx_tab)

        elif type == 'CAPACITY':
            idx_tab = 4
            tab_description = self.tab_capacity
            headers = ['ID', 'NAME', 'CAPACITY']
            self.tab_capacity_table = QTableWidget()
            self.tab_capacity_table.setColumnCount(len(headers))
            for h in headers:
                header_row.append(self.tab_capacity_table.setHorizontalHeaderItem(header_id, QTableWidgetItem(h)))
                header_id += 1

            if len(self.record_list) > 0:
                for row_i, single_data in enumerate(self.record_list):
                    self.tab_capacity_table.setRowCount(self.tab_capacity_table.rowCount() + 1)
                    self.tab_dis_table.setRowHeight(self.tab_capacity_table.rowCount() - 1, 30)
                    id = QTableWidgetItem(str(single_data.id))
                    self.tab_capacity_table.setItem(row_i, 0, id)
                    name = QTableWidgetItem(single_data.name)
                    self.tab_capacity_table.setItem(row_i, 1, name)
                    capacity = QTableWidgetItem(single_data.capacity)
                    self.tab_capacity_table.setItem(row_i, 2, capacity)

            if self.is_construct == False:
                self.tab.removeTab(idx_tab)
                self.tab.insertTab(idx_tab, self.tab_capacity_table, tab_description)
            else:
                self.tab.addTab(self.tab_capacity_table, self.tab_capacity)

            self.tab.setCurrentIndex(idx_tab)

    def exit_app(self):
        application.quit()

if __name__ == '__main__':
    pyqt = os.path.dirname(PyQt6.__file__)
    QApplication.addLibraryPath(os.path.join(pyqt, "Qt", "plugins"))
    application = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(application.exec())