# coding=utf-8

import os
import pickle

class Mouvements():
    """docstring for """
    def __init__(self, tabMouvementDoigt):
        #1 tablepar doigt
        self.tabMouvementDoigt = normalized_tab(tabMouvementDoigt)


    #enregistre le mouvement dans un fichier
    def save_to_file(self,filename):
        with open(filename,"wb") as fichier:
            pickler = pickle.Pickler(fichier)
            pickler.dump(self)

    #enregistre en svg si on veut visualiser le mouvement (peut etre utile pour le debug)
    def save_to_svg(self,filename):
        with open(filename, "wb") as fichier:
            xmax,ymax = find_max(self.tabMouvementDoigt)
            fichier.write('''<?xml version="1.0" encoding="utf-8"?>\n
<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="'''+str(xmax*2+10)+'''" height="'''+str(ymax*2+10)+'''">\n''')
            for soustab in self.tabMouvementDoigt:
                i=0
                while i < len(soustab)-1:
                    fichier.write('<line x1="'+str(soustab[i][0]+xmax+5)+'" y1="'+str(soustab[i][1]+ymax+5)+'" x2="'+str(soustab[i+1][0]+xmax+5)+'" y2="'+str(soustab[i+1][1]+ymax+5)+'" stroke="red" />')
                    i=i+1

            fichier.write('</svg>')

    #compare deux mouvement pour voir si il se ressemble
    def look_like(self,mouv, sensibilite=100):
        #si ce sont exactement les memes ont valide
        if self.tabMouvementDoigt== mouv.tabMouvementDoigt:
            return True
        #si il n'y a pas le meme nombre de doigt c'est faux
        if len(self.tabMouvementDoigt) != len(mouv.tabMouvementDoigt):
            return False
        i=0
        while i<len(self.tabMouvementDoigt):
            if(abs(len(self.tabMouvementDoigt[i])-len(mouv.tabMouvementDoigt[i]))>10):
                return False
            j=0
            k=0
            error=0
            meFaster=(len(self.tabMouvementDoigt[i])<len(mouv.tabMouvementDoigt[i]))
            while (j<len(self.tabMouvementDoigt[i])-1 and k<len(mouv.tabMouvementDoigt[i])-1):
                l=1
                m=1
                while True:
                    #calcul de la direction pour comparer les deux
                    sdx=self.tabMouvementDoigt[i][j][0]-self.tabMouvementDoigt[i][j+l][0]
                    sdy=self.tabMouvementDoigt[i][j][1]-self.tabMouvementDoigt[i][j+l][1]+0.001
                    sd=sdx/sdy
                    mdx=mouv.tabMouvementDoigt[i][k][0]-mouv.tabMouvementDoigt[i][k+m][0]
                    mdy=mouv.tabMouvementDoigt[i][k][1]-mouv.tabMouvementDoigt[i][k+m][1]+0.001
                    md=mdx/mdy
                    print i,j,k,l,m,sd,md
                    #en fonction de la sensibilite on valide ou  pas la portion de déplacement
                    if (abs(sd-md)<sensibilite and (sdx/(mdx+0.001)>=0 and sdy/(mdy+0.001)>=0)):
                        break

                    # on a le droit a une erreure au dessus de la marge par doigt
                    if error==0:
                        error+=1
                        break

                    #test pour voir si il n'y a pas des positions que l'on aurait loupé
                    if meFaster and m<5 and k+m<len(mouv.tabMouvementDoigt[i])-1:
                        m=m+1
                    elif meFaster and l<5 and j+l<len(self.tabMouvementDoigt[i])-1:
                        l=l+1
                    elif (not meFaster) and l<5 and j+l<len(self.tabMouvementDoigt[i])-1:
                        l=l+1
                    elif (not meFaster) and m<5 and k+m<len(mouv.tabMouvementDoigt[i])-1:
                        m=m+1
                    else:
                        return False
                j=j+l
                k=k+m
            i=i+1

        return True

    @staticmethod
    def read_from_file(filename):
        with open(filename,"rb") as fichier:
            unpickler=pickle.Unpickler(fichier)
            mouv=unpickler.load()
            return mouv

#centre les table pour que la première position soit 0,0
def normalized_tab(tab):
    center=tab[0][0]
    newtab=[]
    for soustab in tab:
        newsoustab=[]
        for c in soustab:
            newsoustab.append((c[0]-center[0],c[1]-center[1]))
        newtab.append(newsoustab)
    return newtab

# recherche un maximum dans les tables
def find_max(tab):
    xmax=0
    ymax=0
    for soustab in tab:
        for c in soustab:
            xmax = max(xmax, abs(c[0]))
            ymax = max(ymax, abs(c[1]))
    return (xmax,ymax)

if __name__ == '__main__':
    tab = [[(1,2),(5,6),(7,8)],[(2,3),(5,14)]]
    print tab
    print normalized_tab(tab)
    mouv=Mouvements(tab)
    mouvbis=Mouvements([[(3,4),(0,8)],[(2,3),(5,14)]])
    mouv.save_to_file("MouvTest")
    print mouv.tabMouvementDoigt== Mouvements.read_from_file("MouvTest").tabMouvementDoigt
    mouv.save_to_svg("MouvTest.svg")
    mouvbis.save_to_svg("MouvBis.svg")
    print mouv.look_like(mouvbis)
