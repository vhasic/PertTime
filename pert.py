from __future__ import annotations

import decimal
import math
from decimal import *

from scipy.stats import norm

# postavljanje preciznosti decimalnih brojeva na 2 decimale i minimalnog exponenta na -10
getcontext().prec = 2
getcontext().Emin = -10


class Cvor:
    """
    Klasa predstavlja događaje u mrežnom dijagramu koji označavaju početke i krajeve aktivnosti.
    """

    # statički brojač koji označava broj sljedećeg čvora kreiranog sa noviCvor
    brojac = 0

    # inicijalizacija čvora
    def __init__(self, brojCvora: int):
        """
        Kreira čvor sa zadanim brojem čvora. Baca izuzetak ako brojCvora nije cijeli broj.

        :param brojCvora: Jedinstvena oznaka čvora, koja treba biti cijeli broj.
        """
        if not isinstance(brojCvora, int):
            raise ValueError("Broj čvora treba biti cijeli broj")
        self._brojCvora = brojCvora
        self._ulazneAktivnosti = []
        self._izlazneAktivnosti = []
        self._najranijeVrijeme = 0
        self._najkasnijeVrijeme = 0
        self._rezerva = 0
        self._rang = 0
        self._posjecen = False

    # definisanje getera i setera
    @property
    def brojCvora(self) -> int:
        return self._brojCvora

    @brojCvora.setter
    def brojCvora(self, value: int):
        if not isinstance(value, int):
            raise ValueError("Broj čvora treba biti cijeli broj")
        self._brojCvora = value

    @property
    def ulazneAktivnosti(self) -> list[Aktivnost]:
        return self._ulazneAktivnosti

    @ulazneAktivnosti.setter
    def ulazneAktivnosti(self, value: list[Aktivnost]):
        self._ulazneAktivnosti = value

    @property
    def izlazneAktivnosti(self) -> list[Aktivnost]:
        return self._izlazneAktivnosti

    @izlazneAktivnosti.setter
    def izlazneAktivnosti(self, value: list[Aktivnost]):
        self._izlazneAktivnosti = value

    @property
    def najranijeVrijeme(self) -> decimal:
        return self._najranijeVrijeme

    @najranijeVrijeme.setter
    def najranijeVrijeme(self, value: decimal):
        self._najranijeVrijeme = value

    @property
    def najkasnijeVrijeme(self) -> decimal:
        return self._najkasnijeVrijeme

    @najkasnijeVrijeme.setter
    def najkasnijeVrijeme(self, value: decimal):
        self._najkasnijeVrijeme = value

    @property
    def rezerva(self) -> decimal:
        return self._rezerva

    @property
    def rang(self) -> int:
        return self._rang

    @rang.setter
    def rang(self, value: int):
        self._rang = value

    def izracunajRezervu(self):
        """
        Računa rezervu čvora
        """
        self._rezerva = Decimal(self.najkasnijeVrijeme) - Decimal(self.najranijeVrijeme)

    @staticmethod
    def noviCvor() -> Cvor:
        """
        Kreira novi prazni čvor sa sljedećim po redu brojem

        :return: Novokreirani čvor
        """
        Cvor.brojac = Cvor.brojac + 1
        return Cvor(Cvor.brojac)

    # ispisivanje čvora
    def __str__(self) -> str:
        string = ""
        string += "Broj čvora: " + str(self.brojCvora) + ", "
        string += "Najranije vrijeme: " + str(round(self.najranijeVrijeme, 2)) + ", "
        string += "Najkasnije vrijeme: " + str(round(self.najkasnijeVrijeme, 2)) + ""
        return string

    # poređenje čvorova
    # za ==
    def __eq__(self, other: Cvor) -> bool:
        return self.brojCvora == other.brojCvora

    # za !=
    def __ne__(self, other: Cvor) -> bool:
        return self.brojCvora != other.brojCvora


class Aktivnost:
    """
    Klasa predstavlja aktivnosti u mrežnom dijagramu (veze između čvorova).
    """

    # inicijalizacija aktivnosti
    def __init__(self, naziv: str, preduvjeti: list[str], optimisticnoVrijeme: decimal, modalnoVrijeme: decimal,
                 pesimisticnoVrijeme: decimal):
        """
        Kreiranje aktivnosti koja je jedinstveno definisana svojim imenom.

        :param naziv: naziv aktivnosti
        :param preduvjeti: aktivnosti koje prethode
        :param optimisticnoVrijeme: najduže trajanje
        :param modalnoVrijeme: srednje trajanje
        :param pesimisticnoVrijeme: najkraće trajanje
        """
        self._id = id(self)
        self._naziv = naziv
        self._trajanje = self.izracunajOcekivanoVrijeme(optimisticnoVrijeme, modalnoVrijeme, pesimisticnoVrijeme)
        self._preduvjeti = preduvjeti
        self._pocetniCvor = None
        self._krajnjiCvor = None
        self._varijansa = self.izracunajVarijansu(optimisticnoVrijeme, pesimisticnoVrijeme)
        self._rezervaAktivnosti = 0

    @property
    def varijansa(self) -> decimal:
        return self._varijansa

    @property
    def naziv(self) -> str:
        return self._naziv

    @naziv.setter
    def naziv(self, value: str):
        self._naziv = value

    @property
    def trajannje(self) -> decimal:
        return self._trajanje

    @trajannje.setter
    def trajannje(self, value: decimal):
        self._trajanje = value

    @property
    def preduvjeti(self):
        return self._preduvjeti

    @preduvjeti.setter
    def preduvjeti(self, value):
        self._preduvjeti = value

    @property
    def pocetniCvor(self) -> Cvor:
        return self._pocetniCvor

    @pocetniCvor.setter
    def pocetniCvor(self, value: Cvor):
        self._pocetniCvor = value

    @property
    def krajnjiCvor(self) -> Cvor:
        return self._krajnjiCvor

    @krajnjiCvor.setter
    def krajnjiCvor(self, value: Cvor):
        self._krajnjiCvor = value

    @property
    def rezervaAktivnosti(self):
        return self._rezervaAktivnosti

    def izracunajRezervu(self):
        """
        Računa rezervu aktivnosti kao:
        najkasnije vrijeme krajnjeg čvora - najranije vrijeme početnog čvora - trajanje aktivnosti
        i spašava rezultat u privatni atribut.
        """
        self._rezervaAktivnosti = Decimal(self.krajnjiCvor.najkasnijeVrijeme) - Decimal(
            self.pocetniCvor.najranijeVrijeme) - Decimal(self.trajannje)

    def izracunajOcekivanoVrijeme(self, a: decimal, m: decimal, b: decimal) -> decimal:
        """
        Računa očekivano vrijeme za datu aktivnost kao: očekivanoVrijeme=(a+4m+b)/6
        Baca ValueError ako nije a<=m<=b

        :param a: optimistično vrijeme
        :param m: modalno vrijeme
        :param b: pesimistično vrijeme
        """
        if not (a <= m <= b):
            raise ValueError("Mora vrijediti optimistično <= modlano <= pesimistično vrijeme!")
        return (a + 4 * m + b) / 6

    def izracunajVarijansu(self, a: decimal, b: decimal) -> decimal:
        """
        Računa varijansu za zadanu aktivnost kao: varijansa=((b-a)/6)^2

        :param a: optimistično vrijeme
        :param b: pesimistično vrijeme
        """
        if not (a <= b):
            raise ValueError("Mora vrijediti optimistično <= pesimistično vrijeme!")
        return ((b - a) / 6) ** 2

    # ispisivanje aktivnosti
    def __str__(self) -> str:
        string = ""
        string += "Naziv aktivnosti: " + str(self.naziv) + ", "
        string += "Trajanje aktivnosti: " + str(round(self.trajannje, 2)) + ""
        return string

    # poređenje aktivnosti
    # za ==
    def __eq__(self, other: Aktivnost) -> bool:
        return self.naziv == other.naziv

    # za !=
    def __ne__(self, other: Aktivnost) -> bool:
        return self.naziv != other.naziv


class Pert:
    """
    Klasa koja čuva mrežni dijagram
    """

    # inicijalizacija grafa
    def __init__(self):
        """
        Kreiranje praznog Pert mrežnog dijagrama.

        """
        self._cvorovi = []  # lista čvorova u dijagramu
        self._aktivnosti = []  # lista aktivnosti u dijagramu
        self._pocetniCvor = None  # početni čvor u dijagramu
        self._krajnjiCvor = None  # krajnji čvor u dijagramu
        self._kriticniPutevi = []  # lista kritičnih puteva u dijagramu
        self._trajanjeProjekta = 0  # očekivano trajanje projekta
        self._devijacijaNaKriticnomPutu = 0  # standarda devijacija aktivnosti na kritičnom putu
        self._sviPuteviSaTrajanjemIDevijacijom = []  # lista uređenih trojki (put, Te, sigma) svih puteva od početka do
        # kraja, sa njihovim očekivanim trajanjem i devijacijom

    # definisanje getera i setera
    @property
    def kriticniPutevi(self) -> list:
        return self._kriticniPutevi

    @property
    def devijacijaNaKriticnomPutu(self):
        return self._devijacijaNaKriticnomPutu

    @property
    def sviPuteviSaTrajanjemIDevijacijom(self) -> list:
        return self._sviPuteviSaTrajanjemIDevijacijom

    @property
    def trajanjeProjekta(self) -> decimal:
        return self._trajanjeProjekta

    @property
    def cvorovi(self):
        return self._cvorovi

    @property
    def aktivnosti(self):
        return self._aktivnosti

    @aktivnosti.setter
    def aktivnosti(self, value):
        self._aktivnosti = value

    @property
    def pocetniCvor(self) -> Cvor:
        return self._pocetniCvor

    @pocetniCvor.setter
    def pocetniCvor(self, value):
        self._pocetniCvor = value

    @property
    def krajnjiCvor(self):
        return self._krajnjiCvor

    @krajnjiCvor.setter
    def krajnjiCvor(self, value):
        self._krajnjiCvor = value

    def getBrojCvorova(self):
        return len(self.cvorovi)

    def getBrojAktivnosti(self):
        return len(self.aktivnosti)

    def getCvorSaBrojem(self, i: int) -> Cvor:
        lista = list(filter(lambda x: x.brojCvora == i, self.cvorovi))
        if len(lista) == 0:
            raise ValueError("Cvor sa brojem " + str(i) + " ne postoji!")
        return lista[0]

    # dodaje novu aktivnost u graf
    def dodajAktivnost(self, novaAktivnost: Aktivnost):
        if self.__contains__(novaAktivnost):
            raise ValueError("Aktivnost već postoji, nije je moguće dodati")
        else:
            self.aktivnosti.append(novaAktivnost)

    # dodaje novi čvor u graf
    def __dodajCvor(self, noviCvor: Cvor):
        self.cvorovi.append(noviCvor)

    def kreirajStrukturu(self):
        """
        Kreira strukturu mrežnog dijagrama za postojeće aktivnosti.
        Kreira početne i krajnje čvorove za svaku aktivnost i uspostavlja vezu između čvorova i aktivnosti.
        """
        # početni čvor u grafu
        cvor = Cvor.noviCvor()
        self.__dodajCvor(cvor)
        self.pocetniCvor = cvor
        kopija = self.aktivnosti[:]
        brojac = 0
        for aktivnost in kopija:
            brojac = brojac + 1
            # ako aktivnost nema preduvjeta
            if not aktivnost.preduvjeti:
                self.pocetniCvor.izlazneAktivnosti.append(aktivnost)
                aktivnost.pocetniCvor = self.pocetniCvor
                cvor = Cvor.noviCvor()
                self.__dodajCvor(cvor)
                cvor.ulazneAktivnosti.append(aktivnost)
                aktivnost.krajnjiCvor = cvor
            # ako ima samo jedan preduvjet onda mora biti vezana za krajnji čvor prethodne aktivnosti
            elif len(aktivnost.preduvjeti) == 1:
                # pronalazak preduvjetne aktivnosti u listi aktivnosti
                prethodnaAktivnost = self.dajAktivnostiIzListeNaziva(aktivnost.preduvjeti)[0]
                # prethodnaAktivnost = next((x for x in self.aktivnosti if x.naziv == aktivnost.preduvjeti[0]), None)
                aktivnost.pocetniCvor = prethodnaAktivnost.krajnjiCvor
                prethodnaAktivnost.krajnjiCvor.izlazneAktivnosti.append(aktivnost)
                cvor = Cvor.noviCvor()
                self.__dodajCvor(cvor)
                aktivnost.krajnjiCvor = cvor
                cvor.ulazneAktivnosti.append(aktivnost)
            else:
                # ako dvije aktivnosti imaju iste preduvjete
                # ako neka od do sada obrađenih aktivnosti ima iste preduvjete ne treba dodavati novi početni čvor
                aktivnostSaIstimPreduvjetima = None
                for j in range(0, brojac - 1):
                    if self.aktivnosti[j].preduvjeti == aktivnost.preduvjeti:
                        aktivnostSaIstimPreduvjetima = self.aktivnosti[j]
                        break
                if aktivnostSaIstimPreduvjetima is not None:
                    aktivnostSaIstimPreduvjetima.pocetniCvor.izlazneAktivnosti.append(aktivnost)
                    aktivnost.pocetniCvor = aktivnostSaIstimPreduvjetima.pocetniCvor
                else:
                    nizPreduvjeta = self.dajAktivnostiIzListeNaziva(aktivnost.preduvjeti)

                    # cvor je novododani kraj fiktivnih aktivnosti, a početak stvarne aktivnosti
                    cvor = Cvor.noviCvor()
                    self.__dodajCvor(cvor)
                    for preduvjetnaAktivnost in nizPreduvjeta:
                        fiktivnaAktivnost = Aktivnost("fiktivna", [], 0, 0, 0)
                        self.aktivnosti.append(fiktivnaAktivnost)
                        preduvjetnaAktivnost.krajnjiCvor.izlazneAktivnosti.append(fiktivnaAktivnost)
                        fiktivnaAktivnost.pocetniCvor = preduvjetnaAktivnost.krajnjiCvor
                        fiktivnaAktivnost.krajnjiCvor = cvor
                        cvor.ulazneAktivnosti.append(fiktivnaAktivnost)

                    cvor.izlazneAktivnosti.append(aktivnost)
                    aktivnost.pocetniCvor = cvor
                krCvor = Cvor.noviCvor()
                self.__dodajCvor(krCvor)
                aktivnost.krajnjiCvor = krCvor
                krCvor.ulazneAktivnosti.append(aktivnost)

    def dajAktivnostiIzListeNaziva(self, nazivi: list[str]):
        """
        Vraća listu objekta aktivnosti sa zadanim nazivom. Ako neka aktivnost ne postoji baca izuzetak

        :param nazivi: Lista naziva aktivnosti
        :return: Lista objekta aktivnosti sa zadanim nazivom
        """
        nizPreduvjeta = []
        for i in range(0, len(nazivi)):
            lista = list(filter(lambda x: x.naziv == nazivi[i], self.aktivnosti))
            if len(lista) != 1:
                raise ValueError("Aktivnost sa nazivom: " + nazivi[i] + " ne postoji.")
            aktivnost = lista[0]
            nizPreduvjeta.append(aktivnost)
        return nizPreduvjeta

    def izbaciNepotrebneCvorove(self):
        """
        Skraćuje mrežni dijagram izbacivanjem nepotrebnih čvorova.
        """
        cvoroviZaBrisanje = []
        krajnjiCvorovi = []
        aktivnostiZaBrisanje = []
        for cvor in self.cvorovi:
            if not cvor.izlazneAktivnosti:
                krajnjiCvorovi.append(cvor)
            # izbacivanje viška čvorova za koje vrijedi da u njih ulaze samo fiktivne aktivnosti,
            # u tom slučaju treba obrisati i viška fiktivne aktivnosti
            # ovo vrijedi samo kada su u pitanju samo 2 fiktivne aktivnosti
            if len(cvor.ulazneAktivnosti) == 2:
                a1 = cvor.ulazneAktivnosti[0]
                a2 = cvor.ulazneAktivnosti[1]
                if a1.naziv == "fiktivna" and a2.naziv == "fiktivna":
                    # pošto se a1 briše, ako iz njenog početnog čvora izlazi stvarna aktivnost onda se treba a2 brisati
                    # tj. zamijeniti uloga a1 i a2, kako bi se izbjegli nepotrebni čvorovi
                    for akt in a1.pocetniCvor.izlazneAktivnosti:
                        if akt.naziv != "fiktivna":
                            pomocna = a1
                            a1 = a2
                            a2 = pomocna
                            break
                    # preusmjeravanje
                    a1.pocetniCvor.izlazneAktivnosti.remove(a1)
                    a1.pocetniCvor.izlazneAktivnosti.extend(a1.krajnjiCvor.izlazneAktivnosti)
                    for akt in a1.krajnjiCvor.izlazneAktivnosti:
                        akt.pocetniCvor = a1.pocetniCvor
                    a2.krajnjiCvor = a1.pocetniCvor
                    a1.pocetniCvor.ulazneAktivnosti.append(a2)
                    cvoroviZaBrisanje.append(a1.krajnjiCvor)
                    aktivnostiZaBrisanje.append(a1)

        # svođenje više krajnjih čvorova na samo jedan
        cvoroviZaBrisanje.extend(self.svediNaJedanKraj(krajnjiCvorovi))

        # obrisati viška aktivnosti
        for aktivnost in aktivnostiZaBrisanje:
            self.__obrisiAktivnost(aktivnost)

        # obrisati viška čvorove
        for cvor in cvoroviZaBrisanje:
            self.cvorovi.remove(cvor)

    def __obrisiAktivnost(self, aktivnost):
        self.aktivnosti = list(filter(lambda x: x._id != aktivnost._id, self.aktivnosti))

    def svediNaJedanKraj(self, krajnjiCvorovi: list):
        """
        Funkcija svodi više krajnjih čvorova na samo jedan.

        :param krajnjiCvorovi: Cvorovi u grafu iz kojih ne izlazi niti jedna aktivnost
        :return: Cvorove koje treba izbaciti, ukoliko je graf skraćen. Inače vraća [].
        """
        # ako ima samo jedan kraj onda se ne treba ništa skraćivati
        if len(krajnjiCvorovi) == 1:
            self.krajnjiCvor = krajnjiCvorovi[0]
            return []

        zadnjiCvor = Cvor.noviCvor()
        cvoroviZaBrisanje = []
        predzadnjiCvorovi = []
        dodatiKraj = False
        for cvor in krajnjiCvorovi:
            for aktivnost in cvor.ulazneAktivnosti:
                # ako ima više aktivnosti koje izlaze iz jednog čvora, a barem dvije te aktivnosti završavaju u nekom od krajnjih čvorova
                # tada se mora dodati novi čvor, jer se aktivnosti ne smiju preklopiti
                if predzadnjiCvorovi.__contains__(aktivnost.pocetniCvor):
                    dodatiKraj = True
                    break
                predzadnjiCvorovi.append(aktivnost.pocetniCvor)

        for cvor in krajnjiCvorovi:
            if dodatiKraj:
                fiktivnaAktivnost = Aktivnost("fiktivna", [], 0, 0, 0)
                self.aktivnosti.append(fiktivnaAktivnost)
                cvor.izlazneAktivnosti.append(fiktivnaAktivnost)
                fiktivnaAktivnost.pocetniCvor = cvor
                fiktivnaAktivnost.krajnjiCvor = zadnjiCvor
                zadnjiCvor.ulazneAktivnosti.append(fiktivnaAktivnost)
            # u drugom slučaju samo preusmjeriti sve aktivnosti u jedan čvor novi čvor, a sve dosadašnje krajeve obrisati
            else:
                # sve aktivnosti preusmjeriti u jedan kraj
                zadnjiCvor.ulazneAktivnosti.extend(cvor.ulazneAktivnosti)
                for aktivnost in cvor.ulazneAktivnosti:
                    aktivnost.krajnjiCvor = zadnjiCvor
                cvoroviZaBrisanje.append(cvor)
        self.__dodajCvor(zadnjiCvor)
        self.krajnjiCvor = zadnjiCvor
        return cvoroviZaBrisanje

    def renumerisiCvorove(self):
        """
        Vrši renumeraciju čvorova.
        Nakon izvršavanja funkcije čvorovi u grafu su pravilno (topološki) sortirani
        """
        imaPromjena = True
        i = 0
        while imaPromjena:
            # određivanje ranga čvorova u trenutnoj iteraciji
            imaPromjena = False
            for cvor in self.cvorovi:
                rangPrethodnika = []
                for aktivnost in cvor.ulazneAktivnosti:
                    rangPrethodnika.append(aktivnost.pocetniCvor.rang)
                prethodniRang = cvor.rang
                cvor.rang = max(cvor.rang, (max(rangPrethodnika) if rangPrethodnika else 0) + 1)
                # ako je bila barem jedna promjena ranga potrebno je izvršiti još iteracija u while petlji
                if prethodniRang != cvor.rang: imaPromjena = True
            # Algoritam mora terminirati u n iteracija inače pravilna numeracija ne postoji,
            # odnosno graf ima petlje
            i = i + 1
            if i > self.getBrojCvorova():
                raise RuntimeError("Graf ne smije imati petlje!")

        # sortiranje čvorova po rangu u rastućem poretku
        # key je težina nekog člana, a po defautu sortira u rastućem poretku
        self.cvorovi.sort(key=lambda x: x.rang)

        # renumeracija čvorova na osnovu ranga: najmanji rang najmanji broj čvora, brojanje počinje od 1
        for i in range(self.getBrojCvorova()):
            self.cvorovi[i].brojCvora = i + 1

    def izracunajNajranijaVremena(self):
        """
        Računa najranija vremena za sve događaje (čvorove).
        """
        # najranije vrijeme početnog čvora je 0
        self.pocetniCvor.najranijeVrijeme = 0
        for cvor in self.cvorovi:
            nizVremena = []
            # određivanje najranijeg završetka svake od aktivnosti koja ulazi u čvor
            for aktivnost in cvor.ulazneAktivnosti:
                nizVremena.append(aktivnost.pocetniCvor.najranijeVrijeme + aktivnost.trajannje)

            cvor.najranijeVrijeme = max(nizVremena) if nizVremena else 0

    def izracunajNajkasnijaVremena(self):
        """
        Računa najkasnija vremena za sve događaje (čvorove).
        """
        # najkasnije vrijeme krajnjeg čvora je jednako njegovom najranijem vremenu
        self.krajnjiCvor.najkasnijeVrijeme = self.krajnjiCvor.najranijeVrijeme

        # ide se od kraja ka početku
        reverznaListaCvorova = self.cvorovi[::-1]
        for cvor in reverznaListaCvorova:
            nizVremena = []
            # određivanje najkasnijeg početka svake od aktivnosti koja ulazi u čvor
            for aktivnost in cvor.izlazneAktivnosti:
                nizVremena.append(aktivnost.krajnjiCvor.najkasnijeVrijeme - aktivnost.trajannje)

            cvor.najkasnijeVrijeme = min(nizVremena) if nizVremena else cvor.najkasnijeVrijeme

    def odrediKriticnePuteve(self, trenutniCvor: Cvor, put: list):
        """
        Funkcija rekurzivno određuje sve kritične puteve u grafu, i spašava ih u atribut kriticniPutevi

        :param trenutniCvor: Trenutni čvor u nizu rekurzija
        :param put: Do sada nađeni put
        """
        # označi trenutni čvor posjećenim
        trenutniCvor._posjecen = True
        put.append(trenutniCvor)

        # ako se došlo do krajnjeg čvora to je jedan put
        if trenutniCvor == self.krajnjiCvor:
            self.kriticniPutevi.append(put[:])
        else:
            # idi kroz njegove sljedbenike, tj aktivnost.krajnjiCvor (to su sljedbenici)
            for aktivnost in trenutniCvor.izlazneAktivnosti:
                # ako sljedeći čvor nije posjećen i ako mu je rezerva nula (uslov za kritični put)
                if aktivnost.krajnjiCvor._posjecen == False and aktivnost.krajnjiCvor.rezerva == 0:
                    self.odrediKriticnePuteve(aktivnost.krajnjiCvor, put)

        # izbaci zadnji čvor iz liste i označi ga neposjećenim (može se naći u još nekim putevima)
        put.pop()
        trenutniCvor._posjecen = False

    def odrediSvePuteve(self, trenutniCvor: Cvor, put: list):
        """
        Funkcija rekurzivno određuje sve puteve u grafu,
        vremensko trajanje svagod od tih puteva i devijaciju na svakom putu,
        i spašava ih u atribut kao niz tuple objekata (put,trajanje,devijacija).

        :param trenutniCvor: Trenutni čvor u nizu rekurzija
        :param put: Do sada nađeni put
        """
        # označi trenutni čvor posjećenim
        trenutniCvor._posjecen = True
        put.append(trenutniCvor)

        # ako se došlo do krajnjeg čvora to je jedan put
        if trenutniCvor == self.krajnjiCvor:
            # dodaje se uređena trojka
            devijacija = self.izracunajDevijacijuNaPutu(put)
            trajanje = self.izracunajTrajanjeNaPutu(put)
            self.sviPuteviSaTrajanjemIDevijacijom.append((put[:], trajanje, devijacija))
        else:
            # idi kroz njegove sljedbenike, tj aktivnost.krajnjiCvor (to su sljedbenici)
            for aktivnost in trenutniCvor.izlazneAktivnosti:
                # ako sljedeći čvor nije posjećen
                if aktivnost.krajnjiCvor._posjecen == False:
                    self.odrediSvePuteve(aktivnost.krajnjiCvor, put)

        # izbaci zadnji čvor iz liste i označi ga neposjećenim (može se naći u još nekim putevima)
        put.pop()
        trenutniCvor._posjecen = False

    def izracunajDevijacijuNaKriticnomPutu(self):
        """
        Računa devijaciju na kritičnom putu sa najmanjim brojem aktivnosti.
        """
        varijansa = 0
        kriticniPut = min(self.kriticniPutevi, key=lambda i: len(i))

        for i in range(1, len(kriticniPut)):
            # kritična aktivnost povezuje dva kritična događaja
            prviCvor = kriticniPut[i - 1]
            drugiCvor = kriticniPut[i]
            kriticnaAktivnost = next((x for x in prviCvor.izlazneAktivnosti if x.krajnjiCvor == drugiCvor), None)
            varijansa += kriticnaAktivnost.varijansa

        self._devijacijaNaKriticnomPutu = math.sqrt(varijansa)

    # Da bi procjena trajanja bila što pouzdanija treba naći najveću devijaciju prolazeći kor sve puteve,
    # bilo kritične ili subkritične
    def izracunajDevijacijuNaPutu(self, put: list) -> decimal:
        """
        Računa devijaciju na zadanom putu.

        :param put: Put na kojem se računa devijacija
        """
        varijansa = 0
        for i in range(1, len(put)):
            prviCvor = put[i - 1]
            drugiCvor = put[i]
            # pronalazak aktivnosti koja povezuje prvi i drugi čvor
            aktivnost = next((x for x in prviCvor.izlazneAktivnosti if x.krajnjiCvor == drugiCvor), None)
            if aktivnost is not None:
                varijansa += aktivnost.varijansa

        return math.sqrt(varijansa)

    def azurirajGraf(self):
        """
        Vrši ažuriranje grafa.
        Ovu metodu je potrebno pozvati nakon dodavanja aktivnosti.
        """
        self.kreirajStrukturu()
        self.izbaciNepotrebneCvorove()
        self.renumerisiCvorove()
        self.izracunajNajranijaVremena()
        self.izracunajNajkasnijaVremena()
        self.izracunajTrajanjeProjekta()
        self.izracunajRezerveCvorova()
        self.izracunajRezerveAktivnosti()
        self.odrediKriticnePuteve(self.pocetniCvor, [])
        self.izracunajDevijacijuNaKriticnomPutu()
        self.odrediSvePuteve(self.pocetniCvor, [])

    def izracunajRezerveCvorova(self):
        """
        Prolazi kroz sve čvorove i računa njihove rezerve.
        """
        for cvor in self.cvorovi:
            cvor.izracunajRezervu()

    def izracunajRezerveAktivnosti(self):
        """
        Prolazi kroz sve aktivnosti i računa njihove rezerve.
        """
        for aktivnost in self.aktivnosti:
            aktivnost.izracunajRezervu()

    def izracunajTrajanjeProjekta(self) -> decimal:
        """
        Računa trajanje projekta kao razliku između najkasnijeg vremena krajnjeg čvora i najranijeg vremena početnog čvora.

        :return: Trajanje projekta
        """
        self._trajanjeProjekta = self.krajnjiCvor.najkasnijeVrijeme - self.pocetniCvor.najranijeVrijeme
        return self.trajanjeProjekta

    def izracunajTrajanjeNaPutu(self, put: list) -> decimal:
        """
        Računa trajanje jednog puta u grafu kao zbir trajanja svih aktivnosti na putu.

        :param put: Put za koji se računa trajanje
        :return: Trajanje aktivnosti na putu
        """
        trajanje = 0
        for i in range(0, len(put)):
            prviCvor = put[i - 1]
            drugiCvor = put[i]
            # pronalazak aktivnosti koja povezuje prvi i drugi čvor
            aktivnost = next((x for x in prviCvor.izlazneAktivnosti if x.krajnjiCvor == drugiCvor), None)
            if aktivnost is not None:
                trajanje += aktivnost.trajannje
        return trajanje

    def izracunajProcjenuTrajanjaProjekta(self, p: decimal) -> decimal:
        """
        Računa trajanje projekta za zadanu vjerovatnoću Ts=Te+sigma*Fi^-1(P) na kritičnom putu.

        :param p: Vjerovatnoća sa kojom se procjenjuje trajanje projekta
        :return: Procijenjeno trajanje projekta za zadanu vjerovatnoću
        """
        return self.trajanjeProjekta + self._devijacijaNaKriticnomPutu * norm.ppf(p)

    def izracunajNajduzuProcjenuTrajanjaProjekta(self, p: decimal) -> decimal:
        """
        Računa najduže trajanje projekta na svim putevima, za zadanu vjerovatnoću Ts=Te+sigma*Fi^-1(P)

        :param p: Vjerovatnoća sa kojom se procjenjuje trajanje projekta
        :return: Najduže procijenjeno trajanje projekta za zadanu vjerovatnoću
        """
        fi = norm.ppf(p)
        niz = []
        for tuple in self.sviPuteviSaTrajanjemIDevijacijom:
            niz.append(tuple[1] + tuple[2] * fi)
        return max(niz)

    def izracunajVjerovatnocuZavrsetkaProjekta(self, period: decimal) -> decimal:
        """
        Funckija računa vjerovatnoću završetka projekta za određeni period.

        :param period: Period za koji se traži vjerovatnoća završetka projekta.
        :return: Vjerovatnoća završetka za dati period.
        """
        return norm.cdf((period - self.trajanjeProjekta) / self._devijacijaNaKriticnomPutu)

    # ispisivanje Pert grafa
    def __str__(self) -> str:
        string = ""
        string += "Čvorovi projekta: \n" + str(self.dajStringKolekcije(self.cvorovi)) + "\n"
        string += "Aktivnosti projekta: \n" + str(self.dajStringKolekcije(self.aktivnosti)) + "\n"
        string += "Trajanje projekta: " + str(round(self.trajanjeProjekta, 2)) + "\n"
        string += "Kritični putevi: \n" + self.dajStirngKriticnihPuteva()
        return string

    def dajStringSvihPuteva(self) -> str:
        """
        Predstavlja puteve u grafu pomoću stringa.

        :return: String svih puteva
        """
        rezultat = ""
        for tuple in self.sviPuteviSaTrajanjemIDevijacijom:
            string = ""
            for cvor in tuple[0]:
                string += str(cvor.brojCvora) + " - "
            string = string[:-3]
            rezultat += string + " Trajanje: " + str(round(tuple[1], 2)) + " Devijacija: " + str(
                round(tuple[2], 2)) + "\n"
        return rezultat

    def dajStringKolekcije(self, kolekcija: list) -> str:
        """
        Pretvara proslijeđenu listu u string koji se može ispisati.

        :param kolekcija: Lista čvorova ili lista aktivnosti u grafu.
        :return: String sa svim elementima iz kolekcije.
        """
        string = ""
        for clan in kolekcija:
            string += str(clan) + "\n"
        return string

    def dajStirngKriticnihPuteva(self) -> str:
        """
        Pretvara kritične puteve u stirng koji se može prikazati.

        :return: Stirng naziva aktivnosti na kritičnim putevima
        """
        string = ""
        # prolazi kroz sve kritične puteve
        for kriticniPut in self.kriticniPutevi:
            s = ""
            for i in range(1, len(kriticniPut)):
                # nalazi aktivnosti koje povezuju kritične događaje
                for aktivnost in kriticniPut[i].ulazneAktivnosti:
                    if aktivnost.pocetniCvor == kriticniPut[i - 1] and aktivnost.krajnjiCvor == kriticniPut[i]:
                        s += aktivnost.naziv + " - "
                        break

            # izbacivanje zadnja tri znaka : " - "
            s = s[:-3]
            # dodaje string jednog kritičnog puta
            string += s + "\n"
        return string

    def __contains__(self, item) -> bool:
        """
        Provjerava da li se item nalazi u grafu.

        :param item: Klasa Cvor ili klasa Aktivnost
        :return: Vraća True ako je čvor ili aktivnost u grafu
        """
        return (isinstance(item, Cvor) and (item in self.cvorovi)) or (
                isinstance(item, Aktivnost) and (item in self.aktivnosti))


if __name__ == "__main__":  # pragma: no cover
    print("ok")