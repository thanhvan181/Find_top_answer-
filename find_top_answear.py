import argparse
import time
import random
from requests_html import HTMLSession


parser = argparse.ArgumentParser()
parser.add_argument('N', help="Top N questions on stackoverflow", type=int)
parser.add_argument('label', help="tag of question on page", type=str)
args = parser.parse_args()

numbers = args.N
tag = args.label
session = HTMLSession()

url = ' https://api.stackexchange.com/'

query_string = f'2.2/questions?pagesize={numbers}&order=desc&sort=votes&tagged={tag}&site=stackoverflow'
r = session.get(url +query_string)

data = r.json()
# print(data)
items = [(item['title'], item['question_id'], item['link']) for item in data['items']]

query_answer = '2.2/questions/{}/answers?order=desc&sort=votes&site=stackoverflow'
result = []
session = HTMLSession()

for title, question_id, link in items:
    answer = session.get(url + query_answer.format(question_id))
    d_answer = answer.json()
    top_answer = d_answer['items'][0]
    answer_id = top_answer['answer_id']
    link_to_answer = link + f'/{answer_id}#{answer_id}'
    result.append([title, link_to_answer])
    time.sleep(random.randint(1,3))
for title, link_1 in result:
    print(f'{title}, link to top answer in top: \n {link_1}')