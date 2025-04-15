import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton,
    QHBoxLayout
)
from PySide6.QtCore import Qt
from db_connection import *

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
    def __init__(self, cursor):
        super().__init__()
        self.cursor = cursor
        self.setWindowTitle("Квартиры")
        self.setGeometry(100, 100, 800, 400)

        # Применение глобальных стилей через CSS
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5; /* Цвет фона окна */
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #ccc;
                gridline-color: #ccc;
                font-size: 14px;
                selection-background-color: #d3eaff; /* Цвет выделенной строки */
            }
            QHeaderView::section {
                background-color: #e0e0e0;
                padding: 5px;
                border: 1px solid #ccc;
                font-weight: bold;
            }
            QPushButton {
                background-color: #007bff; /* Синяя кнопка */
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0056b3; /* Цвет при наведении */
            }
            QPushButton:disabled {
                background-color: #cccccc; /* Цвет неактивной кнопки */
                color: #666666;
            }
        """)

        # Создание виджетов
        self.table = QTableWidget(self)
        self.refresh_button = QPushButton("Обновить", self)
        self.add_flat_button = QPushButton("Добавить квартиру", self)
        self.add_flat_button.setEnabled(False)  # Кнопка пока не рабочая

        # Настройка кнопок
        self.refresh_button.clicked.connect(self.refresh_table)

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
        main_layout.addWidget(self.refresh_button, alignment=Qt.AlignLeft)

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
                self.table.setItem(row_idx, col_idx, item)

        # Настройка ширины столбцов
        self.table.resizeColumnsToContents()

# Основная функция для запуска приложения
if __name__ == "__main__":
    # Подключение к базе данных через SSH-туннель
    connection, cursor = connect_with_ssh_tunnel()

    # Создание приложения
    app = QApplication(sys.argv)
    window = MainWindow(cursor)
    window.show()

    # Запуск приложения
    exit_code = app.exec()

    # Закрытие соединения после завершения работы
    db_connection_close(connection, cursor)

    sys.exit(exit_code)