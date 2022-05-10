#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 13:59:31 2020

@author: tourist800
"""

from .ExtractNgrams import extract_ngrams
from .RemoveUnwantedCharacters import remove_unwanted_characters

def extract_ngrams_entity_list(str_entity):
  str_entity_list = []
  if len(extract_ngrams(remove_unwanted_characters(str_entity),1))!=0:
    for i in range(0,len(extract_ngrams(remove_unwanted_characters(str_entity),1)),1):
      str_entity_list.append(extract_ngrams(remove_unwanted_characters(str_entity),1)[i])

  if len(extract_ngrams(remove_unwanted_characters(str_entity),2))!=0:
    for i in range(0,len(extract_ngrams(remove_unwanted_characters(str_entity),2)),1):
      str_entity_list.append(extract_ngrams(remove_unwanted_characters(str_entity),2)[i])

  if len(extract_ngrams(remove_unwanted_characters(str_entity),3))!=0:
    for i in range(0,len(extract_ngrams(remove_unwanted_characters(str_entity),3)),1):
      str_entity_list.append(extract_ngrams(remove_unwanted_characters(str_entity),3)[i])

  return str_entity_list
