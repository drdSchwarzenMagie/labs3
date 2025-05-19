from PySide6.QtWidgets import (
    QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QMessageBox
)
from PySide6.QtCore import Qt


class MainMenuWindow(QWidget):
    def __init__(self, cursor, connection, parent=None):
        super().__init__(parent)
        self.cursor = cursor
        self.connection = connection
        self.setWindowTitle("Главное меню")
        self.resize(400, 300)

        self.setStyleSheet("""
            QWidget {
                background-color: #fdf6f0;
                font-family: 'Segoe UI', Arial;
                font-size: 14px;
                color: #333333;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            QPushButton {
                background-color: #9e3a26;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #7a3024;
            }
            QComboBox {
                border: 1px solid #ccc;
                padding: 5px;
                border-radius: 4px;
                background-color: white;
                color: #333333;
            }
        """)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        # Заголовок
        title = QLabel("Главная форма")
        layout.addWidget(title, alignment=Qt.AlignCenter)

        # Кнопка "Квартиры"
        btn_flats = QPushButton("Квартиры")
        btn_flats.clicked.connect(self.open_flats_window)
        layout.addWidget(btn_flats)

        # Кнопка "Отчет 1: Все квартиры"
        btn_report1 = QPushButton("Отчет 1: Список квартир")
        btn_report1.clicked.connect(self.open_report_1)
        layout.addWidget(btn_report1)

        # Кнопка "Отчет 2: Все работы"
        btn_report2 = QPushButton("Отчет 2: Все работы")
        btn_report2.clicked.connect(self.open_report_2)
        layout.addWidget(btn_report2)

        # Выбор типа работ для отчета 3
        self.type_combo = QComboBox()
        self.load_operation_types()
        layout.addWidget(QLabel("Выберите тип работ:"))
        layout.addWidget(self.type_combo)

        # Кнопка "Отчет 3: Фильтр по типу работ"
        btn_report3 = QPushButton("Отчет 3: По типу работ")
        btn_report3.clicked.connect(self.open_report_3)
        layout.addWidget(btn_report3)

        self.setLayout(layout)

    def load_operation_types(self):
        try:
            query = """
            SELECT intOperationTypeId, txtOperationTypeName
            FROM tblOperationType
            ORDER BY txtOperationTypeName
            """
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            for row in rows:
                type_id = row[0]
                name = row[1]
                self.type_combo.addItem(name, userData=type_id)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить типы работ:\n{e}")

    def open_flats_window(self):
        from flat_info_window import FlatInfoWindow
        from flat import MainWindow

        self.flat = MainWindow(self.cursor, self.connection)
        self.flat.show()
        self.hide()  # Скрываем главное меню

    def open_report_1(self):
        from report_window import ReportWindow

        query = """
        SELECT 
            f.txtFlatAddress AS Адрес,
            o.txtOwnerSurname + ' ' + o.txtOwnerName + ISNULL(' ' + o.txtOwnerSecondName, '') AS Владелец,
            f.intStorey AS Этаж,
            f.fltArea AS Площадь,
            f.intCount AS Жильцов
        FROM tblFlat f
        INNER JOIN tblOwner o ON f.intOwnerId = o.intOwnerId
        """

        self.report_window = ReportWindow(self.cursor, query, "Отчет: Список квартир")
        self.report_window.show()

    def open_report_2(self):
        from report_window import ReportWindow

        query = """
        SELECT 
            f.txtFlatAddress AS Адрес,
            ot.txtOperationTypeName AS [Тип работы],
            op.datOperationDate AS Дата,
            w.txtWorkerSurname + ' ' + w.txtWorkerName AS Мастер,
            op.txtOperationDescription AS Описание
        FROM tblOperation op
        JOIN tblFlat f ON op.intFlatId = f.intFlatId
        JOIN tblOperationType ot ON op.intOperationTypeId = ot.intOperationTypeId
        JOIN tblWorker w ON op.intWorkerId = w.intWorkerId
        ORDER BY op.datOperationDate DESC
        """

        self.report_window = ReportWindow(self.cursor, query, "Отчет: Все ремонтные работы")
        self.report_window.show()

    def open_report_3(self):
        from report_window import ReportWindow

        type_id = self.type_combo.currentData()
        if not type_id:
            QMessageBox.warning(self, "Ошибка", "Выберите тип работы из списка.")
            return

        query = f"""
        SELECT 
            f.txtFlatAddress AS Адрес,
            ot.txtOperationTypeName AS [Тип работы],
            op.datOperationDate AS Дата,
            w.txtWorkerSurname + ' ' + w.txtWorkerName AS Мастер,
            op.txtOperationDescription AS Описание
        FROM tblOperation op
        JOIN tblFlat f ON op.intFlatId = f.intFlatId
        JOIN tblOperationType ot ON op.intOperationTypeId = ot.intOperationTypeId
        JOIN tblWorker w ON op.intWorkerId = w.intWorkerId
        WHERE ot.intOperationTypeId = {type_id}
        ORDER BY op.datOperationDate DESC
        """

        self.report_window = ReportWindow(self.cursor, query, "Отчет: Работы по типу")
        self.report_window.show()