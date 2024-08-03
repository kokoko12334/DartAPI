import dart_fss as dart
import requests
import zipfile
import io
import pickle
import os
import logging
import re
from dotenv import load_dotenv
# Open DART API KEY 설정
load_dotenv()
api_key=os.getenv('DARTAPIKEY')
dart.set_api_key(api_key=api_key)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='dart_report.log',
    filemode='a',  # 파일모드 'a'는 추가 모드, 'w'는 덮어쓰기 모드,
    encoding = 'utf-8'
)
logger = logging.getLogger('my_logger')

with open('corp_info.pkl', 'rb') as file:
    corp_info = pickle.load(file)

# 모든 상장된 기업 리스트 불러오기
corp_list = dart.get_corp_list()

corp_code = '00126380'

# 삼성전자
samsung = corp_list.find_by_corp_code(corp_code=corp_code)

# 연간보고서 검색
reports = samsung.search_filings(bgn_de='20210101', pblntf_detail_ty='a001')

# 가장 최신 보고서 선택
newest_report = reports[0]
xbrl = newest_report.xbrl


xbrl.exist_consolidated()
xbrl.get_cash_flows(True)
xbrl.get_document_information()


dart.api.filings.download_document()

dart.api.filings.get_corp_info(corp_code=corp_code)


reports

# 회사 최신리포트를 DART API 요청하는 함수
def dart_report_request(corp_name, corp_code, stock_code, mofidy_date):
    global cnt
    company = corp_list.find_by_corp_code(corp_code=corp_code)

    try:
        #공시에 올라온 리포트 조회(a001: 사업보고서 a002:반기 보고서 a003:분기보고서)
        reports = company.search_filings(bgn_de='20240101', pblntf_detail_ty=['a001','a002','a003'], sort='date')

        # 최신 리포트 선택
        # 사업보고서는 ZIP 파일 해제할 경우, 감사보고서랑 같이 받기 때문에 최신 리포트가 사업보고서인 경우는 따라 처리가 필요
        is_business_report = re.findall(r'.*사업보고서.*', reports[0].report_nm)
        rcp_no = reports[0].rcp_no
        url = f'https://opendart.fss.or.kr/api/document.xml?crtfc_key={api_key}&rcept_no={rcp_no}'

        # 공시 리포트 xml파일 데이터 요청
        response = requests.get(url)
        response.raise_for_status()  # 요청에 실패하면 예외 발생

        # 응답 데이터 저장 및 ZIP 파일 해제
        with zipfile.ZipFile(io.BytesIO(response.content)) as thezip:
            #company_report 폴더 경로에 압축 해제
            extract_path = 'company_report'
            thezip.extractall(extract_path)

            # 새로운 파일명 지정 (예: '회사이름-DART회사코드-주식코드-최근변경일자')
            file_list = thezip.namelist()
            file_name = file_list[-1]
            current_file_path = os.path.join(extract_path, file_name)
            new_file_name = f'{corp_name}-{corp_code}-{stock_code}-{mofidy_date}.xml'
            new_file_path = os.path.join(extract_path, new_file_name)
            os.rename(current_file_path, new_file_path)

            # 만약 최신 리포트가 사업보고서라면 사업보고서만 저장하고 나머지(감사보고서)는 삭제
            if is_business_report:
                for file in file_list:
                    file_path = os.path.join(extract_path, file)
                    if file_path != new_file_path and os.path.exists(file_path):
                        os.remove(file_path)
        corp_info[corp_name].append(rcp_no)
        logger.info(f"{cnt}.success: {stock_code}-{corp_code}-{corp_name}:{rcp_no}")

    except Exception as e:
        del_list.append(corp_name)
        logger.warning(f"{cnt}.fail: {stock_code}-{corp_code}-{corp_name}, error:{e}")
        return


#[corp_code, stock_code, modify_date, rcp_no]
cnt = 1
del_list = []
for k, v in corp_info.items():
    dart_report_request(k, *v)
    cnt += 1

for corp_name in del_list:
    del corp_info[corp_name]
with open('corp_info.pkl', 'wb') as file:
    pickle.dump(corp_info, file)