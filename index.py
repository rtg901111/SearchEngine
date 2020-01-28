from bs4 import BeautifulSoup
import json
import os
import re
import csv
import pickle
from pymongo import MongoClient

def get_text(tag):
    text_list = []
    if len(tag) != 0:
        for h in tag:
            try:
                text_list.append(h.text)
            except:
                pass
    return text_list

def tokenize(textList, location):
    tokens = {}
    for text in textList:
        line = text.lower()
        word_list = re.findall("[a-z]+", line)
        for word in word_list:
            results = dict()
            if word not in tokens.keys():
                word_counter = 1
                results = {location:word_counter}
                tokens[word] = results
            elif word in tokens.keys():
                tokens[word][location] += 1
    return tokens

def parse_json_file():
    full_dict = dict()
    document_count = 0
    json_data = open('C:/Users/rtg90/Documents/CS 121/Assignment3/bookkeeping.json').read()
    base_path = 'C:/Users/rtg90/Desktop/CS 121/Assignment3/testwebpages/WEBPAGES_RAW'
    data = json.loads(json_data)
    for key in data.keys():
        print(base_path + '/' + key)
        file = open(base_path + '/' + key, 'r', encoding = 'utf-8')
        
        soup = BeautifulSoup(file, "html.parser")

        title = tokenize(get_text(soup.find_all("title")), key)
        h1 = tokenize(get_text(soup.find_all("h1")), key)
        h2 = tokenize(get_text(soup.find_all("h2")), key)
        h3 = tokenize(get_text(soup.find_all("h3")), key)
        b = tokenize(get_text(soup.find_all("b")), key,)
        body = tokenize(get_text(soup.find_all("body")), key,)
        body_raw = soup.find_all("body")
        strong = tokenize(get_text(soup.find_all("strong")), key)
        p = tokenize(get_text(soup.find_all("p")), key)
        a = tokenize(get_text(soup.find_all("a")), key)

        title_body = []
        for x in body_raw:
            if x.previousSibling != '\n':
                previous = str(x.previousSibling).replace('\n', '')
                if previous[len(previous) - 2] != '>':
                    title_body.append(previous)
                if previous[len(previous) - 2] == '>':
                    result = re.match('(.* ?)> ?(.*) ?', previous)
                    title_body.append(result.group(2))
        t_body = tokenize(title_body, key)

        for key,value in title.items():
            if key not in full_dict.keys(): 
                full_dict[key] = value
            elif key in full_dict.keys():
                full_dict[key].update(value)
        for key,value in h1.items():
            if key not in full_dict.keys():
                full_dict[key] = value
            elif key in full_dict.keys():
                full_dict[key].update(value)
        for key,value in h2.items():
            if key not in full_dict.keys():
                full_dict[key] = value
            elif key in full_dict.keys():
                full_dict[key].update(value)       
        for key,value in h3.items():
            if key not in full_dict.keys():
                full_dict[key] = value
            elif key in full_dict.keys():
                full_dict[key].update(value)
        for key,value in b.items():
            if key not in full_dict.keys():
                full_dict[key] = value
            elif key in full_dict.keys():
                full_dict[key].update(value)
        for key,value in body.items():
            if key not in full_dict.keys():
                full_dict[key] = value
            elif key in full_dict.keys():
                full_dict[key].update(value)
        for key,value in strong.items():
            if key not in full_dict.keys():
                full_dict[key] = value
            elif key in full_dict.keys():
                full_dict[key].update(value)
        for key,value in p.items():
            if key not in full_dict.keys():
                full_dict[key] = value
            elif key in full_dict.keys():
                full_dict[key].update(value)
        for key,value in a.items():
            if key not in full_dict.keys():
                full_dict[key] = value
            elif key in full_dict.keys():
                full_dict[key].update(value)
        for key,value in title.items():
            if key not in full_dict.keys():
                full_dict[key] = value
            elif key in full_dict.keys():
                full_dict[key].update(value)

    with open('indexfile.pickle', 'wb') as database:
        pickle.dump(full_dict, database, protocol = pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    parse_json_file()
