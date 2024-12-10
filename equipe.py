class Equipe:
    def __init__(self, nom):
        self.nom = nom
        self.joues = 0              # Matchs joué
        self.gagnes = 0             # Matchs gagné
        self.nuls = 0               # Matchs nul
        self.perdus = 0             # Matchs perdu
        self.points = 0             # Points totaux
        self.butspours = 0
        self.butscontres = 0
        self.diffbut = 0
    def __str__(self):
        return f"{self.nom}: {self.points} points (Joués: {self.joues}, Gagnés: {self.gagnes}, Nuls: {self.nuls}, Perdus: {self.perdus}, Buts pour: {self.butspours}, Buts contre: {self.butscontres})"
    def maj_statistiques(self,resultat, s1,s2):
        self.joues+=1
        self.butspours+=s1
        self.butscontres+=s2
        self.diffbut += (s1-s2)
        if resultat == "gagne":
            self.gagnes += 1
            self.points += 3
        elif resultat == "nul":
            self.nuls += 1
            self.points += 1
        elif resultat == "perdu":
            self.perdus += 1

