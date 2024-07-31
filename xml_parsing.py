from bs4 import BeautifulSoup
import re
import pandas as pd
import pickle
import logging
# def table_to_string(table_tag):
#     t_rows = []
#     if not table_tag.find('THEAD'):
#     # text.append([re.sub(r'\s+', ' ', table_tag.text.strip('\n'))])
#         return

#     thead_tags = table_tag.find('THEAD').find_all('TR')
#     col_length = 0
#     for first_th_tag in thead_tags[0].find_all('TH'):
#         if 'COLSPAN' in first_th_tag.attrs:
#             cnt = int(first_th_tag.attrs['COLSPAN'])
#             col_length += cnt
#         else:
#             col_length += 1

#     t_head = [[''] * col_length for _ in range(len(thead_tags))]

#     for r in range(len(thead_tags)):
        
#         thead_tag = thead_tags[r]
#         th_tags = thead_tag.find_all('TH')
            
#         col_idx = 0
#         for c in range(len(th_tags)):
#             th_tag = th_tags[c]
#             move = 1
#             while t_head[r][col_idx] == 'no12345':
#                 col_idx += 1
#             if 'COLSPAN' in th_tag.attrs:
#                 cnt = int(th_tag.attrs['COLSPAN'])
#                 for i in range(cnt):
#                     t_head[r][col_idx+i] = re.sub(r'\s+', ' ', th_tag.text.strip('\n'))
#                 move = cnt
#             else:
#                 t_head[r][col_idx] = re.sub(r'\s+', ' ', th_tag.text.strip('\n'))
#             if 'ROWSPAN' in th_tag.attrs:
#                 cnt = int(th_tag.attrs['ROWSPAN'])
#                 for i in range(1, cnt):
#                     t_head[r+i][col_idx] = 'no12345'
#             col_idx += move

#     t_head_name = []
#     for i in range(col_length):
#         name = ''
#         for j in range(len(thead_tags)):
#             if t_head[j][i] == 'no12345':
#                 name += ''
#             else:
#                 name += t_head[j][i]
#         t_head_name.append(name)
#     t_rows.append(t_head_name)

#     col_length = len(t_head_name)
#     tr_tags = table_tag.find_all('TR') # t_head 부분 제외
#     row_length = len(tr_tags)
#     row_data = [[''] * col_length for _ in range(row_length)]

#     for r in range(row_length):
#         tr_tag = tr_tags[r]
#         td_tags = tr_tag.findAll('TD')
#         if not td_tags:
#             continue
                
#         col_idx = 0
#         for c in range(len(td_tags)):
#             td_tag = td_tags[c]
#             move = 1
#             if td_tag.text:
#                 data = td_tag.text
#             else:
#                 data = '-'

#             while row_data[r][col_idx]:

#                 col_idx += 1

#             if 'COLSPAN' in td_tag.attrs:
#                 cnt = int(td_tag.attrs['COLSPAN'])
#                 for i in range(cnt):
#                     row_data[r][col_idx+i] = data
#                 move = cnt
#             else:
#                 row_data[r][col_idx] = data


#             if 'ROWSPAN' in td_tag.attrs:
#                 cnt = int(td_tag.attrs['ROWSPAN'])
#                 for i in range(1, cnt):
#                     row_data[r+i][col_idx] = data
#             col_idx += move
    

#     for i in row_data[1:]:
#         t_rows.append(i)

#     df = pd.DataFrame(t_rows[1:], columns=t_rows[0])
#     string = df.to_string(index=False).strip()
#     return string

def table_to_string(table_tag):
    data = []
    
    # 열 수 카운트를 위한 변수
    row_count = 0

    for row in table_tag.find_all("TR"):
        cols = row.find_all('TD')
        row_data = []
        
        for col in cols:
            col_span = int(col.get('COLSPAN', 1))  # 기본값 1
            row_span = int(col.get('ROWSPAN', 1))  # 기본값 1
            
            # 현재 열의 데이터 추가
            row_data.append(col.get_text(strip=True))
            
            # rowspan 처리를 위해 빈 문자열로 채우기
            if row_span > 1:
                for _ in range(1, row_span):
                    if row_count + _ < len(data):
                        data[row_count + _].append("")  # 이후 열에 빈 문자열 추가
            # colspan 처리를 위해 여전히 열 수를 유지
        
        # 데이터 리스트에 추가
        data.append(row_data)
        row_count += 1

    # 결과 출력
    result = []
    for row in data:
        result.append(" | ".join(row))

    return "\n".join(result)

logging.basicConfig(
    level=logging.DEBUG,  
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  
    filename='dart_pre_report.log',  
    filemode='a',  
    encoding = 'utf-8'
)

logger = logging.getLogger('my_logger')

with open('corp_info.pkl', 'rb') as file:
    corp_info = pickle.load(file)

directory = 'company_report'
# corp_info = corp_info['푸드나무']
# corp_info

for k, v in corp_info.items():

    corp_name, corp_code, stock_code, mofidy_date, rcp_no = k, *v

    xml_filename = f'{directory}/{corp_name}-{corp_code}-{stock_code}-{mofidy_date}.xml'

    try:

        with open(xml_filename, 'r', encoding='utf-8') as file:
            xml_data = file.read()
        soup = BeautifulSoup(xml_data, 'xml')

        # 조건에 맞는 SECTION-1 태그 찾기
        extracted_sections = soup.find_all('SECTION-2', {'ACLASS': 'MANDATORY'})
        result = []
        pattern = re.compile(r'L-0-2-\d+-(L1|L2)')
        for section in extracted_sections:
                title = section.find('TITLE', {'ATOC': 'Y', 'AASSOCNOTE':pattern})
                if title:
                    result.append(section)

        text = []
        for section2 in result:
            sub_text = []
            for tag in section2.children:

                match tag.name:

                    case 'TITLE':
                        title = tag.text.strip()
                        sub_text.append(title)

                    case 'P':
                        span_text = []
                        for span_tag in tag.find_all('SPAN'):
                            if span_tag:
                                span_text.append(span_tag.text.strip())

                        if span_text:
                            sub_text.append(" ".join(span_text))

                    case 'TABLE':
                        
                            # string = table_to_string(tag)
                        
                        string = table_to_string(tag)
                        if string:
                            sub_text.append(string)

            text.append("\n".join(sub_text))
        
        if len("".join(text)) <= 300:
            logger.warning(f"fail: {stock_code}-{corp_code}-{corp_name}, len:{len("".join(text))} section2:{len(result)}")
            continue

        file_name = f'company_pre_report/pre_{corp_name}-{corp_code}-{stock_code}-{rcp_no}-{mofidy_date}.txt'
        
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write("\n".join(text))
        
        logger.info(f" text_size:{len("".join(text))}success: {stock_code}-{corp_code}-{corp_name}")
    
    except Exception as e:
    
        logger.warning(f"fail: {stock_code}-{corp_code}-{corp_name}, error:{e}")
        continue

