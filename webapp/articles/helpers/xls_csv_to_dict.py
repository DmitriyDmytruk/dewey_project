import codecs
import csv
import uuid
from typing import IO, Any, Dict, List, Tuple, Union

from xlrd import Book, open_workbook
from xlrd.sheet import Sheet


def columns_mapping(origin_dict: dict) -> Dict:
    """
    Mapping table columns to model columns
    :param origin_dict: dict
    :return: dict
    """
    origin_dict["legal_language"] = origin_dict.pop("regulation")
    origin_dict["local_regulation"] = origin_dict.pop("local_reg")
    origin_dict["abstract"] = origin_dict.pop("abstract_(interpretation)")
    origin_dict["cfr40_part280"] = origin_dict.pop(
        "40cfr_part_280_federal_rule"
    )
    tags = origin_dict["tags"].split("#")[1:]
    origin_dict["tags"] = [{"name": tag} for tag in tags]
    origin_dict["categories"] = [
        {"name": origin_dict[f"category_{i}"]}
        for i in range(1, 17)
        if origin_dict[f"category_{i}"]
    ]
    origin_dict.pop("")
    for i in range(1, 17):
        origin_dict.pop(f"category_{i}")
    origin_dict["unique_id"] = uuid.uuid4().hex[:30]
    return origin_dict


class XLSReader:
    """
    Read .xls file and convert it to dict
    """

    def __init__(self) -> None:
        self.keys = []
        self.sheet = Sheet
        self.file = IO
        self.dict_list = []
        self.state = str

    def open(self, file: IO) -> Tuple[Sheet, List[str]]:
        """
        Open .xls file (from memory)
        """
        book: Book = open_workbook(file_contents=file.read())
        self.sheet: Union[Sheet, Any] = book.sheet_by_index(0)
        self.keys: List[str] = [
            self.sheet.cell(0, col_index).value
            for col_index in range(self.sheet.ncols)
        ]
        return self.sheet, self.keys

    def _read(self, row_index: int) -> Dict[str, str]:
        """
        Columns mapping
        """
        col_index: int
        data = {
            self.keys[col_index]
            .lower()
            .replace(" ", "_")
            .strip(): self.sheet.cell(row_index, col_index)
            .value
            for col_index in range(self.sheet.ncols)
        }
        if self.sheet.cell(row_index, 0).value:
            self.state = self.sheet.cell(row_index, 0).value
        data["state"] = self.state
        data = columns_mapping(data)
        return data

    def to_dict(self, file: IO) -> List[dict]:
        """
        Collects data to list
        """
        self.open(file)
        for row_index in range(1, self.sheet.nrows):
            data = self._read(row_index)
            self.dict_list.append(data)
        return self.dict_list


class CSVReader:
    """
    Read .csv file and convert it to dict
    """

    def __init__(self) -> None:
        self.keys = []
        self.sheet = Sheet
        self.file = IO
        self.dict_list = []
        self.rows_list = []

    def open(self, file: IO) -> Tuple[list, list]:
        """
        Open .csv file (from memory)
        """
        self.rows_list = list(csv.reader(codecs.iterdecode(file, "utf-8")))
        self.keys: List[str] = [
            k.lower().replace(" ", "_") for k in self.rows_list[0]
        ]
        return self.rows_list, self.keys

    def _read(self, rows: list) -> Dict[str, str]:
        """
        Columns mapping
        """
        data = {}
        for index, item in enumerate(rows):
            data[self.keys[index]] = item
        data = columns_mapping(data)
        return data

    def to_dict(self, file: IO) -> List[dict]:
        """
        Collects data to list
        """
        self.open(file)
        dict_list = []
        for rows in self.rows_list[1:]:
            data = self._read(rows)
            dict_list.append(data)
        return dict_list
