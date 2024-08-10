import xml.etree.ElementTree as ET
import re
file_path = "./company_report/로스웰-01139266-900260-20190312.xml"

def find_and_replace_char_in_xml(xml_string, line, column):
    # 문자열을 줄 단위로 나누기
    lines = xml_string.splitlines()

    # 요청한 줄이 유효한지 확인
    if line - 1 < len(lines):
        target_line = lines[line - 1]
        if column - 1 < len(target_line):
            # 해당 위치의 문자 확인
            original_char = target_line[column - 1]
            # 각 문자에 대해 치환 적용
            if original_char == '<':
                replacement_char = '&lt;'
            elif original_char == '>':
                replacement_char = '&gt;'
            elif original_char == '&':
                replacement_char = '&amp;'
            elif original_char == '"':
                replacement_char = '&quot;'
            elif original_char == "'":
                replacement_char = '&apos;'
            else:
                replacement_char = original_char  # 다른 문자는 그대로 유지

            # 문자 치환
            lines[line - 1] = (target_line[:column - 1] + replacement_char +
                               target_line[column:])
            new_xml_string = "\n".join(lines)
            print(f"원래 문자: '{original_char}' -> 변경된 문자: '{replacement_char}'")
            return new_xml_string
        else:
            print("열 번호가 유효하지 않습니다.")
            return xml_string
    else:
        print("줄 번호가 유효하지 않습니다.")
        return xml_string

def parse_xml_string(xml_string):
    while True:
        try:
            # XML 문자열 파싱
            root = ET.fromstring(xml_string)
            print("XML 파싱 성공!")
            return root
        except ET.ParseError as e:
            print("XML 파싱 오류 발생!")
            print("오류 메시지:", e.msg)  # 오류 메시지 출력
            print("오류 위치:", e.position)  # 오류 위치 출력
            line, column = e.position

            # 오류 위치에서 문자 찾기 및 치환
            xml_string = find_and_replace_char_in_xml(xml_string, line, column)

with open(file_path, 'r', encoding='utf-8') as file:
            xml_string = file.read()  # 파일 내용 읽기

if xml_string:
    parse_xml_string(xml_string)

## 사업의 내용


#회계감사인의 감사의견 등

# 결과 출력

xml_string_invalid = """<root>
    <tag1><tag2><Content></tag2></tag1>
    <tag3>More content</tag3>
    <tag4>Invalid & </tag4>
</root>"""  # <tag4> 태그가 닫히지 않고 '&'가 포함된 잘못된 XML

# XML 문자열 파싱 시도
parse_xml_string(xml_string_invalid)




cleaned_string = re.sub(r'<.*?>', '', xml_string)

# 결과 출력
print(cleaned_string.strip())

start_index = cleaned_string.find("사업의 내용")

# "회계감사인의 감사의견 등" 끝 인덱스 찾기 + 길이 (선택적으로 문구의 길이를 더할 수 있음)
end_index = cleaned_string.find("재무에 관한 사항")

# 문자열 슬라이싱
if start_index != -1 and end_index != -1:
    trimmed_string = cleaned_string[start_index:end_index]
else:
    trimmed_string = ''



trimmed_string.replace("\n", "")
len(trimmed_string)
len(trimmed_string.replace("\n", ""))
# 결과 출력
print(trimmed_string)

with open("output.txt", "w", encoding="utf-8") as file:
    file.write(trimmed_string)



with open("output2.txt", "w", encoding="utf-8") as file:
    file.write(trimmed_string.replace("\n", ""))
