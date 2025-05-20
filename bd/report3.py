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

def generate_operation_report(operation_type_name):
    from db_connection import connect_with_ssh_tunnel, db_connection_close
    conn, cursor = connect_with_ssh_tunnel()

    query = """
    SELECT 
        ot.txtOperationTypeName AS OperationType,
        ot.fltOperationPrice AS Price,
        w.txtWorkerSurname + ' ' + w.txtWorkerName + ISNULL(' ' + w.txtWorkerSecondName, '') AS WorkerFullName,
        w.txtWorkerSpecialist AS Specialty,
        f.txtFlatAddress AS FlatAddress,
        o.datOperationDate AS OperationDate,
        o.txtOperationDescription AS Description
    FROM tblOperation o
    JOIN tblOperationType ot ON o.intOperationTypeId = ot.intOperationTypeId
    JOIN tblWorker w ON o.intWorkerId = w.intWorkerId
    JOIN tblFlat f ON o.intFlatId = f.intFlatId
    WHERE ot.txtOperationTypeName = ?
    ORDER BY o.datOperationDate DESC;
    """

    df = pd.read_sql(query, conn, params=[operation_type_name])

    if df.empty:
        print(f"Нет данных по работе '{operation_type_name}'")
        return

    doc = SimpleDocTemplate("Работа.pdf", pagesize=A4)
    elements = []

    # Заголовок отчёта
    operation_type = df.iloc[0]['OperationType']
    price = df.iloc[0]['Price']

    elements.append(Paragraph(f"<b>Наименование работы:</b> {operation_type}", styles["Bold"]))
    elements.append(Paragraph(f"<b>Стоимость:</b> {price:.2f} руб.", styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Список рабочих
    workers = df[['WorkerFullName', 'Specialty']].drop_duplicates()
    elements.append(Paragraph("<b>Рабочие, выполнявшие работу:</b>", styles["Bold"]))
    for _, worker_row in workers.iterrows():
        elements.append(Paragraph(f"- {worker_row['WorkerFullName']} ({worker_row['Specialty']})", styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Таблица квартир
    data = [["Адрес квартиры", "Дата", "Описание"]]
    for _, row in df.iterrows():
        data.append([
            row['FlatAddress'],
            row['OperationDate'].strftime('%d.%m.%Y'),
            row['Description']
        ])

    table = Table(data)
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVu'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table)

    # Сохранение PDF
    doc.build(elements)
    print("Отчет успешно создан: Работа.pdf")
    db_connection_close(conn, cursor)


if __name__ == "__main__":
    # Пример вызова
    generate_operation_report("Столярные работы")