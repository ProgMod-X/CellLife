class Busk:
    bær = None #Antal bær busken har
    tid_til_bær = None #Kor mange runder igjen til busken får eit til bær
    veksetid = None #Kor lang tid det tar for busken å få eit til bær

    def __init__(self, bær, veksetid):
        self.bær = bær
        self.tid_til_bær = veksetid #Kor lang tid til neste bær startar som som veksetida
        self.veksetid = veksetid
    
    def veks(self): #Denne skal kjørast kvar runde og gjer at busken anten får eit til bær, eller i det minste kjem nærmare eit til.
        self.tid_til_bær -= 1
        if self.tid_til_bær == 0:
            self.bær += 1
            self.tid_til_bær = self.veksetid
    
    def spis(self): #Denne funksjonen skal kjørast når ein celle vil spisa ein busk. Dersom funksjonen returnerer false, er det ikkje meir bær igjen, og cella kan ikkje spisa. Dersom det er true, kan cella spisa, og busken har eit færre bær.
        if self.bær == 0:
            return False
        else:
            self.bær -= 1
            return True