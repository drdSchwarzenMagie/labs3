from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QComboBox, QDialog
)
from PySide6.QtCore import Qt


class AddFlatWindow(QDialog):
    def __init__(self, cursor, connection, parent=None):
        super().__init__(parent)
        self.cursor = cursor
        self.connection = connection
        self.setWindowTitle("Новая квартира")
        self.setGeometry(200, 200, 400, 250)
        self.setWindowModality(Qt.ApplicationModal)

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
        self.load_owners()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        # Поле адреса квартиры
        self.address_input = QLineEdit()
        layout.addWidget(QLabel("Адрес квартиры:"))
        layout.addWidget(self.address_input)

        # Выбор владельца
        self.owner_combo = QComboBox()
        layout.addWidget(QLabel("Выберите владельца:"))
        layout.addWidget(self.owner_combo)

        # Этаж
        self.storey_input = QLineEdit()
        layout.addWidget(QLabel("Этаж:"))
        layout.addWidget(self.storey_input)

        # Площадь
        self.area_input = QLineEdit()
        layout.addWidget(QLabel("Площадь (м²):"))
        layout.addWidget(self.area_input)

        # Количество жильцов
        self.count_input = QLineEdit()
        layout.addWidget(QLabel("Количество жильцов:"))
        layout.addWidget(self.count_input)

        # Кнопки
        button_layout = QHBoxLayout()
        save_button = QPushButton("Сохранить")
        cancel_button = QPushButton("Отмена")

        save_button.clicked.connect(self.save_flat)
        cancel_button.clicked.connect(self.close)

        button_layout.addStretch()
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def load_owners(self):
        try:
            query = """
            SELECT intOwnerId, txtOwnerSurname + ' ' + txtOwnerName + ISNULL(' ' + txtOwnerSecondName, '') AS FullName
            FROM tblOwner
            ORDER BY txtOwnerSurname
            """
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            self.owner_combo.addItem("— Выберите владельца —", userData=None)
            for row in rows:
                owner_id = row[0]
                full_name = row[1]
                self.owner_combo.addItem(full_name, userData=owner_id)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить список владельцев:\n{e}")

    def save_flat(self):
        address = self.address_input.text().strip()
        owner_id = self.owner_combo.currentData()
        storey = self.storey_input.text().strip()
        area = self.area_input.text().strip()
        count = self.count_input.text().strip()

        if not all([address, owner_id is not None, storey, area, count]):
            QMessageBox.warning(self, "Ошибка", "Все поля обязательны для заполнения!")
            return

        try:
            storey = int(storey)
            area = float(area)
            count = int(count)

            if storey <= 0 or area <= 0 or count < 0:
                raise ValueError("Некорректные значения.")
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Проверьте корректность числовых значений.")
            return

        try:
            # Добавление квартиры
            self.cursor.execute(
                """
                INSERT INTO tblFlat 
                (txtFlatAddress, intOwnerId, fltArea, intCount, intStorey) 
                VALUES (?, ?, ?, ?, ?)
                """,
                (address, owner_id, area, count, storey)
            )
            self.connection.commit()

            QMessageBox.information(self, "Успех", "Квартира успешно добавлена!")
            self.close()

        except Exception as e:
            self.connection.rollback()
            QMessageBox.critical(self, "Ошибка базы данных", f"Не удалось сохранить данные:\n{e}")