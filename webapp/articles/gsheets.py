import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def get_google_sheet(link="https://docs.google.com/spreadsheets/d/1euoRKgl3ojqXL5xVZzBo3kSZ1SK-xVHbOy3llHzLRyY"):
    """
    Opens Google Sheet document by link

    :param link: URL of a spreadsheet as it appears in a browser.
    :type link: str

    :returns: a :class:`gspread.models.Spreadsheet` instance.
    """
    _google_auth_scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    _credentials = ServiceAccountCredentials.from_json_keyfile_name(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"),
                                                                    _google_auth_scope)
    _google_client = gspread.authorize(_credentials)

    return _google_client.open_by_url(link)
