##광주광역시 버스 정류장
import requests, xmltodict, json
from urllib.parse import urlencode, unquote
from bs4 import BeautifulSoup

url = 'http://api.gwangju.go.kr/xml/stationInfo'
params ={'serviceKey' : 'RFKv4CbXS%2FQn6OUogm1mvTqvk7w85vYYV0AO946MZ35YUyCWPVzEPxV6p1zm7Zjh7y6Pc6RJdYnApvb5ITObHQ%3D%3D' }

response = requests.get(url, params=params)
##print(response.content)

xml_data = response.text
dict_data = xmltodict.parse(xml_data)

son_data = json.loads(json.dumps(dict_data))
##print(json_data)

address_list = json_data['ns2:STATION_INFO']['STATION_LIST']['STATION']


try:
    for i in range(0,4436):
        
        r1 = address_list[i]['BUSSTOP_ID']
        r2 = address_list[i]['BUSSTOP_NAME']
        r3 = address_list[i]['LONGITUDE']
        r4 = address_list[i]['LATITUDE']
        
        print("['"+r1+"','"+ r2 + "','" + r3 + "','" +r4+"'],")
        

        
except IndexError:
    pass








