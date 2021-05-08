# -*- coding: utf-8 -*-
"""
Created on Sat May  8 00:49:03 2021

@author: Pedro
"""

#followed this guide for this first draft: https://www.vipinajayakumar.com/parsing-text-with-python/

import re
import csv
import os

results = []
scrambles = []
datetimes = []

arquivo = "bora_testar.txt"
open(arquivo, 'w').close()

rx_dict = {
    'result': re.compile(r'\..*$'),
    #todo write re expression for scramble that doesn't rely on the being a ' in the scramble
    'scramble': re.compile(r'.*\'.*'),
    #todo not match total solves at end of file and time of export of beggining of file
    'datetime': re.compile(r'.*:.*'),
}

def _parse_line(line):
    """
    Do a regex search against all defined regexes and
    return the key and match result of the first matching regex

    """

    for key, rx in rx_dict.items():
        match = rx.search(line)
        if match:
            return key, match
    # if there are no matches
    return None, None

#todo: simplificar essa função e a próxima
def write_csv_header (nomedoarquivo, string_campos):
    string_campos = string_campos.replace('\n','')
    lista_de_campos = string_campos.split(',')
    if nomedoarquivo in os.listdir():
        arquivoaberto = open(nomedoarquivo, mode='r+',
                                 encoding="utf-8", newline='')
        html = arquivoaberto.read()
        arquivoaberto.close()

        
        if lista_de_campos[0] not in html[:100]:
            arquivoaberto = open(nomedoarquivo, mode='w',
                                 encoding="utf-8", newline='')
            arquivoaberto_csv = csv.writer(arquivoaberto, delimiter=',')
            arquivoaberto_csv.writerow(lista_de_campos)
            arquivoaberto.close()
    else:
            arquivoaberto = open(nomedoarquivo, mode='w',
                                 encoding="utf-8", newline='')
            arquivoaberto_csv = csv.writer(arquivoaberto, delimiter=',')
            arquivoaberto_csv.writerow(lista_de_campos)
            arquivoaberto.close()

def write_csv_lines (nomedoarquivo, dados):
    if dados != []:
        arquivoaberto = open(nomedoarquivo, mode='a+',
                             encoding="utf-8", newline='')
        arquivoaberto_csv = csv.writer(arquivoaberto, delimiter=',', quotechar = '"')
        arquivoaberto_csv.writerows(dados)
        arquivoaberto.close()
                   
def parse_file(filepath):

    # open the file and read through it line by line
    with open(filepath, 'r') as file_object:
        line = file_object.readline()
        
        while line:
            # at each line check for a match with a regex
            key, match = _parse_line(line)
            
            
            # extract result
            if key == 'result':
                result_raw = match.group()
                result_clean = result_raw.replace(". ", "")
                results.append(result_clean)

            # extract scramble
            if key == 'scramble':
                scrambles.append(match.group())

            # extract datetime
            #todo converte datetime string to actual datetime
            if key == 'datetime':
                datetimes.append(match.group())
            
            line = file_object.readline()

filepath = 'meuarquivo_teste.txt'
parse_file(filepath)

attempts = []
attempt_index = 0

for attempt in results:
    join = [results[attempt_index], scrambles[attempt_index], datetimes[attempt_index]]
    attempts.append(join)
    attempt_index = attempt_index + 1
    
campos = "resultado, embaralhamento, hora"

write_csv_header(arquivo, campos)
write_csv_lines(arquivo, attempts)