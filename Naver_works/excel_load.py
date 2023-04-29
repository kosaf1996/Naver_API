import openpyxl
import json 
from collections import OrderedDict
import works_calender_schedule


###################################################################
###                       Excel Load                            ###
###################################################################
class excel_load :
    #########################################
    ##            초기화 함수               ##
    #########################################
    def __init__(self) :
       self.fpath ="C:\\Users\\GoodusData\\Desktop\\calender.xlsx"

    #########################################
    ##          캘린더 Excel Load           ##
    #########################################
    def calender_excel_load(self, token):
       data = openpyxl.load_workbook(self.fpath) #excel load
       sheet = data.worksheets[0] #첫번쨰 워크 시트

       data = OrderedDict()

       data_list = []
        
       for row in sheet.rows:
           data["client_id"] = row[0].value
           data["summary"] = row[1].value
           data["start"] = row[2].value
           data["end"] = row[3].value
           data["timezone"] = row[4].value
           data["calender_id"] = row[5].value
           data["participant"] = row[6].value
           data["calender_name"] = row[8].value
           json_data = json.dumps(data, ensure_ascii=False, indent=4 )
           data_list.append(json_data)
       
       data_list.pop(0)
       calender = works_calender_schedule.calender_schedule()
       return calender.schedule(data_list, token)
