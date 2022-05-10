#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 13:47:21 2020

@author: tourist800
"""
import re

#remove unwanted characters
def remove_unwanted_characters(entitie):
  return re.sub('[^A-Za-z0-9 ]+', ' ', entitie)