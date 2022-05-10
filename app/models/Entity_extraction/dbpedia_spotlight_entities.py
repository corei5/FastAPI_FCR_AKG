import numpy as np
import requests
import json

def annotate_text(text):
    base_url = "http://api.dbpedia-spotlight.org/en/annotate"
    #base_url = "Enter the URL of your DBPedia server"
    params = {"text": """{}""".format(text),
              "confidence": 0.35}
    headers = {'accept': 'application/json'}
    res = requests.get(base_url, params=params, headers=headers)
    if res.status_code != 200:
        raise APIError(res.status_code)
    data = json.loads(res.text)
    return data

def dbp(text):
    data = annotate_text(text)
    entities=[]
    if ("Resources" in data):
        resources = data["Resources"]
        entities = list()
        for each in resources:
            entity = each["@surfaceForm"]
            if entity not in entities:
                entities.append(entity)
    entities_str = ' , '.join(entities)
    if len(entities_str)>1:
        return entities_str
    else:
        return np.nan