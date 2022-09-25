Välipalautus 2: https://tsoha-moodle2.herokuapp.com/
Tajusin juuri, että Herokussa ei pääse näkemään taulujen sisältöä, eli ette pääse näkemään miten jutut lisääntyvät sinne.
Ei siis hirveästi testattavaa tai toiminnallisuuksia, rekisteröinti lisää käyttäjän users-tauluun, mutta en ole ehtinyt tehdä tunnuksen yms. tarkistusta

TODO:
admin _elif_ opiskelija _else_ epäkirjautunut session rakenne
tunnus ja salasana tarkistus
epäkirjautunut -> vain käyttäjille
keksi tapa saada kätevästi session usernamesta id

miten saada linkki kurssin sivulle
miten saada kurssin sivulle lista tehtävistä ja teksteistä
miten saada taskin id


Suunnitelma:
Kurssisivulla lista tehtävistä kaikille
Pistekirjanpito: opettajille opiskelija - pisteet - maxpisteet | opiskelijalle tehtävä - pisteet (viimeinen rivi yht.)
Poista kurssi: poista kaikki missä course_id sama

Etusivu:
lista kursseista, joilla on
linkki kaikkien kurssien sivuille
