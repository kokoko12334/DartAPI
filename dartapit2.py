import OpenDartReader
import os
from dotenv import load_dotenv

load_dotenv()
api_key=os.getenv('DARTAPIKEY')

dart = OpenDartReader(api_key) 


### 1. 공시정보 ###
# 특정기업(삼성전자) 상장이후 모든 공시 목록 (5,600 건+)
dart.list('삼성전자') # 기업이름 혹은,
dart.list('005930') # 종목코드를 사용할 수 있습니다.

# 특정기업(삼성전자) 특정 날짜 이후 공시목록 (날짜에 다양한 포맷이 가능합니다 2022, '2022-01-01', '20220101' )
dart.list('삼성전자', start='2022-01-01') # 2022-01-01 ~ 오늘
dart.list('005930', start='2022-01-01') # 2022-01-01 ~ 오늘

# 특정기업(삼성전자) 특정 일자 범위(start~end)의 공시목록 (날짜에 다양한 포맷이 가능합니다)
dart.list('005930', start='2022-04-28', end='2022-04-28')

# 특정기업(삼성전자) 1999년~이후 모든 정기보고서 (정정된 공시포함)
dart.list('005930', start='1999-01-01', kind='A', final=False)

# 특정기업(삼성전자) 1999년~이후 모든 정기보고서 (최종보고서)
dart.list('005930', start='1999-01-01', kind='A') 

# 2022-07-01 하루동안 모든 기업의 공시목록
dart.list(start='20200701', end='20200701')

# 2022-01-01 ~ 2022-01-10 모든 회사의 모든 공시목록 (3,139 건)
dart.list(start='2022-01-01', end='2022-01-10')

# 2022-01-01 ~ 2022-01-10 모든 회사의 모든 공시목록 (정정된 공시포함) (3,587 건)
dart.list(start='2022-01-01', end='2022-01-10', final=False)

# 2022-01-01~2022-03-30 모든 회사의 정기보고서 (corp를 특정 하지 않으면 최대 3개월) (2,352 건)
dart.list(start='2022-01-01', end='2022-03-30', kind='A')


# ==== 1-2. 공시정보 - 기업개황 ====
# 기업의 개황정보
dart.company('005930')

# 회사명에 "삼성전자"가 포함된 회사들에 대한 개황정보
dart.company_by_name('삼성전자')

# ==== 1-2. 공시정보 - 기업개황 ====
# 기업의 개황정보
dart.company('005930')

# 회사명에 "삼성전자"가 포함된 회사들에 대한 개황정보
dart.company_by_name('삼성전자')


# ==== 1-3. 공시정보 - 공시서류원본파일 ====
# 삼성전자 사업보고서 (2022년 반기사업보고서) 원문 텍스트
xml_text = dart.document('20220816001711')

# ==== 1-3. 공시정보 - 공시서류원본파일 전체 리스트 (사업보고서, 감사보고서) ====
# 삼성전자 사업보고서 (2022년 반기사업보고서) 원문 텍스트, 감사보고서
xml_text_list = dart.document_all('20220816001711')
xml_text = xml_text_list[0]

# ==== 1-4. 공시정보 - 고유번호 ====
# 종목코드로 고유번호 얻기
dart.find_corp_code('005930')

# 기업명으로 고유번호 얻기
dart.find_corp_code('삼성전자')


### 2. 사업보고서 ###
# 조회가능한 사업보고서의 항목: 
['조건부자본증권미상환', '미등기임원보수', '회사채미상환', '단기사채미상환', '기업어음미상환', '채무증권발행', '사모자금사용', '공모자금사용', '임원전체보수승인', '임원전체보수유형', '주식총수', '회계감사', '감사용역', '회계감사용역계약', '사외이사', '신종자본증권미상환', '증자', '배당', '자기주식', '최대주주', '최대주주변동', '소액주주', '임원', '직원', '임원개인보수', '임원전체보수', '개인별보수', '타법인출자']

dart.report('005930', '미등기임원보수', 2021)  # 미등기임원 보수현황
dart.report('005930', '증자', 2021) # 증자(감자) 현황
dart.report('005930', '배당', 2018)  # 배당에 관한 사항




import dart_fss as dart
from dotenv import load_dotenv
load_dotenv()
api_key=os.getenv('DARTAPIKEY')
dart.set_api_key(api_key=api_key)


# 삼성전자 code
corp_code = '00126380'

# 모든 상장된 기업 리스트 불러오기
corp_list = dart.get_corp_list()

# 삼성전자
samsung = corp_list.find_by_corp_code(corp_code=corp_code)

# 연간보고서 검색
reports = samsung.search_filings(bgn_de='20210101', pblntf_detail_ty='a001')

# 가장 최신 보고서 선택
newest_report = reports[0]
newest_report

from dart_fss.xbrl.dart_xbrl import DartXbrl
from arelle import ModelXbrl, XbrlConst
from arelle import Cntlr

# model_xbrl = cntlr.modelManager.load(file_path)
DartXbrl("./company_report/AK홀딩스-00125080-006840-20230111.xml", xbrl=ModelXbrl())
dart.xbrl.get_xbrl_from_file("AK홀딩스-00125080-006840-20230111.xml")

from arelle import Cntlr
from arelle.ModelXbrl import ModelXbrl
import pickle
def load_xbrl_file(filepath):
    # Controller 객체 생성
    cntlr = Cntlr.Cntlr()

    # XBRL 파일 로드

    model_xbrl = cntlr.modelManager.load(filepath)
    print(model_xbrl.facts)
    if model_xbrl.facts is None:
        print("Error loading XBRL file.")
        return
    
    # 성공적으로 로드 및 검증된 경우
    print("XBRL file loaded and validated successfully.")
    return model_xbrl
# XBRL 파일 경로 지정
xbrl_file_path = "path/to/your/xbrl-file.xbrl"


with open('corp_info.pkl', 'rb') as file:
    corp_info = pickle.load(file)



directory = './company_report'
name = '로스웰'
test_data = [(name, corp_info[name])]
corp_name, corp_code, stock_code, mofidy_date, rcp_no = test_data[0][0], *test_data[0][1]
xml_filename = f'{directory}/{corp_name}-{corp_code}-{stock_code}-{mofidy_date}.xml'

# XBRL 파일 로드 및 검증 실행
result = load_xbrl_file(xml_filename)

print(xml_filename)
dart.xbrl.get_xbrl_from_file("test/20240312000736_00760.xml")


import requests
import zipfile
import io
newest_report
api_key
rcp_no = '20240312000736'
url = f'https://opendart.fss.or.kr/api/document.xml?crtfc_key={api_key}&rcept_no={rcp_no}'

        # 공시 리포트 xml파일 데이터 요청
response = requests.get(url)
response.raise_for_status()  # 요청에 실패하면 예외 발생

# 응답 데이터 저장 및 ZIP 파일 해제
with zipfile.ZipFile(io.BytesIO(response.content)) as thezip:
    #company_report 폴더 경로에 압축 해제
    extract_path = 'test'
    thezip.extractall(extract_path)