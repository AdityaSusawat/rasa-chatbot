import requests

api_key = r"579b464db66ec23bdd000001aa1c0850484747ec544a2f2b1a952d6c"
outputformat = r"json"
records = 5000
request = r'https://api.data.gov.in/catalog/19ba71d9-6d58-402d-9b75-a0ebdc034a56?api-key='+api_key+'&format='+outputformat+'&limit='+str(records)
response = requests.get(request)
data = eval(response.text)

data['records'][4999]

category = []
crop = []
querytype = []
querytext = []
kccans = []
identifier = []

for i in range(0,1000):
    category.append(data['records'][i]['category'])
    crop.append(data['records'][i]['crop'])
    querytype.append(data['records'][i]['querytype'])
    identifier.append(i)
    querytext.append(data['records'][i]['querytext'])
    kccans.append(data['records'][i]['kccans'])

import pandas as pd
df = pd.DataFrame()

df["category"] = category
df["crop"] = crop
df["querytype"] = querytype
df["querytext"] = querytext
df["kccans"] = kccans
df['identifier'] = identifier

df["intent"] = df["category"]+df["crop"]+df["querytype"]#+df["identifier"]

import re
def cleanString(x):
    return re.sub('[^A-Za-z0-9]+', '', x)
df["intent"] = df.apply(lambda x: cleanString(str(x["intent"])), axis =1)
df["intent_md"] = "## intent:" + df["intent"]
df["intent_*"] = "* " + df["intent"]
df["intent_-"] = "- " + df["intent"]
df["querytext_md"] = "- " + df["querytext"]
df_pivot = df.pivot_table(index=['intent_md'],
                                     values='querytext_md',
                                     aggfunc=lambda x: '\n'.join(x)).reset_index()

for i,j in zip(df_pivot["intent_md"], df_pivot["querytext_md"]):
    with open('intent.md', 'a') as f:
        print(i, '\n', j, file = f)
    f.close()
    
df["actions_md"] = "utter_" + df["intent"]
df["query_md"] = "## query_" + df["intent"]
df["actions_-"] = "- " + df["actions_md"]
df["actions_:"] = df["actions_md"] + ":"

def cleanAnswer(x):
    return re.sub('[^A-Za-z0-9]+', ' ', x)
df["kccans"] = df["kccans"].replace(r'\\n','', regex=True) 
df["kccans"] = df.apply(lambda x: cleanAnswer(str(x["kccans"])), axis =1)
df["kccans_text"] = '- text: "' + df["kccans"] + '"'
df2 = df[["actions_:","kccans_text"]].drop_duplicates(["actions_:"])
df3 = df[["query_md","intent_*","actions_-"]].drop_duplicates(["intent_*"])