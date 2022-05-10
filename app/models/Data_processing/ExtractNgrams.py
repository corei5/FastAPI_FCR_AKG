#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 13:52:07 2020

@author: tourist800
"""


import nltk
from nltk.util import ngrams
nltk.download('punkt')


# Function to generate n-grams from entitie.
def extract_ngrams(data, num):
    n_grams = ngrams(nltk.word_tokenize(data), num)
    return [ '_'.join(grams) for grams in n_grams]