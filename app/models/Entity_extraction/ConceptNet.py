import hashlib
import json
import requests
import numpy as np
from Data_preprocessing.Data_Clean import CheckLanguage, IsNotAscii, RemoveUnwantedCharacters
from Data_preprocessing.Ngrams import ExtractNgrams, ExtractNgramsEntityList


def conceptNetExpansion(entitiesToExpand_str):
    debug = False
    entityDict = {}
    entityListAll = []


    if type(entitiesToExpand_str) != float:

        entitiesToExpand = entitiesToExpand_str.split(',')
        i = 0
        for entity in entitiesToExpand:
            expandedEntities = set()
            i = i + 1
            str_entity = entity.lower().rstrip().lstrip()

            if len(str_entity.split(" ")) > 1:
                entityList = ExtractNgramsEntityList.extract_ngrams_entity_list(str_entity) + [str_entity]
            else:
                entityList = [str_entity]

            for internal_entity in entityList:
                if type(internal_entity) == int:
                    continue
                hash_object = hashlib.md5(internal_entity.encode('utf-8'))
                filename = hash_object.hexdigest()
                try:
                    with open('cache/ConceptNet/' + filename + ".json", 'r') as cachefile:
                        obj = json.load(cachefile)
                    #                         if debug:
                    #                             print("Read from cache " + filename)
                    #                         else:
                    #                             print("c" + filename, end='')
                except IOError:
                    url = 'http://api.conceptnet.io/c/en/' + internal_entity
                    obj = requests.get(url).json()
                    with open('cache/ConceptNet/' + filename + ".json", 'w') as outfile:
                        json.dump(obj, outfile)

                for edge in obj['edges']:
                    entityLinkedAsStart = str(edge['start']['label'])
                    entityLinkedAsEnd = str(edge['end']['label'])  # str(obj['edges'][i]['end']['label'])
                    if CheckLanguage.isEnglish(entityLinkedAsStart):
                        expandedEntities.add(entityLinkedAsStart)
                    if CheckLanguage.isEnglish(entityLinkedAsEnd):
                        expandedEntities.add(entityLinkedAsEnd)

            for entity in expandedEntities:
                entityListAll.append(entity)

    else:
        return np.nan

        return ','.join(entityListAll)
