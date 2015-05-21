#!/usr/bin/env python
# -*- coding: utf-8 -*-

# imports
import json
import logging
from wxPython._wx import NULL
from warnings import catch_warnings
from __builtin__ import dict
import sys


#Function to load json objects from strings
def open_json(line):
    try:
        return json.loads(line.strip())
    except:
        logging.warning("Not possible parse object json : " + line)
        return

#Function which make a dictionary using the product_id as keys to the recommendation algorithm
def func_product_index(list):
    mat = {}
    for element in list:
        
        if(mat.has_key(element["product_id"])):
            mat[element["product_id"]].append(element["user_id"])
        else:
            mat[element["product_id"]] = [element["user_id"]]
        
    return mat            

#Function which make a dictionary with the product_id and the products correlated and your similarity           
def calc_similarity_dict(dic,max_list):
    sim = {}
    
    for key1 in dic.keys():
        for key2 in dic.keys():
            if (key1 != key2):
                if(sim.has_key(key1)):
                    if (len(sim[key1])<max_list):
                        sim[key1].append((key2,calc_similarity(dic[key1], dic[key2])))
                    else:
                        sim[key1].append((key2,calc_similarity(dic[key1], dic[key2])))
                        sim[key1].sort(key=lambda x: x[1],reverse=True)
                        sim[key1].pop();
                else:
                    sim[key1] = [(key2,calc_similarity(dic[key1], dic[key2]))]
    return sim
                       

#Function which calc the number of similarity of tho products,from their lists of user_id
def calc_similarity(list1,list2):
    c_exist = 0.
    c_total = 0.
    for elem in list1:
        if (elem in list2):
            c_exist = c_exist +1
        c_total = c_total +1 
    return c_exist/c_total

#Function which write the strings in file
def writing(msg,arquivo):
    try:
        f = open(arquivo,'a')
        f.write(msg+"\n")
        f.close()
    except:
        f = open(arquivo,'w')
        f.write(msg+"\n")
        f.close()

#Function main of the Script,Does the calling functions to process the data and make the recommendation system
def desafio_chaordic():
    try:
        arquivo = sys.argv[1]
    except:
        logging.error("Arquivo não passado como parametro")
        exit()
        
    list = []

#Try to open the file in the event error exit the program
    try:
        arq = open(arquivo)
    except:
        logging.error("Arquivo não encontrado")
        exit()
        
#Call the function which read the file and mount a list with json objects       
    for line in arq:
        ret = open_json(line)
        if ret!=NULL:
            list.append(ret)

# Call the function which mount a dict with product_id how the key and the list of users with elements, from the list of jsons
    dict = func_product_index(list)
    
# Call the function which mount the dict with the product_id how a key and the list of similarity with other products_id with elements, from the dict of products_id
    dict_similarity = calc_similarity_dict(dict,40)

# Treats dict_similarity to be written in file into the desired shape
    for key in dict_similarity.keys():
        string_final = '{ "reference_product_id": ' + str(key) + ', "recommendations": ['
        for similarity in dict_similarity[key]:
            string_final = string_final+ '{"product_id": ' + str(similarity[0]) + ', "similarity": ' + str(similarity[1]) + "},"
        string_final =  string_final[0:len(string_final)-1] +  "]}"
        writing(string_final, arquivo.split(".")[0]+"_output."+arquivo.split(".")[1])
    
    
        

desafio_chaordic()
    
        
