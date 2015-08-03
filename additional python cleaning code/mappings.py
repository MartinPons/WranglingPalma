# -*- coding: utf-8 -*-
# mappings.py
"""
Created on Wed Jul 22 17:05:39 2015

@author: Martin
"""
# Mapping for 'name' and 'street'
cami = "Camí ".decode("utf-8")
plaza = "Plaça ".decode("utf-8")
mapping = { "carrer ": "Carrer ",
           "Calle ": "Carrer ",
           "CALLE ": "Carrer ",
           "Carre ": "Carrer ",
           "C/ ": "Carrer ",
           "c/ ": "carrer ",          
           "CL ": "Carrer ",
           "C\\.": "Carrer",
           "plaça ".decode("utf-8"): plaza,
           "Plaza ": plaza,
           "PLAZA ": plaza,
           "camí ".decode("utf-8") : cami,
           "Cami ": cami,
           "Camino ": cami,
           "CAMINO ": cami,
           "avinguda ": "Avinguda ",
           "Avenida ": "Avinguda ",
           "AVENIDA ": "Avinguda ",
           "Avgda ": "Avinguda ",
           "Paseo ": "Passeig ",
           "passeig ": "Passeig ",
           "carretera ": "Carretera ",
           "CARRETERA ": "Carretera ",
           "crta.": "Carretera",
           "CTA.": "Carretera ",
           "CR ": "Carretera ",  
           "^via": "Via",
           "Vía".decode("utf-8"): "Via"
            }
            
# Mapping for housenumber
housenumber_mapping = {"^sn$": "s/n",
                        "bajos": "",
                        "baixos": ""}
                        
                        
# Mapping for Palma city denomination in 'city' tag
palma_mapping = {"palma": "Palma",
                      "Palma de Mallorca": "Palma",
                      "palma de mallorca": "Palma", 
                      "Palma - Illes Balears": "Palma"}
                      
                      
                