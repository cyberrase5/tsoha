https://tsoha-moodle2.herokuapp.com/

Moodle 2.0 on Moodle-kopio, eli opetussovellus

Käyttäjät ovat joko opiskelijoita tai opettajia. Opettajuus pitää todistaa tunnusta luodessa. Opettajat saavat luoda kursseja ja luoda sisältöä kursseilleen. Kurssit jakautuvat kuuteen viikkoon. Sisällöt ovat viikkokohtaisia, ja niitä on kolmea tyyppiä: tekstit, jossa opettaja selittää jonkin asian, kysymys ja vastaus tehtävä (lyhennetty koodissa QA/qa), jossa vastaus syötetään tekstinä (kirjainkoolla ei väliä) sekä monivalintatehtävä (koodissa lyhennetty MC/mc). Opiskelijat voivat nähdä omat kurssikohtaiset pisteensä tehtäväkohtaisesti, ja opettajat lisäksi kaikkien osallistujien (suppeammin, ainoastaan kokonaistilanne). Opiskelijat voivat liittyä ja lähteä kursseilta.

ps. yläpalkin Moodle-teksti toimii linkkinä etusivulle

Toimminot:
- luo käyttäjä, kirjaudu sisään
- luo kurssi (opettajille)
- lisää tehtäviä ja tekstejä (vain kurssin opettajalle)
- ratkaise tehtäviä
- tarkista pistetilanne (opiskelija -> omat, opettaja -> kaikkien)
- liity ja poistu kurssilta

Johdatus tietojenkäsittelytieteeseen viikko 1 sisältää pari valmista tehtävää ja tekstiä

Sana, jolla opettajuus todistetaan: harri


Tietokanta

- users, courses ja texts lienee ilmiselviä
- participants
    - tänne lisätään entry, kun kurssille liitytään ja poistuessa se poistetaan
- tasks
    - tänne tallenetaan tiedot QA/MC-tehtävistä, course_id ja week kertoo oikean paikan. Sarake type 0 = QA, 1 = MC
- submissions
    - sisältää tehtäväkohtaisesti tiedot käyttäjien vastaustilanteesta. Kun kurssille liitytään, luodaan entryt kaikkiin olemassaoleviin tehtäviin tähän tauluun vakioarvoilla (0 pistettä ja käytettyä yritystä) sekä kun opettaja luo uuden kurssin, kaikille kurssin osallistujille lisätään entryt uuteen tehtävään tähän tauluun vakioarvoilla
- choices
    - sisältää monivalintatehtävien vaihtoehdot. Oikea tehtävä tunnistetaan task_id sarakkeesta. Näitä on aina 4kpl/tehtävä

Ominaisuuksien testaamista:

- luo kurssi
    - vain opettaja voi (testattu osoiterivin kautta kirjaantumattomana ja opiskelijana)
- tehtävien lisääminen
    - vain kurssin opettaja voi (testattu osoiteriviltä muuna opettajana, opiskelijana ja epäkirjautuneena)
- kurssin poistaminen
    - vain kurssin opettaja voi (testattu osoiteriviltä muuna opettajana, opiskelijana ja epäkirjautuneena)
- luo tehtävä
    - vain kurssin opettaja voi (testattu osoiteriviltä muuna opettajana, opiskelijana ja epäkirjautuneena)
- vastaa QA-tehtävään
    - vastausnappi katoaa, kun yritykset on käytetty, mutta enterillä voi yhä vastata. routes qa_handler sisältää tarkistuksen, että yrityksiä on liikaa. Myöskin oikean vastauksen jälkeen tehtävään voi yhä vastata, mutta väärästä vastauksesta ei menetä pisteitä
- tieto tuntuu poistuvan tauluista kuten suunniteltu, tauluista ei löydy poistettujen kurssien tietoja
- en tainnut testata ihan kaikkea



Mietteitä erinäisistä aiheista

Tietoturva ja syötteet
- opettajan toiminnoissa on vähemmän tarkastuksia, eikä syötteiden pituuksia tarkasteta. Esimerkiksi opettaja voi lähteä omalta kurssiltaan, mutta vain osoiterivin kautta. En toteuta näitä tarkistuksia, koska opettajien voi olettaa käyttäytyvän asiallisesti
- tasks.html hidden task_id kenttää voi muuttaa mikäli ymmärsin materiaalin oikein, jolloin routes qa_handler hakee väärän tehtävän oikean vastauksen. Tämän ei pitäisi olla ongelma, sillä pisteet päivittyisivät samaan tehtävään

Pylint
- 8.80, tulee valituksia mm. "Redefining name x from outer scope", en jaksa muuttaa ensiksi olleita.
- pisin rivi 113 merkkiä, mielestäni looginen kokonaisuus yhdellä rivillä on tärkeämpää kuin 13 merkkiä liian pitkä rivi

HTML-koodia voisi siistiä reilusti, mutta en halua enää rikkoa mitään