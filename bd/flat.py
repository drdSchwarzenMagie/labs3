import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget,
    QPushButton, QHBoxLayout, QMessageBox
)
from PySide6.QtCore import Qt
from db_connection import connect_with_ssh_tunnel, db_connection_close
from add_flat_window import AddFlatWindow
from flat_info_window import FlatInfoWindow  # Импорт новой формы


# Функция для получения данных из базы данных
def fetch_flat_data(cursor):
    query = """
    SELECT 
        f.txtFlatAddress AS Address,
        o.txtOwnerSurname + ' ' + o.txtOwnerName + ' ' + ISNULL(o.txtOwnerSecondName, '') AS OwnerFullName,
        f.intStorey AS Storey,
        f.fltArea AS Area,
        f.intCount AS ResidentCount
    FROM 
        tblFlat f
    INNER JOIN 
        tblOwner o ON f.intOwnerId = o.intOwnerId
    """
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return []


# Главное окно приложения
class MainWindow(QMainWindow):
    def __init__(self, cursor, connection):
        super().__init__()
        self.cursor = cursor
        self.connection = connection
        self.setWindowTitle("Квартиры")
        self.setGeometry(100, 100, 800, 400)

        # Применение глобальных стилей через CSS
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

        # Создание виджетов
        self.table = QTableWidget(self)
        # self.refresh_button = QPushButton("Обновить", self)
        self.add_flat_button = QPushButton("Добавить квартиру", self)

        # Настройка кнопок
        # self.refresh_button.clicked.connect(self.refresh_table)
        self.add_flat_button.clicked.connect(self.open_add_flat_window)
        self.table.cellDoubleClicked.connect(self.on_cell_double_clicked)  # <-- Новый обработчик

        # Минимальная высота таблицы
        self.table.setMinimumHeight(300)

        # Макет для таблицы и кнопки "Добавить квартиру"
        table_container_layout = QVBoxLayout()

        # Добавляем таблицу
        table_container_layout.addWidget(self.table)

        # Горизонтальный макет для кнопки "Добавить квартиру"
        button_layout = QHBoxLayout()
        button_layout.addStretch()  # Растяжение слева
        button_layout.addWidget(self.add_flat_button)

        # Добавляем кнопку в контейнер
        table_container_layout.addLayout(button_layout)

        # Основной макет
        main_layout = QHBoxLayout()

        # Добавляем кнопку "Обновить" слева
        # main_layout.addWidget(self.refresh_button, alignment=Qt.AlignLeft)

        # Добавляем контейнер с таблицей и кнопкой "Добавить квартиру" справа
        main_layout.addLayout(table_container_layout, stretch=1)

        # Установка макета в контейнер
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Первоначальное заполнение таблицы
        self.refresh_table()

    # Обновление данных в таблице
    def refresh_table(self):
        data = fetch_flat_data(self.cursor)
        if not data:
            return

        # Очистка таблицы
        self.table.clear()

        # Установка заголовков
        headers = ["Адрес", "ФИО владельца", "Этаж", "Площадь", "Количество жильцов"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        # Заполнение данными
        self.table.setRowCount(len(data))
        for row_idx, row_data in enumerate(data):
            for col_idx, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # Только для чтения
                item.setForeground(Qt.black)  # Явно установить цвет текста
                self.table.setItem(row_idx, col_idx, item)

        # Настройка ширины столбцов
        self.table.resizeColumnsToContents()

    # Открытие формы добавления квартиры
    def open_add_flat_window(self):
        self.add_window = AddFlatWindow(self.cursor, self.connection, self)
        self.add_window.show()

    # Обработка двойного клика на ячейке
    def on_cell_double_clicked(self, row, column):
        headers = ["Адрес", "ФИО владельца", "Этаж", "Площадь", "Количество жильцов"]
        if headers[column] == "Адрес":
            address_item = self.table.item(row, 0)
            if address_item:
                flat_address = address_item.text()
                # Получаем intFlatId по адресу
                try:
                    self.cursor.execute("SELECT intFlatId FROM tblFlat WHERE txtFlatAddress = ?", (flat_address,))
                    result = self.cursor.fetchone()
                    if result:
                        flat_id = result[0]
                        self.open_flat_info_window(flat_id)
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось получить ID квартиры:\n{e}")

    # Открытие формы просмотра информации о квартире
    def open_flat_info_window(self, flat_id):
        self.flat_info_window = FlatInfoWindow(self.cursor, self.connection, flat_id, parent=None)
        self.flat_info_window.show()


# Основная функция для запуска приложения
if __name__ == "__main__":
    # Подключение к базе данных через SSH-туннель
    connection, cursor = connect_with_ssh_tunnel()

    # Создание приложения
    app = QApplication(sys.argv)
    window = MainWindow(cursor, connection)
    window.show()

    # Запуск приложения
    exit_code = app.exec()

    # Закрытие соединения после завершения работы
    db_connection_close(connection, cursor)

    sys.exit(exit_code)