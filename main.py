import time
from googleapi import *
from danawatracker import danawa_crawler
from datetime import datetime

SPREADSHEET_ID = "" # Write the Google Spreadsheet ID

if __name__ == '__main__':
    today_date = datetime.today().strftime("%Y%m%d")
    api = GoogleAPI()
    sheet_service = api.get_sheet_service()

    row_num = 2
    message_list = []

    while(True):
        result = spreadsheet_read(sheet_service, SPREADSHEET_ID, f"A{row_num}:F{row_num}")
        info_list = result.get('values')
        if info_list is None:
            break
        
        info_list = info_list[0]
        
        track_url = info_list[3]
        result = danawa_crawler(track_url)
        lowest_now = result.get('price').replace('원', '').replace(',', '')

        track_list = [info_list[0], info_list[1], lowest_now, result.get('link')]
        if int(lowest_now) <= int(info_list[4]):
            track_list.append("LOWEST")
            update_list = [lowest_now, today_date]
            spreadsheet_write(sheet_service, SPREADSHEET_ID, f"E{row_num}:F{row_num}", update_list)
        message_list.append(track_list)
        row_num += 1
        time.sleep(2)


    gmail_service = api.get_gmail_service()
    message_text = "\n".join(
        ["\t".join(lst) for lst in message_list]
    )
    print(message_text)
    message = create_message('Sender Email', 'Receiver Email', today_date, message_text)
    send_message(gmail_service, 'me', message)