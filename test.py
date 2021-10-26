
from bs4 import BeautifulSoup
import re
import json


path = "C:/Users/piotr/PycharmProjects/Project_93_selenium/data/2021_10_21_001/car_details/6090350732.html"

file = open (path, 'r', encoding="utf-8")
html_text = file.read()

soup = BeautifulSoup (html_text, 'html.parser')
tag_script = soup.findAll ("script",text=re.compile('GPT.targeting'))
script_text = tag_script[0].text
pattern = re.compile(r"GPT.targeting\s+=\s+(\{.*?\});\n")
data = pattern.search(script_text).group(1)
data = json.loads(data)

print(data)
v_body_type = data['body_type'][0]
v_country_origin = data['country_origin'][0]




#script type="text/javascript">
