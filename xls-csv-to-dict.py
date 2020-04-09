import csv

from xlrd import open_workbook


# Read xls file

book = open_workbook("test.xls")
sheet = book.sheet_by_index(0)

keys = [sheet.cell(0, col_index).value for col_index in range(sheet.ncols)]

dict_list = []
for row_index in range(1, sheet.nrows):
    d = {
        keys[col_index]: sheet.cell(row_index, col_index).value
        for col_index in range(sheet.ncols)
    }
    dict_list.append(d)

print(dict_list)
# [{'Column1': '1_value1', 'Column2': '2_value1', 'Column3': '3_value1'}, {'Column1': '1_value2', 'Column2': '2_value2', 'Column3': '3_value2'}, {'Column1': '1_value3', 'Column2': '2_value3', 'Column3': '3_value3'}, {'Column1': '', 'Column2': '2_value4', 'Column3': ''}]


# Read csv file

with open("test.csv") as f:
    reader = csv.reader(f)
    dict_list = []
    rows_list = [rows for rows in reader]
    keys = rows_list[0]
    for row in rows_list[1:]:
        d = {keys[index]: value for index, value in enumerate(row)}
        dict_list.append(d)

print(dict_list)
# [{'Column1': '1_value1', 'Column2': '2_value1', 'Column3': '3_value1'}, {'Column1': '1_value2', 'Column2': '2_value2', 'Column3': '3_value2'}, {'Column1': '1_value3', 'Column2': '2_value3', 'Column3': '3_value3'}, {'Column1': '', 'Column2': '2_value4', 'Column3': ''}]
