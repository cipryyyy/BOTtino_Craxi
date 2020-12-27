# BOTtino Craxi

## Cosa fa il bot?
BOTtino Craxi svolge quattro funzioni:
* #### Funzione main

  Controlla la pagina instagram "[__governo_del_cambianiente__](https://www.instagram.com/governo_del_cambianiente/)";
* #### Funzione news

  Legge le notizie dal canale telegram "[__NOTIZIÆ__](https://t.me/notiziae)";

* #### Funzione on_message

  Esegue comandi richiesti in chat.

## Come funziona?
Il bot per funzionare utilizza i programmi [main.py](https://github.com/cipryyyy/BOTtino_Craxi/blob/main/main.py) e [notiziae_reader.py](https://github.com/cipryyyy/BOTtino_Craxi/blob/main/notiziae_reader.py) per lavorare rispettivamente su discord e su telegram.

## Come si richiama un comando?
Per utilizzae un comando basta scrivere il nome del comando desiderato preceduto da __/__ o __.__
Es. ```.link``` oppure ```/link```

__I comandi preceduti da '!' non sono utilizzabili da tutti gli utenti dato che possono compromettere il corretto funzionamento del bot__

### Comandi disponibili
Lista dei comandi disponibili:
* ```link``` Mostra tutti i link utili della pagina.
* ❗ ```manual``` Esegue la funzione main solo una volta (_1_)

![BOTtino Craxi](http://subwork.altervista.org/photo_2020-11-28_15-55-53.jpg)

(1) _La pagina viene scansionata solo ogni 10-12 minuti (più eventuali pause) per evitare il ban temporaneo della rete, con questo comando viene eseguita una scansione aggiuntiva seguita da una pausa prolungata._
