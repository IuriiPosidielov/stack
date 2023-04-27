from bs4 import BeautifulSoup
import requests
import urllib.parse
import re
import pyperclip
import argparse


q = "how parse command line parameters python"

headers = {
        "referer":"referer: https://www.google.com/",
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
        }
        
def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)
    
def single_page_question_answer(url):
	with requests.Session() as s:
		s.post(url, headers=headers)
		response = s.get(url, headers=headers)

	page = BeautifulSoup(response.text, "html.parser")
	
	question = page.find_all("meta", property="og:title")
	answers=page.find_all("div", class_="s-prose js-post-body")
	print(len(answers))
	if (len(answers)<2):
		return question,"",""
	answer = answers[1]
	code_in_answer = []
	answer_string="" 
	for data in answer:
		if (data.getText().replace("\n","")!=""):
			answer_string += data.getText().replace("\n", "")
			answer_string += "\n"
		found_tags= re.findall(r'<[^>]+>', str(data))
		for tag in found_tags:
			if tag == "<code>":
				start_index = str(data).find("<code>") + 6
				end_index = str(data).find("</code>")
				code_in_answer.append(str(data)[start_index:end_index])
	code = ""
	for cod in code_in_answer:
		code += cod
	return question[0]['content'],answer_string,code


# parameter
parser = argparse.ArgumentParser(description="IT Assistant")
parser.add_argument("-q", action='store', dest='question', default='', help='your IT question')

result = parser.parse_args()

if (pyperclip.paste()!=""):
	q = pyperclip.paste()

if (result.question!=""):
	q = result.question
	
query = "site:stackoverflow.com python "
query = query + q

query = urllib.parse.quote_plus(query)

print (query)

with requests.Session() as s:
    url = f"https://www.google.com/search?q=" + query
    s.post(url, headers=headers)
    response = s.get(url, headers=headers)

soup = BeautifulSoup(response.text, "html.parser")

print (soup.title)
h = soup.find_all("a", href=True)
for i in h:
	if ("//stack" in i["href"]):
		url = i['href']
		print (url)
		q,a,c = single_page_question_answer(url)
		print(q)
		print(a)
		print(c)
		pyperclip.copy(str(c))
		break
