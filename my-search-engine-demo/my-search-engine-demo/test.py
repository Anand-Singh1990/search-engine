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