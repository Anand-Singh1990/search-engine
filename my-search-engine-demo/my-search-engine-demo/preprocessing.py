# from pathlib import Path
# import json
#from dataclasses import dataclass
#from dataclasses_json import dataclass_json
# import csv

# @dataclass_json
# @dataclass(order=True, frozen=True)
# class Article:
#     """The data model for processed articles
#     """
#     id: str
#     timestamp: str
#     source: str
#     title: str
#     body: str

from pathlib import Path
import json
import csv
from BhagvadGita2 import data
source_articles = open('data.csv')
csvreader = csv.reader(source_articles)

dataset=[]
count_i = 0
count_j = 0
for i in csvreader:
    sno = i[0]
    title = i[1]
    chapter = i[2]
    verse = i[3]
    sanskrit_trans = i[4]
    hindi_trans = i[5]
    english_trans = i[6]
    value=""
    #print(len(data))
    count_j = 46
    for j in data:
        if count_j>len(data)+46:
            break
        #print(j)
        print(count_i,"----------",count_j)
        if count_j == count_i:
            #print(j.get("body"))
            value = j.get("body")
            count_j = count_j+1
            break
        count_j = count_j+1
    count_i = count_i+1
    dataset.append({
        "source":"Bhagvad Gita",
        "sno":sno,
        "title":title,
        "chapter":chapter,
        "verse":verse,
        "sanskrit":sanskrit_trans,
        "hindi_trans":hindi_trans,
        "english_trans":english_trans,
        "context":value

    }
    )
    


json_object = json.dumps(dataset,ensure_ascii=False,indent=4)

# print(json_object)
 
# Writing to sample.json
with open("sample.json", "w") as outfile:
    outfile.write(json_object)



# destination_articles = Path(__file__).resolve().parent.parent.parent / 'data' / 'aylien_covid_news_data_sample.jsonl'



# with open(source_articles,'r') as source_file:
#     with open(destination_articles, 'w') as destination_file:
#         for i in range(5000):
#             line = source_file.readline()
#             json_line = json.loads(line)
#             id = str(json_line.get('id'))
#             timestamp = json_line.get('published_at')
#             source = json_line.get('source').get('domain')
#             title = json_line.get('title')
#             body = json_line.get('body')

#             mini_article = Article(id=id, timestamp=timestamp, source=source, title=title, body=body)
#             destination_file.write(mini_article.to_json()+'\n')

    
    
