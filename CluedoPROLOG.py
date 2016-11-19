__author__ = 'Antonio Norelli'


personaggi = ['Miss Scarlett', 'Professor Plum', 'Colonnello Mustard', 'Dottor Verde', 'Signora Bianchi', 'Signora Pavone']
armi = ['Corda', 'Tubo di piombo', 'Pugnale', 'Chiave inglese', 'Candeliere', 'Rivoltella']
stanze = ['Cucina', 'Sala da ballo', 'Salotto', 'Sala da pranzo', 'Sala del biliardo', 'Biblioteca', 'Veranda', 'Studio', 'Anticamera']
listecarte = [personaggi, armi, stanze]

# trasforma i nomi degli elementi in stringhe più semplici
def sim(string):
    return string.rsplit(None, 1)[-1].lower()

# inizializzazione giocaori
num_gioc = int(input('\nQuanti giocatori ci sono?\n'))
list_gioc = list(range(num_gioc))


# inizializzazione knowledge database ################################################################

f = open('CluedoDatabase.pl', 'w')

f.write('% WATSONcluedo\n\n% assistente per CLUEDO 1a edizione\n% autore: Antonio Norelli.\n\n\n% usare "make." per aggiornare il database\n\n')
f.write(':- discontiguous vista/2.\n:- discontiguous richiesta_non_soddisfatta/4.\n:- discontiguous richiesta_soddisfatta/4.\n')

#database #######################
for i in range(num_gioc):
    f.write('giocatore(gioc' + str(i) + ').\n')
f.write('giocatore(qualcuno).\n')

for i in personaggi:
    f.write('personaggio(' + sim(i) + ').\n')
for i in armi:
    f.write('arma(' + sim(i) + ').\n')
for i in stanze:
    f.write('stanza(' + sim(i) + ').\n')

#rules ###########################

#basic
f.write('innocente(X) :-\n\tpersonaggio(X),\n\tgiocatore(Giocatore),\n\tvista(Giocatore, X).\n')
f.write('\narmainnocente(X) :-\n\tarma(X),\n\tgiocatore(Giocatore),\n\tvista(Giocatore, X).\n')
f.write('\nstanzainnocente(X) :-\n\tstanza(X),\n\tgiocatore(Giocatore),\n\tvista(Giocatore, X).\n')
f.write('\nsospettato(X) :-\n\tpersonaggio(X),\n\tnot(innocente(X)).\n')
f.write('\narmasospetta(X) :-\n\tarma(X),\n\tnot(armainnocente(X)).\n')
f.write('\nstanzasospetta(X) :-\n\tstanza(X),\n\tnot(stanzainnocente(X)).\n')

#complex
f.write('\nvista(qualcuno,X) :-\n')
f.write('\t((richiesta_non_soddisfatta(gioc0,Carta,Altra1,Altra2),\n')
f.write('\tpersonaggio(X),\n')
f.write('\tpersonaggio(Carta),\n')
f.write('\tdif(X,Carta),\n')
f.write('\tarma(Altra1),\n')
f.write('\tstanza(Altra2));\n')
f.write('\t(richiesta_non_soddisfatta(gioc0,Altra1,Carta,Altra2),\n')
f.write('\tarma(X),\n')
f.write('\tarma(Carta),\n')
f.write('\tdif(X,Carta),\n')
f.write('\tpersonaggio(Altra1),\n')
f.write('\tstanza(Altra2));\n')
f.write('\t(richiesta_non_soddisfatta(gioc0,Altra1,Altra2,Carta),\n')
f.write('\tstanza(X),\n')
f.write('\tstanza(Carta),\n')
f.write('\tdif(X,Carta),\n')
f.write('\tpersonaggio(Altra1),\n')
f.write('\tarma(Altra2))),\n')
f.write('\tnot(vista(gioc0,Carta)).\n')


f.write('\nvista(X,Carta) :-\n')
f.write('\tgiocatore(Y),\n')
f.write('\tgiocatore(Z),\n')
f.write('\tdif(X,Y),\n')
f.write('\tdif(X,Z),\n')
f.write('\t(richiesta_soddisfatta(X,Carta,Altra1,Altra2) ;')
f.write('\trichiesta_soddisfatta(X,Altra1,Carta,Altra2) ;')
f.write('\trichiesta_soddisfatta(X,Altra1,Altra2,Carta)),\n')
f.write('\tvista(Y,Altra1),\n')
f.write('\tvista(Z,Altra2).\n')



f.close()

# aggiornamento database #################################################

def cartemie(listecarte):
    control = 0
    while(control==0):
        tipocarta = int(input("\nChe tipo di carta hai?\n0: personaggio\n1: arma\n2: stanza\n"))
        print("\nChe carta e'?\n")
        for i in listecarte[tipocarta]:
            print(listecarte[tipocarta].index(i), i)
        indicecarta = int(input())
        carta = listecarte[tipocarta][indicecarta]
        with open('CluedoDatabase.pl', 'a') as f:
            f.write('vista(gioc0,' + sim(carta) +').\n')
        control = int(input("\nHai un'altra carta da mostrarmi?\n0: si\n1: no\n"))

def cartechieste(listecarte, mia):
    chieste = ''
    for j in range(3):
        print("\nChe carta e' stata chiesta?\n")
        for i in listecarte[j]:
            print(listecarte[j].index(i), i)
        indicecarta = int(input())
        chieste += ',' + sim(listecarte[j][indicecarta])
    check = int(input("\nE' stata soddisfatta la richiesta?\n0: sì\n1: no\n"))
    if mia == 1 and check == 0:
        tipocarta = int(input("\nChe tipo di carta hai visto?\n0: personaggio\n1: arma\n2: stanza\n"))
        print("\nChe carta e'?\n")
        for i in listecarte[tipocarta]:
            print(listecarte[tipocarta].index(i), i)
        indicecarta = int(input())
        carta = listecarte[tipocarta][indicecarta]
        check = 0
    if check == 0:
        print('\nDa chi?\n')
        print("0: Tu\n1: Primo giocatore alla tua sinistra e così via")
        for i in range(num_gioc-2):
            print(str(i+2) + ":")
        checkgioc = input()
        with open('CluedoDatabase.pl', 'a') as f:
            if mia == 1: f.write('vista(gioc' + str(checkgioc) + ',' + sim(carta) +').\n')
            else: f.write('richiesta_soddisfatta(gioc' + str(checkgioc) + chieste +').\n')
    if mia == 1 and check == 1:
        with open('CluedoDatabase.pl', 'a') as f:
            f.write('richiesta_non_soddisfatta(gioc0' + chieste +').\n')

# programma #################################################

cartemie(listecarte)
print('\nChi comincia?\n')
print("0: Tu\n1: Primo giocatore alla tua sinistra e così via")
for i in range(num_gioc-2):
    print(str(i+2) + ":")
checkgioc = int(input())
while True:
    for i in range((num_gioc - checkgioc)%num_gioc):
        print('### turno di ', (i+checkgioc)%num_gioc, ' #############################')
        if int(input('Salta il turno?\n0: si\n1: no\n')): cartechieste(listecarte, 0)
    print('###turno di  0 #############################')
    if int(input('Salta il turno?\n0: si\n1: no\n')): cartechieste(listecarte, 1)
    for i in range(num_gioc - (num_gioc - checkgioc)%num_gioc -1):
        print('turno di ', (i+1)%num_gioc , ' #############################')
        if int(input('Salta il turno?\n0: si\n1: no\n')): cartechieste(listecarte, 0)












