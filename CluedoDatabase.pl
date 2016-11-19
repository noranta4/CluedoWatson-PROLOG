% WATSONcluedo

% assistente per CLUEDO 1a edizione
% autore: Antonio Norelli.


% usare "make." per aggiornare il database

:- discontiguous vista/2.
:- discontiguous richiesta_non_soddisfatta/4.
:- discontiguous richiesta_soddisfatta/4.
giocatore(gioc0).
giocatore(gioc1).
giocatore(gioc2).
giocatore(qualcuno).
personaggio(scarlett).
personaggio(plum).
personaggio(mustard).
personaggio(verde).
personaggio(bianchi).
personaggio(pavone).
arma(corda).
arma(piombo).
arma(pugnale).
arma(inglese).
arma(candeliere).
arma(rivoltella).
stanza(cucina).
stanza(ballo).
stanza(salotto).
stanza(pranzo).
stanza(biliardo).
stanza(biblioteca).
stanza(veranda).
stanza(studio).
stanza(anticamera).
innocente(X) :-
	personaggio(X),
	giocatore(Giocatore),
	vista(Giocatore, X).

armainnocente(X) :-
	arma(X),
	giocatore(Giocatore),
	vista(Giocatore, X).

stanzainnocente(X) :-
	stanza(X),
	giocatore(Giocatore),
	vista(Giocatore, X).

sospettato(X) :-
	personaggio(X),
	not(innocente(X)).

armasospetta(X) :-
	arma(X),
	not(armainnocente(X)).

stanzasospetta(X) :-
	stanza(X),
	not(stanzainnocente(X)).

vista(qualcuno,X) :-
	((richiesta_non_soddisfatta(gioc0,Carta,Altra1,Altra2),
	personaggio(X),
	personaggio(Carta),
	dif(X,Carta),
	arma(Altra1),
	stanza(Altra2));
	(richiesta_non_soddisfatta(gioc0,Altra1,Carta,Altra2),
	arma(X),
	arma(Carta),
	dif(X,Carta),
	personaggio(Altra1),
	stanza(Altra2));
	(richiesta_non_soddisfatta(gioc0,Altra1,Altra2,Carta),
	stanza(X),
	stanza(Carta),
	dif(X,Carta),
	personaggio(Altra1),
	arma(Altra2))),
	not(vista(gioc0,Carta)).

vista(X,Carta) :-
	giocatore(Y),
	giocatore(Z),
	dif(X,Y),
	dif(X,Z),
	(richiesta_soddisfatta(X,Carta,Altra1,Altra2) ;	richiesta_soddisfatta(X,Altra1,Carta,Altra2) ;	richiesta_soddisfatta(X,Altra1,Altra2,Carta)),
	vista(Y,Altra1),
	vista(Z,Altra2).
vista(gioc0,scarlett).
