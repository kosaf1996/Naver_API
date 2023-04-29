import works_jwt
import works_token
import excel_load

    #########################################
    ##              메인 함수               ##
    #########################################  
if __name__ == '__main__':
    #Class
    works_jwt = works_jwt.works_jwt()
    token = works_token.works_token()
    excel_load = excel_load.excel_load()

    #function Call
    #jwt 생성
    jwt = works_jwt.jwt_works()
    #token 생성 
    token = token.works_token(jwt)

    #캘린더 일정 생성 
    #excel_load.calender_excel_load(token)

    
    

        