from bs4 import BeautifulSoup
import re
import pickle
from lxml import etree
from xml.etree import ElementTree as et
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

with open('corp_info.pkl', 'rb') as file:
    corp_info = pickle.load(file)


directory = 'company_report'

name = '로스웰'
test_data = [(name, corp_info[name])]
for k, v in test_data:

    corp_name, corp_code, stock_code, mofidy_date, rcp_no = k, *v

    xml_filename = f'{directory}/{corp_name}-{corp_code}-{stock_code}-{mofidy_date}.xml'

    try:

        with open(xml_filename, 'r', encoding='utf-8') as file:
            xml_data = file.read()

        
        if xml_data.startswith('<?xml'):
            xml_data = xml_data.split('?>', 1)[1]
        
        xml_data = xml_data.replace("&", "&amp;")
        import xml.etree.ElementTree as ETree

        parser = ETree.XMLParser(encoding="utf-8")
        tree = ETree.parse(xml_filename, parser=parser)
        print(ETree.tostring(tree.getroot()))

        soup = BeautifulSoup(xml_data, 'xml')
        print(len(str(soup)))
        soup = etree.fromstring(xml_data)
        et.parse(xml_filename)


        
        
        # 조건에 맞는 SECTION-2 태그 찾기
        extracted_sections = soup.find_all('SECTION-2')
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
                        string = table_to_string(tag)
                        if string:
                            sub_text.append(string)

            text.append("\n".join(sub_text))
        
        if len("".join(text)) <= 300:
            print(f"fail: {stock_code}-{corp_code}-{corp_name}, len:{len("".join(text))} section2:{len(result)}")
            continue

        file_name = f'company_pre_report/pre_{corp_name}-{corp_code}-{stock_code}-{rcp_no}-{mofidy_date}.txt'
        
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write("\n".join(text))
        
        print(f" text_size:{len("".join(text))}success: {stock_code}-{corp_code}-{corp_name}")
    
    except Exception as e:
    
        print(f"fail: {stock_code}-{corp_code}-{corp_name}, error:{e}")
        continue


from lxml import etree
parser = etree.XMLParser(recover=True)
if xml_data.startswith('<?xml'):
            xml_data = xml_data.split('?>', 1)[1]

xml_data = xml_data.replace("&", "&amp;")
result = etree.fromstring(xml_data)