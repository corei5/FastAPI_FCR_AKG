#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 13:02:47 2020

@author: tourist800
"""
import string
#remove other languages
def isEnglish(word):
    char_set = string.ascii_letters
    return all((True if x in char_set else False for x in word))