import os
import requests
import uuid
import pandas as pd 

def set_output(name, value):
    with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        print(f'{name}={value}', file=fh)

# def set_multiline_output(name, value):
#     with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
#         delimiter = uuid.uuid1()
#         print(f'{name}<<{delimiter}', file=fh)
#         print(value, file=fh)
#         print(delimiter, file=fh)
        
filename = os.environ.get("INPUT_FILENAME")
api_url = "https://endoflife.date/api/mssqlserver.json"
response = requests.get(api_url)
data = pd.read_csv(filename, dtype=str) 
df = pd.DataFrame(data)

for index, row in df.iterrows():
    print(row['name'], row['version'], row['eol'])
    api_url = "https://endoflife.date/api/" + row["name"] +".json"
    response = requests.get(api_url)
    if response.status_code == 200:
        for r in response.json():
            if r['cycle'] == row['version']:
                data.loc[index, 'eol'] = r['eol']
        data.to_csv("AllDetails.csv", index=False) 

print(data) 

# set_output("num", 1)
# print(os.environ['GITHUB_OUTPUT'])