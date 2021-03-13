from __future__ import annotations

import decimal

from scipy.stats import norm
import math
from decimal import *

# postavljanje preciznosti decimalnih brojeva na 2 decimale i minimalnog exponenta na -10
# todo možda postaviti prec na 5 npr, a Emin na 0
getcontext().prec = 2
getcontext().Emin = -10


# todo pošto listama može biti proslijeđeno bilo šta, i mmože imati duplikata, potrebno je provjeriti prije kreiranja čvorova i aktivnosti


class Cvor:
    """
    Klasa predstavlja događaje u mrežnom dijagramu koji označavaju početke i krajeve aktivnosti.
    """

    # statički brojač koji označava broj sljedećeg čvora kreiranog sa noviCvor
    brojac = 0

    # inicijalizacija čvora
    def __init__(self, brojCvora: int):
        """

        :param brojCvora: Jedinstvena oznaka čvora
        """
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

    # todo ovo sam samo na jednom mjestu koristio, a na svima je korišteno append, vidjeti šta je bolje
    # def dodajIzlaznuAktivnost(self, aktivnost):
    #     self.izlazneAktivnosti.append(aktivnost)

    # ispisivanje čvora
    def __str__(self) -> str:
        string = ""
        string += "{Broj čvora: " + str(self.brojCvora) + ", "
        # string+="Ulazne aktivnosti: "+self.ulazneAktivnosti+"\n"
        # string+="Izlazne aktivnosti: "+self.izlazneAktivnosti+"\n"
        string += "Najranije vrijeme: " + str(self.najranijeVrijeme) + ", "
        string += "Najkasnije vrijeme: " + str(self.najkasnijeVrijeme) + "}"
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
    # todo razmisliti o dodavnaju najranijeg i najkasnijeg početka
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

    # todo da li vraćati preduvjete kao listu aktivnosti ili onako kako je zadano kao niz stringova naziva prethodnih aktivnosti
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
        self._rezervaAktivnosti=Decimal(self.krajnjiCvor.najkasnijeVrijeme)-Decimal(self.pocetniCvor.najranijeVrijeme)-Decimal(self.trajannje)

    def izracunajOcekivanoVrijeme(self, a: decimal, m: decimal, b: decimal) -> decimal:
        """
        Računa očekivano vrijeme za datu aktivnost kao: očekivanoVrijeme=(a+4m+b)/6

        :param a: optimistično vrijeme
        :param m: modalno vrijeme
        :param b: pesimistično vrijeme
        """
        return (a + 4 * m + b) / 6

    def izracunajVarijansu(self, a: decimal, b: decimal) -> decimal:
        """
        Računa varijansu za zadanu aktivnost kao: varijansa=((b-a)/6)^2

        :param a: optimistično vrijeme
        :param b: pesimistično vrijeme
        """
        return ((b - a) / 6) ** 2

    # ispisivanje aktivnosti
    def __str__(self) -> str:
        string = ""
        string += "{Naziv aktivnosti: " + str(self.naziv) + ", "
        string += "Trajanje aktivnosti: " + str(self.trajannje) + "}"
        # string += "Preduvjeti: " + str(self.preduvjeti) + "\n"
        # string += "Početni čvor: " + str(self.pocetniCvor) + "\n"
        # string += "Krajnji čvor: " + str(self.krajnjiCvor) + "\n"
        return string

    # poređenje aktivnosti
    # za ==
    def __eq__(self, other: Aktivnost) -> bool:
        return self.naziv == other.naziv

    # za !=
    def __ne__(self, other: Aktivnost) -> bool:
        return self.naziv != other.naziv


# todo dodati računanje Z i računanje vjerovatnoće za određeno trajanje
class Pert:
    """
    Klasa koja čuva mrežni dijagram
    """

    # inicijalizacija grafa
    # todo provjeriti ovaj parametar graf!!
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
        self._procijenjenoVrijemeTrajanja = 0  # trajanje projekta koje se računa na zahtjev sa određenom vjerovatnoćom
        self._devijacijaNaKriticnomPutu = 0  # standarda devijacija aktivnosti na kritičnom putu

    # definisanje getera i setera
    @property
    def kriticniPutevi(self) -> list:
        return self._kriticniPutevi

    @property
    def trajanjeProjekta(self) -> decimal:
        return self._trajanjeProjekta

    @property
    def procijenjenoTrajanjeProjekta(self) -> decimal:
        return self._procijenjenoVrijemeTrajanja

    @property
    def cvorovi(self):
        return self._cvorovi

    @cvorovi.setter
    def cvorovi(self, value):
        self._cvorovi = value

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

    # dodaje novu aktivnost u graf
    def dodajAktivnost(self, novaAktivnost: Aktivnost):
        if self.__contains__(novaAktivnost):
            raise UserWarning("Aktivnost već postoji, nije je moguće dodati")
        else:
            self.aktivnosti.append(novaAktivnost)

    # dodaje novi čvor u graf
    def dodajCvor(self, noviCvor: Cvor):
        self.cvorovi.append(noviCvor)

    def kreirajStrukturu(self):
        """
        Kreira strukturu mrežnog dijagrama za postojeće aktivnosti.
        Kreira početne i krajnje čvorove za svaku aktivnost i uspostavlja vezu između čvorova i aktivnosti.
        """
        # početni čvor u grafu
        cvor = Cvor.noviCvor()
        self.dodajCvor(cvor)
        self.pocetniCvor = cvor
        kopija= self.aktivnosti[:]
        for aktivnost in kopija:
            # ako aktivnost nema preduvjeta
            if not aktivnost.preduvjeti:
                # self.pocetniCvor.dodajIzlaznuAktivnost(aktivnost)
                self.pocetniCvor.izlazneAktivnosti.append(aktivnost)
                aktivnost.pocetniCvor = self.pocetniCvor
                cvor = Cvor.noviCvor()
                self.dodajCvor(cvor)
                cvor.ulazneAktivnosti.append(aktivnost)
                aktivnost.krajnjiCvor = cvor
            # ako ima samo jedan preduvjet onda mora biti vezana za krajnji čvor prethodne aktivnosti
            elif len(aktivnost.preduvjeti) == 1:
                # pronalazak preduvjetne aktivnosti u listi aktivnosti
                prethodnaAktivnost = next((x for x in self.aktivnosti if x.naziv == aktivnost.preduvjeti[0]), None)
                aktivnost.pocetniCvor = prethodnaAktivnost.krajnjiCvor
                prethodnaAktivnost.krajnjiCvor.izlazneAktivnosti.append(aktivnost)
                cvor = Cvor.noviCvor()
                self.dodajCvor(cvor)
                aktivnost.krajnjiCvor = cvor
                cvor.ulazneAktivnosti.append(aktivnost)
            else:
                # pronalazak svih preduvjetnih aktivnosti
                nizPreduvjeta = []
                for i in range(0, len(aktivnost.preduvjeti)):
                    nizPreduvjeta.append(next((x for x in self.aktivnosti if x.naziv == aktivnost.preduvjeti[i]), None))
                # cvor je novododani kraj fiktivnih aktivnosti, a početak stvarne aktivnosti
                cvor = Cvor.noviCvor()
                self.dodajCvor(cvor)
                for preduvjetnaAktivnost in nizPreduvjeta:
                    fiktivnaAktivnost = Aktivnost("fiktivna", [], 0, 0, 0)
                    # todo naknadno sam stavio da se spašavaju i fiktivne aktivnosti
                    # ne vjerujem da treba dodavati ove fiktivne aktivnosti
                    self.aktivnosti.append(fiktivnaAktivnost)
                    preduvjetnaAktivnost.krajnjiCvor.izlazneAktivnosti.append(fiktivnaAktivnost)
                    fiktivnaAktivnost.pocetniCvor = preduvjetnaAktivnost.krajnjiCvor
                    fiktivnaAktivnost.krajnjiCvor = cvor
                    cvor.ulazneAktivnosti.append(fiktivnaAktivnost)

                cvor.izlazneAktivnosti.append(aktivnost)
                aktivnost.pocetniCvor = cvor
                krCvor = Cvor.noviCvor()
                self.dodajCvor(krCvor)
                aktivnost.krajnjiCvor = krCvor
                krCvor.ulazneAktivnosti.append(aktivnost)
        self.odrediKrajnjiCvor()

    def odrediKrajnjiCvor(self):
        """
        Određuje krajnji čvor.
        Krajnji čvor je čvor iz kojeg ne izlazi niti jedna aktivnost.
        """
        for cvor in self.cvorovi:
            if len(cvor.izlazneAktivnosti) == 0:
                self.krajnjiCvor = cvor
                return

    # ima više krajnjih čvorova i zbog toga ništa ne radi
    def izbaciNepotrebneCvorove(self):
        """
        Skraćuje mrežni dijagram izbacivanjem nepotrebnih čvorova
        """
        #svođenje više krajnjih čvorova na samo jedan
        zadnjiCvor = Cvor.noviCvor()
        cvoroviZaBrisanje = []
        for cvor in self.cvorovi:
            if not cvor.izlazneAktivnosti:
                # sve aktivnosti preusmjeriti u jedan kraj
                zadnjiCvor.ulazneAktivnosti.extend(cvor.ulazneAktivnosti)
                for aktivnost in cvor.ulazneAktivnosti:
                    aktivnost.krajnjiCvor = zadnjiCvor
                cvoroviZaBrisanje.append(cvor)

        # obrisati ostale čvorove
        for cvor in cvoroviZaBrisanje:
            self.cvorovi.remove(cvor)
        self.dodajCvor(zadnjiCvor)
        self.krajnjiCvor = zadnjiCvor

    def renumerisiCvorove(self):
        """
        Vrši renumeraciju čvorova.
        Nakon izvršavanja funkcije čvorovi u grafu su pravilno (topološki) sortirani
        """
        imaPromjena = True
        i=0
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
            #todo ovo je dodano testirati
            #Algoritam mora terminirati u n iteracija inače pravilna numeracija ne postoji,
            # odnosno graf ima petlje
            i=i+1
            if i>len(self.cvorovi):
                raise RuntimeError("Graf ne smije imati petlje!")


        # todo provjeriti da nebi bilo problema nakon što se sortiraju u Pert klasi
        # sortiranje čvorova po rangu u rastućem poretku
        # key je težina nekog člana, a po defautu sortira u rastućem poretku
        self.cvorovi.sort(key=lambda x: x.rang)

        # renumeracija čvorova na osnovu ranga: najmanji rang najmanji broj čvora, brojanje počinje od 1
        for i in range(len(self.cvorovi)):
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

    # ovo nije ok kada ima više kritičnih puteva
    def odrediKriticnePuteve(self, trenutniCvor: Cvor, put: list):
        # označi trenutni čvor posjećenim
        trenutniCvor._posjecen = True
        put.append(trenutniCvor)
        # put.append(trenutniCvor.brojCvora)

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

    # todo Kako raditi kada ima više kritičnih puteva? Da li treba za svaki kritični put računati varijansu?
    def izracunajDevijacijuNaKriticnomPutu(self):
        varijansa = 0
        kriticniPut = self.kriticniPutevi[0]
        for i in range(1, len(kriticniPut)):
            # kritična aktivnost povezuje dva kritična događaja
            prviCvor = kriticniPut[i - 1]
            drugiCvor = kriticniPut[i]
            kriticnaAktivnost = next((x for x in prviCvor.izlazneAktivnosti if x.krajnjiCvor == drugiCvor), None)
            varijansa += kriticnaAktivnost.varijansa

        self._devijacijaNaKriticnomPutu = math.sqrt(varijansa)

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
        # self.izracunajNajranijaINajkasnijaVremena()
        self.izracunajRezerveCvorova()
        self.izracunajRezerveAktivnosti()
        self.odrediKriticnePuteve(self.pocetniCvor, [])
        self.izracunajDevijacijuNaKriticnomPutu()

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

    def izracunajProcjenuTrajanjaProjekta(self, p: decimal) -> decimal:
        """
        Računa trajanje projekta za zadanu vjerovatnoću Ts=Te+sigma*Fi^-1(P)

        :param p: Vjerovatnoća sa kojom se procjenjuje trajanje projekta
        """
        # return self.trajanjeProjekta + self._devijacijaNaKriticnomPutu * Pert.izracunajInverznoFi(p)
        return self.trajanjeProjekta + self._devijacijaNaKriticnomPutu * norm.ppf(p)

    # todo ovo nisam siguran
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
        string += "Trajanje projekta: " + str(self.trajanjeProjekta) + "\n"
        string += "Kritični putevi: \n" + self.dajStirngKriticnihPuteva()
        return string

    def dajStringKolekcije(self, kolekcija: list) -> str:
        """

        :param kolekcija: Lista čvorova ili lista aktivnosti u grafu.
        :return: String sa svim elementima iz kolekcije.
        """
        string = ""
        for clan in kolekcija:
            string += str(clan) + "\n"
        return string

    def dajStirngKriticnihPuteva(self) -> str:
        """

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
        Da li se item nalazi u grafu.

        :param item: Klasa Cvor ili klasa Aktivnost
        :return: Vraća True ako je čvor ili aktivnost u grafu
        """
        return (isinstance(item, Cvor) and (item in self.cvorovi)) or (
                isinstance(item, Aktivnost) and (item in self.aktivnosti))


if __name__ == "__main__":
    # graf = Pert()
    # graf.dodajAktivnost(Aktivnost("A", [], 1, 2, 3))
    # graf.dodajAktivnost(Aktivnost("B", ["A"], 4, 4, 4))
    # graf.dodajAktivnost(Aktivnost("C", ["B"], 4, 5, 12))
    # graf.dodajAktivnost(Aktivnost("D", ["B"], 9, 10, 11))
    # graf.dodajAktivnost(Aktivnost("E", ["B"], 19, 19, 19))
    # graf.dodajAktivnost(Aktivnost("F", ["C", "D"], 12, 12, 12))
    # graf.dodajAktivnost(Aktivnost("G", ["E", "F"], 6, 7, 14))
    # graf.dodajAktivnost(Aktivnost("H", ["E", "F"], 2, 4, 24))
    # graf.dodajAktivnost(Aktivnost("I", ["G"], 2, 4, 6))
    # graf.dodajAktivnost(Aktivnost("J", ["G", "H"], 3, 3, 3))
    # graf.azurirajGraf()
    # print(graf)
    # print(graf.izracunajProcjenuTrajanjaProjekta(0.25))
    # print(graf.izracunajProcjenuTrajanjaProjekta(0.9987))
    # if Decimal(0) - Decimal(0.000000000000002) == 0:
    #     print("ok")
    print(norm.cdf(norm.ppf(0.25)))
