import requests
import json
###################################################################
###                      캘린더 스케줄                           ###
###################################################################
class calender_schedule :
    #########################################
    ##            초기화 함수               ##
    #########################################
    def __init__(self):
        pass 

    #########################################
    ##           캘린더 일정 생성           ##
    #########################################      
    def schedule(self, data_list, token):        
        for data_list in data_list :
            jsonObject = json.loads(data_list)
            
            if jsonObject['client_id'] == None :
                pass

            if  jsonObject['client_id'] is not None :
                calender_id = calender_schedule.calender_id(self,jsonObject['client_id'], token, jsonObject['calender_name'])
                url = f"https://www.worksapis.com/v1.0/users/{jsonObject['client_id']}/calendars/{calender_id}/events"

                header = {
                    "Authorization" : f"Bearer {token}",
                    "Content-Type" : "application/json"
                }

                data = { 
                    "eventComponents": [    
                    {
                        "summary" : jsonObject['summary'],
                        #"description": "Memo",
                        #"categoryId": "1",
                        "start": {
                            "dateTime" : jsonObject['start'],
                            "timeZone" : jsonObject['timezone']
                        },
                        # "end" : {
                        #     "dateTime" : jsonObject['end'],
                        #     "timeZone" : jsonObject['timezone']
                        # },
                        # "organizer": {
                        #     "email": jsonObject['client_id'],
                        # },
                    }
                    ]
                }

                requests.post(url,headers=header,json=data)

    #########################################
    ##        클라이언트 아이디 조회         ##
    #########################################      
    def calender_id(self, client_id, token, tg_calender) :
        url = f"https://www.worksapis.com/v1.0/users/{client_id}/calendar-personals"
        header = {
                    "Authorization" : f"Bearer {token}"
                }
        calender_list = requests.get(url, headers=header).json()

        calender_list = calender_list.get("calendarPersonals")

        for i in calender_list:
            if i.get("calendarName") == tg_calender: 
                return i.get("calendarId")
            else :
                pass 