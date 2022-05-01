import requests
api_key = r"579b464db66ec23bdd000001aa1c0850484747ec544a2f2b1a952d6c"
outputformat = r"json"
records = 5000
request = r'https://api.data.gov.in/catalog/19ba71d9-6d58-402d-9b75-a0ebdc034a56?api-key='+api_key+'&format='+outputformat+'&limit='+str(records)
response = requests.get(request)
data = eval(response.text)

data['records'][4999]