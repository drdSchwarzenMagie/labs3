import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Регистрация шрифта DejaVuSerif.ttf
pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSerif.ttf'))  # Убедись, что файл лежит рядом

# Создание пользовательских стилей на основе нового шрифта
styles = {
    "Normal": ParagraphStyle(
        name='Normal',
        fontName='DejaVu',
        fontSize=12,
        leading=14,
        textColor=colors.black
    ),
    "Heading1": ParagraphStyle(
        name='Heading1',
        fontName='DejaVu',
        fontSize=14,
        fontWeight='bold',
        textColor=colors.black
    )
}


def generate_workers_report():
    # Подключение к БД и получение данных — твой SQL-запрос
    from db_connection import connect_with_ssh_tunnel, db_connection_close
    conn, cursor = connect_with_ssh_tunnel()

    query = """
    SELECT 
        w.intWorkerId,
        w.txtWorkerSurname + ' ' + w.txtWorkerName + ISNULL(' ' + w.txtWorkerSecondName, '') AS FullName,
        w.txtWorkerSpecialist AS Specialty,
        o.datOperationDate AS Date,
        ot.txtOperationTypeName AS OperationType,
        f.txtFlatAddress AS FlatAddress,
        ot.fltOperationPrice AS Price
    FROM tblWorker w
    LEFT JOIN tblOperation o ON w.intWorkerId = o.intWorkerId
    LEFT JOIN tblOperationType ot ON o.intOperationTypeId = ot.intOperationTypeId
    LEFT JOIN tblFlat f ON o.intFlatId = f.intFlatId
    ORDER BY w.intWorkerId, o.datOperationDate DESC
    """

    df = pd.read_sql(query, conn)

    doc = SimpleDocTemplate("Рабочие.pdf", pagesize=A4)
    elements = []

    worker_ids_done = set()
    workers_count = 0

    for index, row in df.iterrows():
        worker_id = row['intWorkerId']

        if worker_id not in worker_ids_done:
            worker_ids_done.add(worker_id)
            workers_count += 1

            full_name = row['FullName']
            specialty = row['Specialty']

            worker_data = df[df['intWorkerId'] == worker_id]
            total_price = worker_data['Price'].sum()
            operations_count = len(worker_data)

            # Добавляем данные
            elements.append(Paragraph(f"<b>ФИО:</b> {full_name}", styles["Normal"]))
            elements.append(Paragraph(f"<b>Специальность:</b> {specialty}", styles["Normal"]))
            elements.append(Paragraph(f"<b>Общая сумма за работы:</b> {total_price:.2f} руб.", styles["Normal"]))
            elements.append(Spacer(1, 12))

            # Таблица операций
            data = [["Тип работы", "Адрес квартиры", "Дата", "Стоимость"]]
            for _, op_row in worker_data.iterrows():
                data.append([
                    op_row['OperationType'],
                    op_row['FlatAddress'],
                    op_row['Date'].strftime('%d.%m.%Y') if pd.notna(op_row['Date']) else '',
                    f"{op_row['Price']:.2f}" if pd.notna(op_row['Price']) else ''
                ])

            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 0), (-1, -1), 'DejaVu'), 
            ]))
            elements.append(table)
            elements.append(Spacer(1, 12))

            elements.append(Paragraph(f"<b>Количество выполненных работ:</b> {operations_count}", styles["Normal"]))
            elements.append(Paragraph(f"<b>Итого сумма:</b> {total_price:.2f} руб.", styles["Normal"]))
            elements.append(HRFlowable(width="100%", thickness=1, color=colors.black))
            elements.append(Spacer(1, 12))

    elements.append(Paragraph(f"<b>Всего рабочих в отчёте:</b> {workers_count}", styles["Normal"]))

    doc.build(elements)
    print("Отчет успешно создан: Рабочие.pdf")

    db_connection_close(conn, cursor)


if __name__ == "__main__":
    generate_workers_report()