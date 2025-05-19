from PySide6.QtWidgets import (
    QMainWindow, QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QHBoxLayout, QPushButton, QWidget, QDialog, QMessageBox
)
from PySide6.QtCore import Qt


class FlatInfoWindow(QMainWindow):
    def __init__(self, cursor, connection, flat_id, parent=None):
        super().__init__(parent)
        self.cursor = cursor
        self.connection = connection
        self.flat_id = flat_id
        self.setWindowTitle("Квартира")
        self.resize(800, 500)

        self.setStyleSheet("""
    QWidget {
        background-color: #fdf6f0;
        color: #333333;
        font-family: 'Segoe UI', Arial;
        font-size: 14px;
    }
    QLabel {
        color: #333333;
        font-weight: bold;
        font-size: 16px;
    }
    QLineEdit, QComboBox, QDateTimeEdit {
        border: 1px solid #ccc;
        padding: 5px;
        border-radius: 4px;
        background-color: white;
        color: #333333;
    }
    QPushButton {
        background-color: #9e3a26;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 8px 16px;
        min-width: 90px;
    }
    QPushButton:hover {
        background-color: #7a3024;
    }
    QPushButton#secondary {
        background-color: #6b4423;
    }
    QPushButton#secondary:hover {
        background-color: #55331a;
    }
    QTableWidget {
        background-color: white;
        border: 1px solid #e0e0e0;
        gridline-color: #eee;
        selection-background-color: #f5dcdc;
        color: #333333;
    }
    QHeaderView::section {
        background-color: #8B5E3C;
        padding: 5px;
        border: 1px solid #7a4c2d;
        font-weight: bold;
        color: white;
    }
""")

        self.init_ui()
        self.load_flat_data()
        self.load_operation_data()

    def init_ui(self):
        container = QWidget()
        self.setCentralWidget(container)
        layout = QVBoxLayout()

        # Информация о квартире
        info_layout = QVBoxLayout()

        self.address_label = QLabel("")
        self.owner_label = QLabel("")
        self.storey_label = QLabel("")
        self.area_label = QLabel("")
        self.count_label = QLabel("")

        info_layout.addWidget(self.address_label)
        info_layout.addWidget(self.owner_label)
        info_layout.addWidget(self.storey_label)
        info_layout.addWidget(self.area_label)
        info_layout.addWidget(self.count_label)

        layout.addLayout(info_layout)
        layout.addSpacing(20)

        # Таблица с ремонтными работами
        self.operation_table = QTableWidget()
        self.operation_table.setColumnCount(4)
        self.operation_table.setHorizontalHeaderLabels(["Дата", "Тип работы", "ФИО работника", "Описание"])
        self.operation_table.setSortingEnabled(True)

        layout.addWidget(QLabel("Ремонтные работы:"))
        layout.addWidget(self.operation_table)

        # Кнопки
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        add_work_button = QPushButton("Добавить работу")
        add_work_button.clicked.connect(self.open_add_operation_window)

        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(self.return_to_flat_window)

        button_layout.addWidget(add_work_button)
        button_layout.addWidget(close_button)

        layout.addLayout(button_layout)
        container.setLayout(layout)

    def load_flat_data(self):
        try:
            query = """
            SELECT 
                f.txtFlatAddress,
                o.txtOwnerSurname + ' ' + o.txtOwnerName + ISNULL(' ' + o.txtOwnerSecondName, ''),
                f.intStorey,
                f.fltArea,
                f.intCount
            FROM tblFlat f
            INNER JOIN tblOwner o ON f.intOwnerId = o.intOwnerId
            WHERE f.intFlatId = ?
            """
            self.cursor.execute(query, (self.flat_id,))
            row = self.cursor.fetchone()

            if row:
                address, owner, storey, area, count = row
                self.address_label.setText(f"Адрес: {address}")
                self.owner_label.setText(f"Владелец: {owner}")
                self.storey_label.setText(f"Этаж: {storey}")
                self.area_label.setText(f"Площадь: {area} м²")
                self.count_label.setText(f"Количество жильцов: {count}")
        except Exception as e:
            print("Ошибка загрузки данных о квартире:", e)

    def load_operation_data(self):
        try:
            query = """
            SELECT 
                op.datOperationDate,
                ot.txtOperationTypeName,
                w.txtWorkerSurname + ' ' + w.txtWorkerName + ISNULL(' ' + w.txtWorkerSecondName, ''),
                op.txtOperationDescription
            FROM tblOperation op
            JOIN tblOperationType ot ON op.intOperationTypeId = ot.intOperationTypeId
            JOIN tblWorker w ON op.intWorkerId = w.intWorkerId
            WHERE op.intFlatId = ?
            ORDER BY op.datOperationDate DESC
            """
            self.cursor.execute(query, (self.flat_id,))
            rows = self.cursor.fetchall()

            self.operation_table.setRowCount(len(rows))
            for row_idx, row_data in enumerate(rows):
                for col_idx, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(str(cell_data))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.operation_table.setItem(row_idx, col_idx, item)

            self.operation_table.resizeColumnsToContents()

        except Exception as e:
            print("Ошибка загрузки данных о работах:", e)

    def open_add_operation_window(self):
        from new_operation_window import NewOperationWindow
        dialog = NewOperationWindow(self.cursor, self.connection, {'flat_id': self.flat_id}, parent=self)

        if dialog.exec() == QDialog.Accepted:
            QMessageBox.information(self, "Успех", "Работа успешно добавлена!")
            self.load_operation_data()
    def return_to_flat_window(self):
        
        if self.parent():  # если MainWindow передан как parent
            self.parent().show()  # показываем обратно главное окно
        self.close()