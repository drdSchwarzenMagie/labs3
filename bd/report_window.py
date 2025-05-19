from PySide6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt


class ReportWindow(QWidget):
    def __init__(self, cursor, query, title, parent=None):
        super().__init__(parent)
        self.cursor = cursor
        self.query = query
        self.setWindowTitle(title)
        self.resize(800, 400)

        self.setStyleSheet("""
            QWidget {
                background-color: #fdf6f0;
                font-family: 'Segoe UI', Arial;
                font-size: 14px;
                color: #333333;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #ccc;
                gridline-color: #eee;
                selection-background-color: #f5dcdc;
            }
            QHeaderView::section {
                background-color: #8B5E3C;
                color: white;
                padding: 5px;
                border: 1px solid #7a4c2d;
                font-weight: bold;
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
        """)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.table = QTableWidget()
        layout.addWidget(self.table)

        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button, alignment=Qt.AlignRight)

        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        try:
            self.cursor.execute(self.query)
            rows = self.cursor.fetchall()
            if not rows:
                return

            self.table.setColumnCount(len(rows[0]))
            self.table.setHorizontalHeaderLabels([desc[0] for desc in self.cursor.description])
            self.table.setRowCount(len(rows))

            for row_idx, row_data in enumerate(rows):
                for col_idx, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(str(cell_data))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.table.setItem(row_idx, col_idx, item)

            self.table.resizeColumnsToContents()

        except Exception as e:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные отчёта:\n{e}")