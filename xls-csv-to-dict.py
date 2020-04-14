import csv
from typing import Dict

from xlrd import open_workbook


def columns_mapping(origin_dict: dict) -> Dict:
    origin_dict["legal_language"] = origin_dict.pop("legal_regulation")
    tags = origin_dict["tags"].split(",")
    origin_dict["tags"] = [{"name": tag} for tag in tags]
    categories = origin_dict["categories"].split(",")
    origin_dict["categories"] = [{"name": category} for category in categories]

    return d


# Read xls file
book = open_workbook("test.xls")
sheet = book.sheet_by_index(0)

keys = [sheet.cell(0, col_index).value for col_index in range(sheet.ncols)]

dict_list = []
for row_index in range(1, sheet.nrows):
    d = {
        keys[col_index]
        .lower()
        .replace(" ", "_"): sheet.cell(row_index, col_index)
        .value
        for col_index in range(sheet.ncols)
    }
    d = columns_mapping(d)
    dict_list.append(d)

print(dict_list)


# Read csv file
with open("test.csv") as f:
    rows_list = list(csv.reader(f))
    keys = [k.lower().replace(" ", "_") for k in rows_list[0]]
    dict_list = []
    for row in rows_list[1:]:
        d = {}
        for index, item in enumerate(row):
            d[keys[index]] = item
        d = columns_mapping(d)
        dict_list.append(d)

print(dict_list)
