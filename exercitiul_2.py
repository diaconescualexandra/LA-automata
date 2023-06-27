# Radu Ioana Alexandra - grupa 141
# Diaconescu Alexandra - grupa 144

import os


class Automat:
    def __init__(self):
        self.alfabet_input = []
        self.alfabet_ls = []
        self.ls_stari = []  # cate o lista pt alfabet input,stari si tranzitii
        self.ls_tranz = []  # alfabet lista, si o lista vida
        self.lista = []


def valids(aut):
    valid = 0
    for elem in aut.ls_stari:  # se verifica validitatea starilor date, intrucat
        if 'S' in elem:  # doar o singura stare poate fi urmata de litera S
            valid += 1
        if valid > 1:
            print("Verificati input.txt, S poate aparea doar langa o singura stare!")
            # se iese din program, intrucat a fost introdus un input.txt invalid
            os._exit(1)


def citire(nume_fisier):
    automat1 = Automat()
    with open(nume_fisier) as f:
        x = f.readlines()  # punem toate liniile din input.txt in x
        for i in range(0, len(x)):
            # sterge \n de la sfarsitul fiecarui string din lista x
            x[i] = x[i].strip("\n")
        i = 0
        """
            Se parcurge lista x. Se verifica daca un element din lista corespunde
            unui sir cheie "Input_alph","List_alph","Transitions:","States", iar apoi se adauga elementele
            care urmeaza in lista corespunzatoare, pana se ajunge la un sir "End", moment in care
            se iese din structura if. Doua dintre structurile if se folosesc de functia split si
            o valoare auxiliara sir pentru a crea liste de liste (pentru stari avem starea si
            daca este urmata de S sau F, iar pentru tranzitii separam fiecare element al tranzitiei).

        """
    while i < len(x):
        if (x[i] == "Input_alph:"):
            while (x[i] != "End"):
                i = i + 1
                if (x[i] != "End"):
                    automat1.alfabet_input.append(x[i])
        elif (x[i] == "List_alph:"):
            while (x[i] != "End"):
                i = i + 1
                if (x[i] != "End"):
                    automat1.alfabet_ls.append(x[i])
                    automat1.alfabet_ls.append(f"!{x[i]}")
        elif (x[i] == "States:"):
            while (x[i] != "End"):
                i = i + 1
                if (x[i] != "End"):
                    sir = x[i]
                    sir = sir.split(",")
                    automat1.ls_stari.append(sir)
        elif (x[i] == "Transitions:"):
            while (x[i] != "End"):
                i = i + 1
                if (x[i] != "End"):
                    sir = x[i]
                    sir = sir.split(",")
                    automat1.ls_tranz.append(sir)
        i = i+1
    valids(automat1)
    return automat1


def validare(aut):
    ls_stari1 = []
    for lista in aut.ls_stari:
        ls_stari1.append(lista[0])  # extragem starile din ls_stari
    '''
        Cum o tranzitie este de forma "stare,sigma,stare", verificam daca
        primul si ultimul element din tranzitie apartin listei starilor, iar
        al doilea element apartine listei sigma. Se afiseaza pe ecran
        un mesaj ce contine tranzitia si validitatea sa.
    '''
    for elem in aut.ls_tranz:
        if ((elem[0] in ls_stari1)
            and (elem[3] in ls_stari1)
            and (elem[1] in aut.alfabet_input)
            and ((elem[2] in aut.alfabet_ls) or elem[2] == 'epsilon')
            and ((elem[4] in aut.alfabet_ls) or elem[4] == 'epsilon')
            and ((elem[5] in aut.alfabet_ls) or elem[5] == 'epsilon')):  # am modificat conditia:
                # i merge de la indicele 2 pana la ultimul indice al tranzitiei
                print("Tranzitia {} este VALIDA!".format(elem))
        else:  # pentru a permite validarea nfa-urilor, care au tranz de forma
              print("Tranzitia {} este INVALIDA!".format(elem))  # s1,sigma,s2.1,s2.2 etc

def gestiune_lista(aut, tranz):
  if tranz[4] !='epsilon' and tranz[4] in aut.lista: #stergere element din lista
    aut.lista.remove(tranz[4])
  if tranz[5] !='epsilon' and tranz[5] not in aut.lista: #adaugare element in lista
    aut.lista.append(tranz[5])


def procesare_str(aut):
    sir = []
    x = input()
    while(x !="n"):  #se introduc simboluri din alph input, se da enter
      sir.append(x)  # cand s-a terminat de introdus, se scrie n
      x = input()
    ls_finale = []
    for stare in aut.ls_stari:
        if "S" in stare:  # se verifica starea intiala
            x = stare[0]
        if "F" in stare:  # se face o lista cu starile finale
            ls_finale.append(stare[0])
    for i in range(0, len(sir)):
        ok = 0
        for tranz in aut.ls_tranz:
            if ((tranz[0] ==x) 
            and (tranz[1]==sir[i])):  #ultima stare din traseu e I din tranz si litera din tranz e litera curenta
              if tranz[2] =='epsilon':
                x = tranz[3]        #x = a doua stare din tranz
                ok = 1
                gestiune_lista(aut, tranz)
              elif tranz[2][0] =="!": #se verifica absenta lui tranz[2] din lista
                if tranz[2][1:3] not in aut.lista:
                  x = tranz[3]
                  ok = 1
                  gestiune_lista(aut, tranz)
              elif tranz[2] in aut.lista:  # se verifica apartenenta lui tranz[2] in lista
                x = tranz[3]
                ok = 1
                gestiune_lista(aut, tranz)

    if i ==len(sir)-1 and ok==1: #daca a ajuns la finalul stringului
        if x in ls_finale:  # si ultima stare este una din cele finale
            print("sir acceptat!")
        else:
            print("sir respins!")
    else:
        print("sir respins!")

automat1 = citire("input_lfa.in")

print(automat1.alfabet_input)
print(automat1.alfabet_ls)
print(automat1.lista)
print(automat1.ls_stari)
print(automat1.ls_tranz)

validare(automat1)
procesare_str(automat1)
