# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 09:41:28 2022

@author: mar_altermark
"""
import xlrd
import openpyxl
import sys
import math
import numpy as np
import numpy.random as r
import matplotlib.pyplot as plt

def lire(chemin):
    try:
         document = xlrd.open_workbook(chemin)
    except FileNotFoundError:
         sys.exit("Le fichier d'extraction n'est pas trouvé à l'emplacement "+chemin)
    resultat = []
    feuille_bdd = document.sheet_by_index(0)
    nbrows = feuille_bdd.nrows
    colonnes = [0,2,1,3]
    for l in range(1, nbrows):
        ligne = []
        for c in colonnes:
            ligne.append(feuille_bdd.cell_value(l, c))
        resultat.append(ligne)
    return resultat

def lireGeo(chemin):
    try:
         document = xlrd.open_workbook(chemin)
    except FileNotFoundError:
         sys.exit("Le fichier d'extraction n'est pas trouvé à l'emplacement "+chemin)
    resultat = []
    feuille_bdd = document.sheet_by_index(0)
    nbrows = feuille_bdd.nrows
    colonnes = [1,3,6,7]
    for l in range(1, nbrows):
        ligne = []
        for c in colonnes:
            ligne.append(feuille_bdd.cell_value(l, c))
        resultat.append(ligne)
    return resultat

def distance(ptA, ptB):
    latA = ptA[3]
    longA = ptA[2]
    latB = ptB[3]
    longB = ptB[2]
    if latA==latB and longA==longB:
        return 0
    else:
        distance_VO = math.acos(math.sin(latA)*math.sin(latB)+math.cos(latA)*math.cos(latB)*math.cos(longB-longA))*6371
        distance_route =float( 1.4*distance_VO)
    return distance_route

def bilan_carboneAB(ptA, ptB, m0):
    masseA = ptA[4]
    return 1.4*(m0-masseA)*distance(ptA,ptB)*0.0919000/1000


def BC_chemin(ordre, points):
    BC = 0
    m0 = sum([points[k][4] for k in ordre])
    for i in range(len(ordre)-1):
        BC += bilan_carboneAB(points[ordre[i]], points[ordre[i+1]], m0)
        m0 = m0-points[ordre[i]][4]
    return BC

def evaluerChemin(ordre, points):
    m0 = sum([points[k][4] for k in ordre])
    return BC_chemin(ordre,points)/m0

def permute(arr):
    from itertools import permutations
    perms = permutations(arr) 
    return perms

def tracerChemin(ordres, points, color):
    m0 = sum([k[4] for k in points])
    m0_ = m0
    ordre = ordres[2]
    for i in range(len(ordre)-1):
        plt.plot([points[ordre[i]][2], points[ordre[i+1]][2]],[points[ordre[i]][3], points[ordre[i+1]][3]], color = color,linewidth=1+3*m0/m0_, zorder = 1)
        m0 -= points[ordre[i]][4]
    for i in points:
        if i==points[0]:
            plt.scatter([i[2]],[i[3]], color = 'green', zorder = 3)
        else:
            plt.scatter([i[2]],[i[3]], color = 'red', zorder = 2)
    labels = [str(int(i))+"/"+str(int(points[i][4]))+'kg-'+str(points[i][1]) for i in range(len(points))]
    for i, label in enumerate(labels):
        plt.annotate(label, (points[i][2], points[i][3]))
    labels = [str(i) for i in range(len(points))]
    plt.title('Bilan Carbone:'+str(int(ordres[1]))+'kgCO2e -  '+str(ordre))
    plt.show()
    
    
def court_trajet(points):
    pts = [[0,0,k[2], k[3]] for k in points]
    ordre = solve_tsp_dynamic(pts)
    
    
    return ordre
def solve_tsp_dynamic(pts): #https://gist.github.com/mlalevic/6222750
    import itertools    
    #calc all lengths
    all_distances = [[distance(pts[x], pts[y]) for y in range(len(pts))] for x in range(len(pts))]
    #initial value - just distance from 0 to every other point + keep the track of edges
    A = {(frozenset([0, idx+1]), idx+1): (dist, [0,idx+1]) for idx,dist in enumerate(all_distances[0][1:])}
    cnt = len(pts)
    for m in range(2, cnt):
        B = {}
        for S in [frozenset(C) | {0} for C in itertools.combinations(range(1, cnt), m)]:
            for j in S - {0}:
                B[(S, j)] = min( [(A[(S-{j},k)][0] + all_distances[k][j], A[(S-{j},k)][1] + [j]) for k in S if k != 0 and k!=j])  #this will use 0th index of tuple for ordering, the same as if key=itemgetter(0) used
        A = B
    try:
        res = min([(A[d][0] + all_distances[0][d[1]], A[d][1]) for d in iter(A)])
        return res[1]   
    except ValueError:
        fonctionsMatrices.print_log_erreur("Optimisation de la sous livraison n°"+str(int(0))+" impossible", inspect.stack()[0][3])
        return False
