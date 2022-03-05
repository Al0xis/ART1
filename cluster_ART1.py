# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 13:58:28 2022

@author: alexi
"""

import numpy as np
import random 

def filled_samples(_sample, _number_samples, _number_features):
    for i in range(_number_samples):
        for j in range(_number_features + 1):
            if (j == _number_features):
                _sample[i, number_features] = -1
            else:
                _sample[i, j] =  random.randint(0, 1)
                
def proximity_test(_sample, _prototype, _number_elements, _beta):
    v_and = np.zeros(_number_elements)
    vector_and(_sample, _prototype, v_and, _number_elements)
    mag = magnitude(v_and, _number_elements)
    term_l = mag/(_beta + magnitude(_prototype, _number_elements))
    term_r = magnitude(_sample, _number_elements)/(_beta + _number_elements)
    if (term_l > term_r): 
        return 1
    else:
        return 0
        
    
def vector_and(_vector1, _vector2, _v_and, _number_elements):
    for i in range(_number_elements):
        if(_vector1[i] == 1 and _vector2[i] == 1):
            _v_and[i] = 1
        else:
            _v_and[i] = 0

def magnitude(_vector, _number_elements):
    mag = 0
    for i in range(_number_elements):
        mag += _vector[i]
    return mag

def vigilance_test(_sample, _prototype, _number_elements, _rho):
    v_and = np.zeros(_number_elements)
    vector_and(_sample, _prototype, v_and, _number_elements)
    mag = magnitude(v_and, _number_elements)
    term_l = mag/magnitude(_sample, _number_elements)
    if(term_l >= _rho):
        return 1
    else:
        return 0

def vector_merge(_vector1, _vector2,_number_elements):
    for i in range(_number_elements):
        if(_vector1[i] == 0 or _vector2[i] == 0):
            _vector2[i] = 0

def vector_copy(_vector1, _vector2, _number_elements):
    for i in range(_number_elements):
        _vector2[i] = _vector1[i]
        
def make_recommendation(_samples_in_cluster, _index, _samples, _number_samples, _number_features, _prototype):
    beer_list = ["Corona", "Tecate", "Modelo", "Victoria", "Indio", "XX", "Leon", "Pacifico", "Bohemia", "Sol"]
    index_sample = np.zeros(int(_samples_in_cluster))
    aux = 0
    for i in range(_number_samples):
        if (sample[i, _number_features] == _index):
            index_sample[aux] = i
            aux += 1
    frecuency_options = np.zeros(_number_features)
    for i in range(len(index_sample)):
        for j in range(number_features):
            if(sample[int(index_sample[i]), j] == 1):
                frecuency_options[j] += 1
    index_recommendation = np.argwhere(frecuency_options == (int(_samples_in_cluster)-1))
    sample_for_recommendation = np.zeros(len(index_recommendation))
    aux2 = 0
    for i in range(len(index_sample)):
        for j in range(len(index_recommendation)):
            if (sample[int(index_sample[i]), int(index_recommendation[j])] == 0):
                sample_for_recommendation[aux2] = int(index_sample[i]);
                aux2 += 1
    if (len(sample_for_recommendation) == 0):
        print("It's not possible to give a recommendation for this cluster because it doesn't meet the requirements to give one")
    else:
        for i in range(len(sample_for_recommendation)):
            print("The recommendation for sample", int(sample_for_recommendation[i]), "it's", 
                  beer_list[int(index_recommendation[i])], "because it's a member of the other samples")
            
    
number_samples = int(input("Number of samples: "))
number_features = 10

sample = np.zeros([number_samples, number_features+1])

filled_samples(sample, number_samples, number_features)

beta = 1.0
rho = 0.5
number_prototypes = 0
prototype = np.copy(sample)
sample[0, number_features] = 0
number_prototypes += 1; 

print("\nThis algorithm classifies the preferences of consumers of the following beers brands:")
print("Corona, Tecate, Modelo, Victoria, Indio, XX, Leon, Pacifico, Bohemia, Sol")

print("\nThe following", number_samples, "samples will be grouped:\n")
for i in range(number_samples):
    print("Sample", i+1, ":", sample[i, 0:number_features-1])

for i in range(number_samples):
    merged = 0
    for j in range(number_prototypes):
        if(proximity_test(sample[i], prototype[j], number_features, beta)) and vigilance_test(sample[i], prototype[j], number_features, rho):
            vector_merge(sample[i], prototype[j], number_features)
            sample[i, number_features] = j
            merged = 1
            break
    if (not merged):
        vector_copy(sample[i], prototype[number_prototypes], number_features)
        sample[i, number_features] = number_prototypes
        number_prototypes += 1
        
print("\nFinally,", number_prototypes, "clusters were found.")
for i in range(number_prototypes):
    print("\nCluster", i+1, "=>" ,prototype[i, 0:number_features], "includes:")
    for j in range(number_samples):
        if (sample[j, number_features] == i):
            print("Sample", j, " :", sample[j, 0:number_features])
            
samples_in_cluster = np.zeros(number_prototypes)

for i in range(number_prototypes):
    for j in range(number_samples):
        if(sample[j, number_features] == i):
            samples_in_cluster[i] += 1

clusters_for_recommendation = np.argwhere(samples_in_cluster >= 4)

if (clusters_for_recommendation.size == 0):
    print("\nThere's no clusters with enough information for a recommendation to be made.")
else:
    for i in range(len(clusters_for_recommendation)):
        print("\nRECOMMENDATIONS FOR CLUSTER", int(clusters_for_recommendation[i])+1, ":")
        make_recommendation(samples_in_cluster[int(clusters_for_recommendation[i])], int(clusters_for_recommendation[i]), sample, number_samples, number_features, prototype)
    