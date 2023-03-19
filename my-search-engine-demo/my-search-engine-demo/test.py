# import requests
# from bs4 import BeautifulSoup
# r = requests.get('https://www.sacred-texts.com/hin/rigveda/rv01001.htm')
# soup = BeautifulSoup(r.content, 'html.parser')
# lines = soup.find_all('p')[1]
# for line in lines:
#     print(line.text)
#     print()
    
    

# import requests
# from bs4 import BeautifulSoup
# import re
# URL = 'https://www.sacred-texts.com/hin/rigveda/rv0'
# for page in range(1001, 1192):
#     urll=URL + str(page) + '.htm'
#     print(urll)
#     r = requests.get(urll)
#     soup = BeautifulSoup(r.content, 'html.parser')
#     lines = soup.find_all('p')[1]
#     lines = str(lines)
#     pattern = re.compile("<(?:\"[^\"]*\"['\"]*|'[^']*'['\"]*|[^'\">])+>")
#     lines = re.sub(pattern,'',lines)
#     print(lines)
#     # for line in lines:
#     #     line = re.compile("<(?:\"[^\"]*\"['\"]*|'[^']*'['\"]*|[^'\">])+>")
#     #     print(line.text)
    
# import requests
# from bs4 import BeautifulSoup
# URL = 'https://www.sacred-texts.com/hin/rigveda/rv0'
# for page in range(1001, 1192):
#     urll=URL + str(page) + '.htm'
#     print(urll)
#     r = requests.get(urll)
#     soup = BeautifulSoup(r.content, 'html.parser')
#     lines = soup.find_all('p')[1]
#     for line in lines:
#         print(line.text)


from creds import cred
import requests
index_name = "vedic-index"
endpoint = cred.get("ACS_ENDPOINT")
credential = cred.get("ACS_API_KEY")
headers = {
    "Content-Type": "application/json",
    "api-key": credential,
}
search_url = f"{endpoint}/indexes/{index_name}/docs/search?api-version=2020-06-30"

search_body = {
    "count": True,
    "search": "arjun",
    "searchFields": "english_trans,context",
    "searchMode": "all",
    "select": "source, title, hindi_trans, english_trans, context",
    "top": 100,
}



response = requests.post(search_url, headers=headers, json=search_body).json()

print(response)

