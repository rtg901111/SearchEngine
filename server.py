from bottle import route, request, response, run
import pickle
import json
import math
import re


file = open("./indexfile.pickle", "rb")
full_dict = pickle.load(file)
urlDict = json.loads(open("./testwebpages/WEBPAGES_RAW/bookkeeping.json").read())
file.close()


def order(query: str):
    try:
        query_words = query.split()
        docList = {}
        for key in query_words:
            dft = len(full_dict[key])  # dft is the number of documents containing the word

            for k, v in full_dict[key].items():  # key = ( folder, file) value = frequency of the word
                tftd = 1+ math.log(v)  # tftd = number of occurrences of t in document d : (1 + log(tftd))
                N = 37497  # N is the total # of documents in the corpus
                wtd = tftd * math.log(N / dft)

                title_text = urlDict[k[0]]

                if urlDict[k[0]] in docList:
                    docList[(k,title_text)] = docList[(k,title_text)] + wtd
                else:
                    docList[(k,title_text)] = wtd
        return sorted(docList, key=lambda key: docList[key], reverse=True)
    except KeyError:
        print("KeyError")
        return []


@route("/")
def home():
    q = request.query.q.lower()
    print(q)
    calculation=None
    try:
        if re.match("^[^A-Z,a-z]*$", q):
            calculation = eval(q)
    except:
        pass

    url_list = order(q)
    total_results = len(url_list)
    url_list = url_list[:20]

    response.add_header("Access-Control-Allow-Origin","*")
    print("done")
    return json.JSONEncoder().encode({
        "calculation": calculation,
        "urlList": url_list,
        "query": q,
        "totalResults": total_results
    })


run(host="localhost", port=8000, debug=True)

