import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Регистрация шрифта с поддержкой кириллицы
pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSerif.ttf'))

# Стили
styles = {
    "Normal": ParagraphStyle(
        name='Normal',
        fontName='DejaVu',
        fontSize=12,
        leading=14,
        textColor=colors.black
    ),
    "Bold": ParagraphStyle(
        name='Bold',
        fontName='DejaVu',
        fontSize=12,
        fontWeight='bold',
        textColor=colors.black
    )
}

def generate_repair_report():
    from db_connection import connect_with_ssh_tunnel, db_connection_close
    conn, cursor = connect_with_ssh_tunnel()

    query = """
    SELECT 
        f.txtFlatAddress AS FlatAddress,
        o.txtOwnerSurname + ' ' + o.txtOwnerName + ISNULL(' ' + o.txtOwnerSecondName, '') AS OwnerFullName,
        f.fltArea AS Area,
        f.intCount AS ResidentCount,
        ot.txtOperationTypeName AS OperationType,
        ot.fltOperationPrice AS Price,
        op.datOperationDate AS OperationDate,
        op.txtOperationDescription AS Description,
        w.txtWorkerSurname + ' ' + w.txtWorkerName + ISNULL(' ' + w.txtWorkerSecondName, '') AS WorkerFullName
    FROM tblFlat f
    JOIN tblOwner o ON f.intOwnerId = o.intOwnerId
    LEFT JOIN tblOperation op ON f.intFlatId = op.intFlatId
    LEFT JOIN tblOperationType ot ON op.intOperationTypeId = ot.intOperationTypeId
    LEFT JOIN tblWorker w ON op.intWorkerId = w.intWorkerId
    ORDER BY f.intFlatId, ot.txtOperationTypeName, op.datOperationDate DESC;
    """

    df = pd.read_sql(query, conn)

    doc = SimpleDocTemplate("Ремонт.pdf", pagesize=A4)
    elements = []

    current_flat_id = None
    flat_data = {}
    operation_type_counter = {}

    for index, row in df.iterrows():
        flat_address = row['FlatAddress']

        if flat_address != current_flat_id:
            # Начало новой квартиры
            current_flat_id = flat_address
            flat_data = {
                'OwnerFullName': row['OwnerFullName'],
                'Area': row['Area'],
                'ResidentCount': row['ResidentCount']
            }
            total_price = 0
            operation_type_counter = {}  # Сброс счетчика по типам работ

            elements.append(Paragraph(f"<b>Адрес:</b> {flat_address}", styles["Normal"]))
            elements.append(Paragraph(f"<b>ФИО владельца:</b> {flat_data['OwnerFullName']}", styles["Normal"]))
            elements.append(Paragraph(f"<b>Площадь:</b> {flat_data['Area']} м²", styles["Normal"]))
            elements.append(Paragraph(f"<b>Количество проживающих:</b> {flat_data['ResidentCount']}", styles["Normal"]))
            elements.append(Spacer(1, 12))

        # Если есть данные о работе
        if pd.notna(row['OperationType']):
            op_type = row['OperationType']
            price = row['Price']
            date = row['OperationDate'].strftime('%d.%m.%Y') if pd.notna(row['OperationDate']) else ''
            desc = row['Description']
            worker = row['WorkerFullName']

            # Подсчет общей суммы и количества по типу
            if op_type not in operation_type_counter:
                operation_type_counter[op_type] = {'count': 0, 'price': price}
            operation_type_counter[op_type]['count'] += 1

            # Вывод заголовка типа работы
            if operation_type_counter[op_type]['count'] == 1:
                elements.append(Paragraph(f"<b>Тип работы:</b> {op_type}", styles["Bold"]))
                elements.append(Paragraph(f"<b>Стоимость:</b> {price:.2f} руб.", styles["Normal"]))
                elements.append(Spacer(1, 6))

            # Добавляем строку операции
            data = [["Дата", "Описание", "Рабочий"]]
            data.append([date, desc, worker])

            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('FONTNAME', (0, 0), (-1, -1), 'DejaVu'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(table)
            elements.append(Spacer(1, 6))

            # Вывод количества по типу работы
            if operation_type_counter[op_type]['count'] > 1 and list(operation_type_counter.keys()).index(op_type) == list(operation_type_counter.keys()).index(op_type):
                elements.pop()  # Убираем повторяющийся стиль таблицы
                elements.append(Paragraph(f"Количество работ '{op_type}': {operation_type_counter[op_type]['count']}", styles["Normal"]))
                elements.append(HRFlowable(width="100%", thickness=1, color=colors.black))
                elements.append(Spacer(1, 12))

            # Общая сумма
            total_price += price

        # Конец квартиры — вывод общей стоимости
        if df[df['FlatAddress'] == flat_address].iloc[-1].name == index:
            elements.append(Paragraph(f"<b>Общая сумма:</b> {total_price:.2f} руб.", styles["Bold"]))
            elements.append(HRFlowable(width="100%", thickness=1, color=colors.black))
            elements.append(Spacer(1, 12))

    # Сохранение PDF
    doc.build(elements)
    print("Отчет успешно создан: Ремонт.pdf")
    db_connection_close(conn, cursor)


if __name__ == "__main__":
    generate_repair_report()