import database
import xlsxwriter

id_list = []
nome_list = []
status_list = []
hora_inicio_list = []
hora_total_list = []


def load_data():
    id_list.clear()
    nome_list.clear()
    status_list.clear()
    hora_inicio_list.clear()
    hora_total_list.clear()
    rows = database.oficiais()
    for row in rows:
        id_list.append(row[0])
        nome_list.append(row[1])
        status_list.append(row[2])
        hora_inicio_list.append(row[3])
        hora_total_list.append(row[4])


def get_planilha():
    workbook = xlsxwriter.Workbook('autoponto.xlsx')
    sheet = workbook.add_worksheet()
    title = workbook.add_format({'bold': True, 'align': 'center'})
    center = workbook.add_format({'align': 'center'})

    sheet.write('A1', 'ID', title)
    sheet.set_column(0, 0, 8)
    sheet.write('B1', 'Nome', title)
    sheet.set_column(1, 1, 28)
    sheet.write('C1', 'Ponto Total', title)
    sheet.set_column(2, 2, 12)

    for item in range(len(id_list)):
        sheet.write(item+1, 0, id_list[item])
        sheet.write(item+1, 1, nome_list[item])
        sheet.write(item+1, 2, str(hora_total_list[item]), center)
    workbook.close()
