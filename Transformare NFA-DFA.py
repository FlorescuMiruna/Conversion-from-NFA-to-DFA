f = open("NFA",'r')
stari = f.readline()
alfabet = f.readline()
stare_initiala = f.readline()
stare_initiala = stare_initiala[:-1]
nr_stari_finale = f.readline()
stari_finale = f.readline()
stari_finale = stari_finale.split()
nr_tranzitii = int(f.readline())

stari = stari.split()
alfabet = alfabet.split()


#Retinem tabelul de tranzitii al NFA-ului intr-un dictionar, unde cheia e un tuplu
#care contine un frozenset, ce contine o singura stare si o "litera" din alfabetul respectiva
#iar valoarea scheii va fi multimea (frozenset) de stari in care automatul poate ajunge cu starea
#respectiva

Tabel_NFA = {}

for x in range(nr_tranzitii):
    x = f.readline()
    x = x.split()
    tuplu = frozenset(x[0]), x[1]
    #print(tuplu)
    multime = x[2:]
    multime = frozenset(multime)
    Tabel_NFA[tuplu] = multime

print("Tabel NFA:" ,Tabel_NFA)
f.close()

Q = []   #Facem o lista in care vom retine starile DFA-ului, in care punem starea initiala
Tabel_DFA = {}
Q.append(frozenset(stare_initiala))

def adaugare(stare_1):
    stare_2 = frozenset()
    for y in alfabet:
        stare_2 = frozenset()
        for x in stare_1:
            tuplu = frozenset(x), y
            if tuplu in Tabel_NFA.keys():
                stare_2 = stare_2 | frozenset(Tabel_NFA[tuplu])    #Starea din tabelul DFA-ului va fi reuniunea starilor din DFA
        if stare_2 != frozenset({}):   #Daca starea nu este vida, o adaugam in tabelul de stari al DFA-ului
            Tabel_DFA[(stare_1, y)] = stare_2
            if stare_2 not in Q:       #Daca starea nu a fost deja adaugata in lista de stari a DFA-ului o adaugam, si apelam
                Q.append(stare_2)      #si pentru ea functia de adaugare in tabel, functia se opreste atunci cand nu mai este nicio stare
                adaugare(stare_2)      #care nu a fost adaugata


g = open("DFA",'w')

adaugare(frozenset(stare_initiala))
print("Tabel DFA:",Tabel_DFA)
for i in range(len(Q)):
    Q[i] = [y for y in Q[i]]
    Q[i].sort()

g.write("DFA-ul are " +str(len(Q)) +" stari:" +"\n")
sir =""
for x in Q:
    sir += "["
    for i in x:
        sir += i +", "
    sir = sir[:-2]
    sir += "], "

g.write(sir[:-2] +'\n')
sir = "Starile finale sunt:\n"    #Starile finale vor fi cele care erau stari finale in NFA
for x in Q:
    ok = False
    for y in x:
        if y in stari_finale:
            ok = True
    if ok == True:
        sir += "["
        for i in x:
            sir += i +", "
        sir = sir[:-2]
        sir += "], "
g.write(sir[:-2]+ '\n')
g.write("Tranzitiile sunt:\n")

for x in Q:
    for litera in alfabet:
        tuplu = frozenset(x),litera
        if tuplu in Tabel_DFA.keys():
            sir = "["
            for i in x:
                sir += i + ", "
            sir = sir[:-2]
            sir += "]    " + litera + "    ["
            for i in sorted(list(Tabel_DFA[tuplu])):
                sir += i + ", "
            sir = sir[:-2]
            sir += "]\n"
            g.write(sir)
g.close()