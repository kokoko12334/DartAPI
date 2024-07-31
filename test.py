import dart_fss as dart
import requests
import zipfile
import io
import re
# Open DART API KEY 설정
api_key='2442c769899b3d87601dd4964b46f09cadbe243f'
dart.set_api_key(api_key=api_key)

corp_list = dart.get_corp_list()
#00303873

corp_code = '00663289'

company = corp_list.find_by_corp_code(corp_code=corp_code)

# 사업보고서 검색

reports = company.search_filings(bgn_de='20240101', pblntf_detail_ty=['a003','a002','a001'], sort='date')
# 첫번째 리포트 선택

reports

matches = re.findall(r'.*사업보고서.*', reports[0].report_nm)
rcp_no = reports[0].rcp_no
url = f'https://opendart.fss.or.kr/api/document.xml?crtfc_key={api_key}&rcept_no={rcp_no}'
# 데이터 요청
response = requests.get(url)
response.raise_for_status()  # 요청에 실패하면 예외 발생

with zipfile.ZipFile(io.BytesIO(response.content)) as thezip:
    thezip.extractall()
    if matches:
        file_list = thezip.namelist()

        file_name = thezip.namelist()[-1]
        print(file_name)
    else:
        pass

