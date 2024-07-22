import pandas as pd
import json

with open('student.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

if isinstance(data, list):
    df = pd.DataFrame(data)
else:
    df = pd.json_normalize(data)

df.to_csv('student.csv', index=False)