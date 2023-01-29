# Naver_API
 ### 1.Server Image Create & Delete
* Global 변수 영역만 수정하여 진행합니다.
 ##### 1.Server Image Create 
1. ncloud_accesskey, ncloud_secretkey  네이버클라우드에서 인증키발급받은 키를 입력합니다. 
2. log_path 이미지 생성한 로그가 생성될 경로입니다. 
     절대경로로 입력하여야 합니다. 
3. api_server 네이버 클라우드의 일반, 공공, 금융 별로 나누워 요청 하게됩니다.  각 클라우드 별로 경로가 틀리니 네이버클라우드 API 가이드를 참고하여 입력 바랍니다. 
4. Instance_list 서버 이미지로 생성할 인스턴스 아이디 값을 리스트 형식으로 입력합니다. ex)523823
5. ServerImageName_list 는 생성될 서버 이미지의 이름 입니다. Instance_list[0] 번과 ServerImageName_list[0] 번 형식으로 매핑 되게 됩니다. 
6. 생성되는 서버이미지 명은 test1-2023-01-30 형식으로 생성되게 됩니다. 

 ##### 2.Server Image Delete 
1. Delete Server Image 는 ServerImageName_list만 입력하면 삭제 되게 됩니다.
2. 삭제되는 서버 이미지 명은 test1-2023-01-30 형식으로 삭제되게 됩니다. 
3. log_delete() 함수는 생성된 로그를 일정기간 지나면 지워주는 함수입니다. 기본 값은 30일입니다. 
3. 이외 나머지는 Create Server Image 와 동일합니다. 
