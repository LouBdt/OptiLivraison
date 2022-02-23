import openpyxl
import xlrd
import fonctions as f
import numpy as np
import numpy.random as r
import matplotlib.pyplot as plt


def main(override, cps, BDDGeoloc):
    nombre_dessais = 1000
    echantillon = []
    if not override:
        CP_depart = input("Code postal de départ:")
        codePostaux = [CP_depart]
        cp = CP_depart
        i = 1
        while cp!="":
            try:
                cp = int(input("CP n°"+str(i)+':'))
                codePostaux.append(int(cp))
                i+=1
            except ValueError:
                break
            
        for cp in codePostaux:
            trouve = False
            for i in BDDGeoloc:
                if float(cp) == i[0]:
                    echantillon.append(i)
                    trouve = True
                    break
            if not trouve:
                print("Code postal introuvé ("+str(int(cp))+")")
                cp = int(input("Remplacer par:"))
    else:
        for cp in cps:
            trouve = False
            for i in BDDGeoloc:
                if float(cp) == i[0]:
                    echantillon.append(i)
                    trouve = True
                    break
            if not trouve:
                print("Code postal introuvé ("+str(int(cp))+")")
                cp = int(input("Remplacer par:"))
    masse = 0
    echantillon[0].append(0)
    if not override:
        for cp in echantillon[1:]:
            try:
                print("(indiquer 0 si c'est le point de départ)")
                masse = int(input("Masse (kg) à livrer au CP "+str(int(cp[0]))+':'))
                cp.append(masse)
            except ValueError:
                break
    else:
        for cp in echantillon[1:]:
            try:
                cp.append(r.randint(10,9999,1)[0])
            except ValueError:
                break
    print("=============================")
    for point in echantillon:
        print(point[1]+'('+str(int(point[0]))+'): '+str(point[4])+'kg')
    print("=============================")
    meilleur = []
    tous = []
    echantillon[-1].append(0)
    ordres = f.permute([k for k in range(1,len(echantillon))])
    meilleurBCpourN = np.inf
    pire = []
    worstpath = []
    worst = -np.inf
    for ordre in ordres:
        ordre = [0]+[k for k in ordre]+[0]
        bc = f.BC_chemin(ordre,echantillon)
        tous.append([len(echantillon), bc, ordre])
        if bc < meilleurBCpourN:
            meilleurBCpourN = bc
            meilleurCheminpourN = ordre
        elif bc> worst:
            worst = bc
            worstpath = ordre
    meilleur.append([len(echantillon), meilleurBCpourN, meilleurCheminpourN])
    pire.append([len(echantillon), worst, worstpath])
    ordre_moyen = f.court_trajet(echantillon)+[0]
    ordre_moyen2 = list(reversed(ordre_moyen))
    BC_ordre_moyen = f.BC_chemin(ordre_moyen, echantillon)
    BC_ordre_moyen2 = f.BC_chemin(ordre_moyen2, echantillon)
    if BC_ordre_moyen2>BC_ordre_moyen:
        ordre_moyen = ordre_moyen
        BC_ordre_moyen = BC_ordre_moyen
    else:
        ordre_moyen = ordre_moyen2
        BC_ordre_moyen = BC_ordre_moyen2
    moyen = [[len(echantillon),BC_ordre_moyen,ordre_moyen]]
    if True:
        plt.figure()
        plt.scatter([k[0] for k in tous],[k[1] for k in tous], color = 'grey')
        plt.scatter([k[0] for k in meilleur],[k[1] for k in meilleur], color = 'green')
        plt.scatter([k[0] for k in moyen], [k[1] for k in moyen], color = 'blue')
        plt.xlabel("Nombre de points livrés")
        plt.ylabel("Bilan carbone (kgCO2e)")
        labels = [str(k[2]) for k in meilleur+moyen+pire]
        for i, label in enumerate(labels):
            plt.annotate(label, ([float(k[0]) for k in meilleur+moyen+pire][i],[float(k[1]) for k in meilleur+moyen+pire][i]))
        plt.show()
    
    f.tracerChemin(moyen[0], echantillon, 'blue', "Shortest Path")
    # f.tracerChemin(pire[0], echantillon, 'grey', "Worst path")
    f.tracerChemin(meilleur[0], echantillon, 'green', "Low carbon Path")
    print("Le trajet vert est "+str(int(100*(meilleurBCpourN-BC_ordre_moyen)/BC_ordre_moyen))+"% moins émissif que le trajet bleu")
    # print("Le trajet vert est "+str(int(100*(meilleurBCpourN-worst)/worst))+"% moins émissif que le trajet gris")
    return (meilleurBCpourN-BC_ordre_moyen)/BC_ordre_moyen


MULTITEST = True

BDDGeoloc = f.lireGeo("BDDgeoloc.xlsx")
if MULTITEST:
    iterations = 100
    minimum_points = 5      #En dessous de 5 c'est pas très intéressant
    maximum_points = 11     #12 maximum, au-delà c'est très long
    codes_p = [i for i in range(1000, 96000, 1000)]
    x =[]
    y = []
    for i in range(minimum_points,maximum_points):
        
        for j in range(iterations):
        
            x.append(i)
            sample = r.randint(0,len(codes_p),i)
            print("Test n°" + str((i-minimum_points)*iterations+j))
            score = abs(100*main(True,[codes_p[k]for k in sample],BDDGeoloc))
            y.append(score)
        
    E = [[j,[y[i] for i in range(len(y)) if x[i]==j]] for j in range(minimum_points,maximum_points)]
    moyennes = [[],[]]
    for i in E:
        try:
            moyenne = sum(i[1])/len(i[1])
        except ZeroDivisionError:
            moyenne = 0
        moyennes[0].append(i[0])
        moyennes[1].append(moyenne)
        i[1] = moyenne
    plt.figure()
    plt.xlabel('Nombre de points livrés')
    plt.ylabel('Avantage carbone du trajet vert (%)')
    plt.scatter(x,y, c = 'b')
    plt.title('En rouge la moyenne')
    plt.scatter(moyennes[0],moyennes[1], c = 'r')
    print("En moyenne, les trajets verts permettent d'émettre "+str(int(10*sum(moyennes[1])/len(moyennes[1]))/10)+"% moins que les trajets les plus courts, en bleu")
else:
    score = abs(100*main(False,[],BDDGeoloc))
    print("Le bilan carbone du trajet optimisé est "+str(score)+"% moins émissif que le plus court trajet")
    