from PySide6.QtWidgets import (
    QDialog, QLabel, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout,
    QMessageBox, QDateTimeEdit, QFormLayout, QLineEdit
)
from PySide6.QtCore import Qt, QDateTime, QDate


class NewOperationWindow(QDialog):
    def __init__(self, cursor, connection, flat_info, parent=None):
        super().__init__(parent)
        self.cursor = cursor
        self.connection = connection
        self.flat_id = flat_info['flat_id']
        self.setWindowTitle("Новая работа")
        self.resize(500, 400)

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
        self.load_workers()
        self.load_operation_types()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Информация о квартире (только для чтения)
        info_group = QVBoxLayout()
        self.address_label = QLabel(f"<b>Адрес:</b> {self.parent().address_label.text()}")
        self.owner_label = QLabel(f"<b>Владелец:</b> {self.parent().owner_label.text()}")
        self.area_label = QLabel(f"<b>Площадь:</b> {self.parent().area_label.text()}")

        self.address_label.setStyleSheet("font-size: 18px;")
        self.owner_label.setStyleSheet("font-size: 18px;")
        self.area_label.setStyleSheet("font-size: 18px;")

        info_group.addWidget(self.address_label)
        info_group.addWidget(self.owner_label)
        info_group.addWidget(self.area_label)

        layout.addLayout(info_group)
        layout.addSpacing(20)

        # Форма данных
        form_layout = QFormLayout()

        # Дата проведения работ
        self.date_edit = QDateTimeEdit(date=QDate.currentDate(), calendarPopup=True)
        self.date_edit.setDisplayFormat("dd-MM-yyyy")  # Можно использовать "dd.MM.yyyy" или другой формат
        self.date_edit.setDateRange(QDate(1, 1, 2000), QDate(31, 12, 2100))
        self.date_edit.setDateTime(QDateTime.currentDateTime())
        form_layout.addRow("Дата проведения работ:", self.date_edit)

        # Тип работ
        self.type_combo = QComboBox()
        form_layout.addRow("Тип работ:", self.type_combo)

        # Рабочий
        self.worker_combo = QComboBox()
        form_layout.addRow("ФИО рабочего:", self.worker_combo)

        # Описание работы
        self.description_input = QLineEdit()
        form_layout.addRow("Описание работы:", self.description_input)

        layout.addLayout(form_layout)

        # Кнопки
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        save_button = QPushButton("Сохранить")
        cancel_button = QPushButton("Отмена")

        save_button.clicked.connect(self.save_operation)
        cancel_button.clicked.connect(self.reject)  # закрытие диалога без сохранения

        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

    def load_workers(self):
        try:
            query = """
            SELECT intWorkerId, txtWorkerSurname + ' ' + txtWorkerName + ISNULL(' ' + txtWorkerSecondName, '') AS FullName
            FROM tblWorker
            ORDER BY txtWorkerSurname
            """
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            for row in rows:
                worker_id = row[0]
                full_name = row[1]
                self.worker_combo.addItem(full_name, userData=worker_id)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить список рабочих:\n{e}")

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

    def save_operation(self):
        date = self.date_edit.dateTime().toString("yyyy-MM-dd")
        type_id = self.type_combo.currentData()
        worker_id = self.worker_combo.currentData()
        description = self.description_input.text().strip()

        if not all([type_id is not None, worker_id is not None]):
            QMessageBox.warning(self, "Ошибка", "Выберите тип работы и рабочего.")
            return

        try:
            query = """
            INSERT INTO tblOperation 
            (intFlatId, intOperationTypeId, datOperationDate, intWorkerId, txtOperationDescription)
            VALUES (?, ?, ?, ?, ?)
            """
            self.cursor.execute(query, (self.flat_id, type_id, date, worker_id, description or None))
            self.connection.commit()
            self.accept()  # Закрываем диалог как успешный
        except Exception as e:
            self.connection.rollback()
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить данные:\n{e}")