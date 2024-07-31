from bs4 import BeautifulSoup
from tqdm import tqdm
import pickle

xml_filename = 'CORPCODE.xml'  # xml파일이름.
with open(xml_filename, 'r', encoding='utf-8') as file:
    xml_data = file.read()
soup = BeautifulSoup(xml_data, 'xml')

result = dict()
for list_tag in tqdm(soup.find_all('list')):
    code = list_tag.find('stock_code')
    
    if code.text.strip():
        corp_code = list_tag.find('corp_code').text.strip()
        stock_code = list_tag.find('stock_code').text.strip()
        modify_date = list_tag.find('modify_date').text.strip()
        corp_name = list_tag.find('corp_name').text.strip()
        result[corp_name] = [corp_code, stock_code, modify_date] 
        
print(len(result))
print(result['삼성전자'])


with open("corp_info.pkl", "wb") as file:
    pickle.dump(result, file)
