import unittest
from pert import Pert
from pert import Aktivnost
from pert import Cvor


# todo odrediti najbolji način za testiranje
# Strukturalno (White box testiranje)


# Inkrementalno bottom up testiranje

class TestoviCvora(unittest.TestCase):
    # ova se metoda izvršava prije svakog testa
    def setUp(self):
        self.cvor = Cvor(1)

    def testKreiranjaCvoraSaCijelimBrojem(self):
        c = Cvor(5)
        self.assertEqual(c.brojCvora, 5)

    def testIzuzetkaZaKreiranjeCvoraSaFPBrojem(self):
        with self.assertRaises(ValueError):
            c = Cvor(5.2)
        with self.assertRaisesRegex(ValueError, "Broj čvora treba biti cijeli broj"):
            c = Cvor(5.2)

    def testPostavljanjaCijelogBrojaCvora(self):
        self.cvor.brojCvora = 2
        self.assertEqual(self.cvor.brojCvora, 2)

    def testPostavljanjaFPBrojaCvora(self):
        with self.assertRaisesRegex(ValueError, "Broj čvora treba biti cijeli broj"):
            self.cvor.brojCvora = 2.1

    def testPostavljanjaUlaznihAktivnosti(self):
        aktivnosti1 = [Aktivnost("A", [], 1, 2, 3), Aktivnost("B", ["A"], 4, 4, 4), Aktivnost("C", ["B"], 4, 5, 12)]
        self.assertEqual(len(self.cvor.ulazneAktivnosti), 0)
        self.cvor.ulazneAktivnosti = aktivnosti1
        self.assertEqual(len(self.cvor.ulazneAktivnosti), 3)

    def testPostavljanjaIzlaznihAktivnosti(self):
        aktivnosti1 = [Aktivnost("A", [], 1, 2, 3), Aktivnost("B", ["A"], 4, 4, 4), Aktivnost("C", ["B"], 4, 5, 12)]
        self.assertEqual(len(self.cvor.izlazneAktivnosti), 0)
        self.cvor.izlazneAktivnosti = aktivnosti1
        self.assertEqual(len(self.cvor.izlazneAktivnosti), 3)

    def testPostavljanjaNajranijegVremena(self):
        self.assertEqual(self.cvor.najranijeVrijeme, 0)
        self.cvor.najranijeVrijeme = 5
        self.assertEqual(self.cvor.najranijeVrijeme, 5)

    def testPostavljanjaNajkasnijegVremena(self):
        self.assertEqual(self.cvor.najkasnijeVrijeme, 0)
        self.cvor.najkasnijeVrijeme = 5
        self.assertEqual(self.cvor.najkasnijeVrijeme, 5)

    def testPostavljanjaRanga(self):
        self.assertEqual(self.cvor.rang, 0)
        self.cvor.rang = 5
        self.assertEqual(self.cvor.rang, 5)

    def testPostavljanjaRezerve(self):
        self.assertEqual(self.cvor.rezerva, 0)
        self.cvor.najkasnijeVrijeme = 5.2
        self.cvor.najranijeVrijeme = 2.2
        self.cvor.izracunajRezervu()
        self.assertEqual(self.cvor.rezerva, 3)

    def testFunkcijeNoviCvor(self):
        Cvor.brojac = 0
        c = Cvor.noviCvor()
        self.assertEqual(c.brojCvora, 1)
        c = Cvor.noviCvor()
        self.assertEqual(c.brojCvora, 2)

    def testIspisivanjaCvora(self):
        string = str(self.cvor)
        self.assertEqual(string, "{Broj čvora: 1, Najranije vrijeme: 0, Najkasnije vrijeme: 0}")

    def testPoredjenjaCvorovaNaJednakost(self):
        c = Cvor(1)
        self.assertTrue(c == self.cvor)

    def testPoredjenjaCvorovaNaNejednakost(self):
        c = Cvor(2)
        self.assertTrue(c != self.cvor)


class TestoviAktivnosti(unittest.TestCase):
    # ova se metoda izvršava prije svakog testa
    def setUp(self):
        self.aktivnost = Aktivnost("C", ["B"], 4, 5, 12)

    def testVarijanseAktivnosti(self):
        a = Aktivnost("A", [], 6, 5, 12)
        self.assertEqual(a.varijansa, 1)

    def testPostavljanjaNazivaAktivnosti(self):
        self.assertEqual(self.aktivnost.naziv, "C")
        self.aktivnost.naziv = "D"
        self.assertEqual(self.aktivnost.naziv, "D")

    def testPostavljanjaTrajanjaAktivnosti(self):
        self.assertEqual(self.aktivnost.trajannje, 6)
        self.aktivnost.trajannje = 3.3
        self.assertEqual(self.aktivnost.trajannje, 3.3)

    def testPostavljanjaPreduvjetaAktivnosti(self):
        a = Aktivnost("D", ["A"], 4, 5, 12)
        self.assertEqual(len(self.aktivnost.preduvjeti), 1)
        self.aktivnost.preduvjeti = ["A", "B", "C"]
        self.assertEqual(len(self.aktivnost.preduvjeti), 3)
        self.assertIn("A", self.aktivnost.preduvjeti)
        self.assertIn("B", self.aktivnost.preduvjeti)
        self.assertIn("C", self.aktivnost.preduvjeti)

    def testPostavljanjaPocetnogCvoraAktivnosti(self):
        self.assertIsNone(self.aktivnost.pocetniCvor)
        c = Cvor(1)
        self.aktivnost.pocetniCvor = c
        self.assertIsInstance(self.aktivnost.pocetniCvor, Cvor)
        self.assertEqual(self.aktivnost.pocetniCvor, c)

    def testPostavljanjaKrajnjegCvoraAktivnosti(self):
        self.assertIsNone(self.aktivnost.krajnjiCvor)
        c = Cvor(1)
        self.aktivnost.krajnjiCvor = c
        self.assertIsInstance(self.aktivnost.krajnjiCvor, Cvor)
        self.assertEqual(self.aktivnost.krajnjiCvor, c)

    def testIzracunavanjaRezerveAktivnosti(self):
        self.assertEqual(self.aktivnost.rezervaAktivnosti, 0)
        c1 = Cvor(1)
        c1.najranijeVrijeme = 4
        c2 = Cvor(2)
        c2.najkasnijeVrijeme = 12
        self.aktivnost.pocetniCvor = c1
        self.aktivnost.krajnjiCvor = c2
        self.aktivnost.izracunajRezervu()
        self.assertEqual(self.aktivnost.rezervaAktivnosti, 2)

    def testIzracunavanjaOcekivanogTrajanjaAktivnosti(self):
        self.assertEqual(self.aktivnost.izracunajOcekivanoVrijeme(4, 5, 12), 6)

    def testIzracunavanjaVarijanseAktivnosti(self):
        self.assertEqual(self.aktivnost.izracunajVarijansu(6, 12), 1)

    def testIspisivanjaAktivnosti(self):
        string = str(self.aktivnost)
        self.assertEqual(string, "{Naziv aktivnosti: C, Trajanje aktivnosti: 6.0}")

    def testPoredjenjaAktivnostiNaJednakost(self):
        a = Aktivnost("C", ["B"], 4, 5, 12)
        self.assertTrue(a == self.aktivnost)

    def testPoredjenjaAktivnostiNaNejednakost(self):
        a = Aktivnost("D", ["A"], 4, 5, 12)
        self.assertTrue(a != self.aktivnost)


# todo Nedovršeno
class TestoviPertKlase(unittest.TestCase):
    # ova se metoda izvršava prije svakog testa
    def setUp(self):
        self.graf = Pert()
        self.graf.dodajAktivnost(Aktivnost("A", [], 1, 2, 3))
        self.graf.dodajAktivnost(Aktivnost("B", ["A"], 4, 4, 4))
        self.graf.dodajAktivnost(Aktivnost("C", ["B"], 4, 5, 12))
        self.graf.dodajAktivnost(Aktivnost("D", ["B"], 9, 10, 11))
        self.graf.dodajAktivnost(Aktivnost("E", ["B"], 19, 19, 19))
        self.graf.dodajAktivnost(Aktivnost("F", ["C", "D"], 12, 12, 12))
        self.graf.dodajAktivnost(Aktivnost("G", ["E", "F"], 6, 7, 14))
        self.graf.dodajAktivnost(Aktivnost("H", ["E", "F"], 2, 4, 24))
        self.graf.dodajAktivnost(Aktivnost("I", ["G"], 2, 4, 6))
        self.graf.dodajAktivnost(Aktivnost("J", ["G", "H"], 3, 3, 3))
        self.graf.kreirajStrukturu()

    # ova metoda se izvršava nakon svakog testa
    def tearDown(self):
        self.graf=None

    def testGetBrojCvorova(self):
        self.assertEqual(self.graf.getBrojCvorova(), 14)

    def testGetBrojAktivnosti(self):
        self.assertEqual(self.graf.getBrojAktivnosti(), 16)

    def testGetCvorSaBrojem(self):
        graf=Pert()
        graf.dodajAktivnost(Aktivnost("A", [], 1, 2, 3))
        cvor = graf.getCvorSaBrojem(1)
        self.assertIsNotNone(cvor)
        self.assertIsInstance(cvor, Cvor)

    def testGetCvorSaBrojemIzuzetak(self):
        with self.assertRaisesRegex(ValueError, "Cvor sa brojem 20 ne postoji!"):
            cvor = self.graf.getCvorSaBrojem(20)

    def testDodavanjaAktivnosti(self):
        graf = Pert()
        a = Aktivnost("D", ["A"], 4, 5, 12)
        graf.dodajAktivnost(a)
        self.assertEqual(graf.getBrojAktivnosti(), 1)
        self.assertIsInstance(self.graf.aktivnosti[0], Aktivnost)
        self.assertIn(a, self.graf.aktivnosti)

    # todo za ovu metodu nacrtati graf i testirati minimalni obuhvat puteva

    # Ciklomatska kompleksnost
    # Pert.izbaciNepotrebneCvorove - C(17)
    # Pert.kreirajStrukturu - C(13)

    # todo napraviti test i za ovo: Ne smije mi se algoritam zbuniti
    # Provjeri sam 5.5 on ovo svede na pravilan oblik, ali mi u ovom primjeru iz čvora 2 izlaze aktivnost B i fiktivna koje se preklapaju
    # a zbog toga što je fiktivna to ne pravi problem
    # Ako bi htio ovo riješiti to bi bila ogromna komplikacija, jer bi moro sve do početka grafa ići i tražiti
    # self.graf.dodajAktivnost(Aktivnost("A", [], 1, 2, 3))
    # self.graf.dodajAktivnost(Aktivnost("B", ["A"], 1, 2, 3))
    # self.graf.dodajAktivnost(Aktivnost("C", ["A", "B"], 1, 2, 3))
    # self.graf.dodajAktivnost(Aktivnost("D", ["A", "B"], 1, 2, 3))

    # todo Promijenio sam u Pertu, sada je M=8 i treba promijeniti graf puteva i ovaj niz čvorova; test je i dalje dobar
    # Pert.kreirajStrukturu - M=9 bez for i if ova u lamba funkcijama za pretraživanje
    # test prolazi kroz grane: 1-2-3-19-20- 2-3-4-19-20- 2-3-4-5- 6-7-8-9-10- 6-7-9-10- 11-18-19-20- 2-3-4-5- 6-7-9-10-
    # 11- 12-13-14- 12-13-14-15-16-17- 15-16-17-18-19-20-21
    def testKreiranjaStrukture(self):
        # #prva Aktivnost, bez preduvjeta
        # #1-2-19-20-
        # self.graf.dodajAktivnost(Aktivnost("A", [], 1, 2, 3))
        # #Aktivnosti sa jednim preduvjetom
        # #2-3-4-19-20-
        # self.graf.dodajAktivnost(Aktivnost("B", ["A"], 1, 2, 3))
        # self.graf.dodajAktivnost(Aktivnost("C", ["A"], 1, 2, 3))
        # #Aktivnost sa dva preduvjeta
        # #2-3-4-5-6-7-9-10-6-7-9-10-11-12-13-14-12-13-14-15-16-17-15-16-17-18-19-20-
        # self.graf.dodajAktivnost(Aktivnost("D", ["B","C"], 1, 2, 3))
        # #Aktivnost sa dva ista preduvjeta kao neka prethodna
        # #2-3-4-5-6-7-9-10-11-18-19-20-21
        # self.graf.dodajAktivnost(Aktivnost("E", ["B","C"], 1, 2, 3))

        # aktivnosti su postavljene u setUp funkciji i kreirana je struktura
        # self.graf.kreirajStrukturu()
        self.assertEqual(self.graf.getBrojCvorova(), 14)
        # graf nije skraćen pa ima i fiktivne aktivnosti
        self.assertEqual(self.graf.getBrojAktivnosti(), 16)

    def testDajAktivnostiIzListeNaziva(self):
        niz = ["A", "E", "B"]
        aktivnosti = self.graf.dajAktivnostiIzListeNaziva(niz)
        self.assertEqual(len(aktivnosti), 3)
        for i in range(len(niz)):
            self.assertIsInstance(aktivnosti[i], Aktivnost)
            self.assertEqual(aktivnosti[i].naziv, niz[i])

    def testIzuzetkaDajAktivnostiIzListeNaziva(self):
        niz = ["A", "E", "K", "B"]
        with self.assertRaisesRegex(ValueError, "Aktivnost sa nazivom: K ne postoji."):
            aktivnosti = self.graf.dajAktivnostiIzListeNaziva(niz)

    # todo promijeniti
    # test prolazi kroz grane:1-2-3-4-5-6-7-8-9-10-11- 7-8-10-11-12-13-14-15-16-17-18-19-20- 2-3-5-6-7-8-10-11-12-13-17-18-19-20-
    # 2-3-5-6-7-8-10-11-12-18-19-20- 2-3-5-6-19-20- 21-22-23--21-22-23- 24-25-26-24-25-26-27
    def testIzbacivanjaNepotrebnihCvorova(self):
        # aktivnosti su postavljene u setUp funkciji
        # self.graf.kreirajStrukturu()
        self.graf.izbaciNepotrebneCvorove()
        # broj čvorova treba biti smanjen sa 14 na 10
        self.assertEqual(self.graf.getBrojCvorova(), 10)
        self.assertEqual(self.graf.getBrojAktivnosti(), 13)

    #todo zbog redolsijeda izvršavanja testova ova 3 testa padaju
    #pomoćna funkcija
    def kreirajGraf(self):
        graf = Pert()
        graf.dodajAktivnost(Aktivnost("A", [], 1, 2, 3))
        graf.dodajAktivnost(Aktivnost("B", ["A"], 4, 4, 4))
        graf.dodajAktivnost(Aktivnost("C", ["B"], 4, 5, 12))
        graf.dodajAktivnost(Aktivnost("D", ["B"], 9, 10, 11))
        graf.dodajAktivnost(Aktivnost("E", ["B"], 19, 19, 19))
        graf.dodajAktivnost(Aktivnost("F", ["C", "D"], 12, 12, 12))
        graf.dodajAktivnost(Aktivnost("G", ["E", "F"], 6, 7, 14))
        graf.dodajAktivnost(Aktivnost("H", ["E", "F"], 2, 4, 24))
        graf.dodajAktivnost(Aktivnost("I", ["G"], 2, 4, 6))
        graf.dodajAktivnost(Aktivnost("J", ["G", "H"], 3, 3, 3))
        graf.kreirajStrukturu()
        return graf

    #
    # test prolazi kroz grane: 1-2-3-4-5-6-7- 3-4-6-7-8- 9-10-11-12-13-11-12-13-15-16- 9-10-14-15-16-17
    def testSvodjenjaNaJedanKraj1(self):
        graf=self.kreirajGraf()
        krajnjiCvorovi = [graf.getCvorSaBrojem(12), graf.getCvorSaBrojem(14)]

        cvoroviZaBrisanje = graf.svediNaJedanKraj(krajnjiCvorovi)
        self.assertEqual(len(cvoroviZaBrisanje), 2)
        self.assertEqual(graf.krajnjiCvor, graf.getCvorSaBrojem(15))

    def testSvodjenjaNaJedanKraj2(self):
        graf = self.kreirajGraf()
        # ovo će obrisati više krajeva
        graf.izbaciNepotrebneCvorove()
        krajnjiCvorovi = [graf.getCvorSaBrojem(15)]

        cvoroviZaBrisanje = graf.svediNaJedanKraj(krajnjiCvorovi)
        self.assertEqual(len(cvoroviZaBrisanje), 0)
        self.assertEqual(graf.krajnjiCvor, graf.getCvorSaBrojem(15))

    def testSvodjenjaNaJedanKraj3(self):
        graf = self.kreirajGraf()
        krajnjiCvorovi = [graf.getCvorSaBrojem(10), graf.getCvorSaBrojem(11)]

        cvoroviZaBrisanje = graf.svediNaJedanKraj(krajnjiCvorovi)
        self.assertEqual(len(cvoroviZaBrisanje), 0)

    def testRenumerisiCvorove(self):
        self.graf.izbaciNepotrebneCvorove()
        self.graf.renumerisiCvorove()
        cvorovi = self.graf.cvorovi
        for i in range(len(cvorovi)):
            self.assertEqual(cvorovi[i].brojCvora, i + 1)

    def testRenumerisiCvoroveIzuzetak(self):
        graf = Pert()
        graf.dodajAktivnost(Aktivnost("A", [], 1, 2, 3))
        b = Aktivnost("B", ["A"], 1, 2, 3)
        graf.dodajAktivnost(b)
        # graf.dodajAktivnost(Aktivnost("C", ["B"], 1, 2, 3))
        graf.kreirajStrukturu()
        # preusmjeravam B da bih napravio petlju cvorova 1-2-1
        graf.cvorovi.remove(graf.cvorovi[2])
        cvor1 = graf.cvorovi[0]
        b.krajnjiCvor = cvor1
        cvor1.ulazneAktivnosti.append(b)
        with self.assertRaisesRegex(RuntimeError, "Graf ne smije imati petlje!"):
            graf.renumerisiCvorove()

    def testIzracunajNajranijaVremena(self):
        self.graf.izbaciNepotrebneCvorove()
        self.graf.renumerisiCvorove()
        self.graf.izracunajNajranijaVremena()
        # ako je dobro izračunato zadnji čvor treba imati vrijednost 40
        self.assertEqual(self.graf.getCvorSaBrojem(10).najranijeVrijeme, 40)

    def testIzracunajNajkasnijaVremena(self):
        self.graf.izbaciNepotrebneCvorove()
        self.graf.renumerisiCvorove()
        self.graf.izracunajNajranijaVremena()
        self.graf.izracunajNajkasnijaVremena()
        # ako je dobro izračunato prvi čvor treba imati vrijednost 0
        self.assertEqual(self.graf.getCvorSaBrojem(1).najkasnijeVrijeme, 0)

    def testOdrediKriticnePuteve(self):
        self.graf.izbaciNepotrebneCvorove()
        self.graf.renumerisiCvorove()
        self.graf.izracunajNajranijaVremena()
        self.graf.izracunajNajkasnijaVremena()
        self.graf.izracunajRezerveCvorova()
        self.graf.odrediKriticnePuteve(self.graf.pocetniCvor, [])
        actual = self.graf.dajStirngKriticnihPuteva()
        expected = "A - B - C - F - fiktivna - G - I\nA - B - D - fiktivna - F - fiktivna - G - I\nA - B - E - G - I\n"
        self.assertEqual(actual, expected)

    # provjera na osnovu tabele iz primjera 8.6
    # ovdje se testiraju istovremeno i funkcije: izracunajTrajanjeNaPutu i izracunajDevijacijuNaPutu
    def testOdrediSvePuteve(self):
        self.graf.izbaciNepotrebneCvorove()
        self.graf.renumerisiCvorove()
        self.graf.izracunajNajranijaVremena()
        self.graf.izracunajNajkasnijaVremena()
        self.graf.izracunajRezerveCvorova()
        self.graf.odrediSvePuteve(self.graf.pocetniCvor, [])
        putevi = self.graf.sviPuteviSaTrajanjemIDevijacijom
        trajanja = [36, 35, 34, 40, 39, 38, 37, 36, 35]
        devijacije = [2.03, 1.91, 3.92, 1.56, 1.41, 3.7, 1.53, 1.37, 3.68]
        self.assertEqual(len(putevi), 9)
        for i in range(len(putevi)):
            self.assertEqual(putevi[i][1], trajanja[i])
            # zaokružuje na 2 decimale i poredi
            self.assertAlmostEqual(putevi[i][2], devijacije[i], places=2)

    def testIzracunajDevijacijuNaKriticnomPutu(self):
        self.graf.izbaciNepotrebneCvorove()
        self.graf.renumerisiCvorove()
        self.graf.izracunajNajranijaVremena()
        self.graf.izracunajNajkasnijaVremena()
        self.graf.izracunajRezerveCvorova()
        self.graf.odrediKriticnePuteve(self.graf.pocetniCvor, [])
        self.graf.izracunajDevijacijuNaKriticnomPutu()
        # zaokružuje na 2 decimale i poredi
        self.assertAlmostEqual(self.graf.devijacijaNaKriticnomPutu, 1.53, places=2)

    # ovo se testira u sistemskim testovima
    # def testAzurirajGraf(self):
    #     pass

    # todo
    def testIzracunajRezerveCvorova(self):
        self.graf.izbaciNepotrebneCvorove()
        self.graf.renumerisiCvorove()
        self.graf.izracunajNajranijaVremena()
        self.graf.izracunajNajkasnijaVremena()
        self.graf.izracunajRezerveCvorova()

        rezerve=[0,0,0,0,0,0,0,0,1,0]
        for i in range(self.graf.getBrojCvorova()):
            self.assertEqual(self.graf.cvorovi[i].rezerva,rezerve[i])

    def testIzracunajRezerveAktivnosti(self):
        self.graf.izbaciNepotrebneCvorove()
        self.graf.renumerisiCvorove()
        self.graf.izracunajNajranijaVremena()
        self.graf.izracunajNajkasnijaVremena()
        self.graf.izracunajRezerveAktivnosti()

        #todo provjeriti ovo što je rezerva negativna
        rezerve = [0,0,4,0,3,0,0,2,0,1,0,1,-36]
        for i in range(self.graf.getBrojAktivnosti()):
            self.assertEqual(self.graf.aktivnosti[i].rezervaAktivnosti, rezerve[i])

    #u sistemskim testovima
    # def testIzracunajTrajanjeProjekta(self):
    #     pass

    # def testIzracunajTrajanjeNaPutu(self):
    #     pass

    #u sistemskim testovima
    # def testIzracunajProcjenuTrajanjaProjekta(self):
    #     pass

    # def testIzracunajNajduzuProcjenuTrajanjaProjekta(self):
    #     pass

    # def testIzracunajVjerovatnocuZavrsetkaProjekta(self):
    #     pass

    # todo popraviti nakon što naprqavim da se devijacija prikazuje sa 2 decimale
    def testDajStringSvihPuteva(self):
        self.graf.izbaciNepotrebneCvorove()
        self.graf.renumerisiCvorove()
        self.graf.izracunajNajranijaVremena()
        self.graf.izracunajNajkasnijaVremena()
        self.graf.izracunajTrajanjeProjekta()
        self.graf.izracunajRezerveCvorova()
        self.graf.odrediSvePuteve(self.graf.pocetniCvor, [])
        actual = self.graf.dajStringSvihPuteva()
        expected="1 - 2 - 3 - 5 - 6 - 7 - 8 - 10 Trajanje: 36.0 Devijacija: 2.03\n" \
                 "1 - 2 - 3 - 5 - 6 - 7 - 8 - 9 - 10 Trajanje: 35.0 Devijacija: 1.91\n" \
                 "1 - 2 - 3 - 5 - 6 - 7 - 9 - 10 Trajanje: 34.0 Devijacija: 3.92\n" \
                 "1 - 2 - 3 - 4 - 5 - 6 - 7 - 8 - 10 Trajanje: 40.0 Devijacija: 1.56\n" \
                 "1 - 2 - 3 - 4 - 5 - 6 - 7 - 8 - 9 - 10 Trajanje: 39.0 Devijacija: 1.41\n" \
                 "1 - 2 - 3 - 4 - 5 - 6 - 7 - 9 - 10 Trajanje: 38.0 Devijacija: 3.7\n" \
                 "1 - 2 - 3 - 7 - 8 - 10 Trajanje: 37.0 Devijacija: 1.53\n" \
                 "1 - 2 - 3 - 7 - 8 - 9 - 10 Trajanje: 36.0 Devijacija: 1.37\n" \
                 "1 - 2 - 3 - 7 - 9 - 10 Trajanje: 35.0 Devijacija: 3.68\n"
        self.assertEqual(actual,expected)

    # def testDajStirngKriticnihPuteva(self):
    #     pass

    def testDodavanjaAktivnostiSaIstimImenom(self):
        with self.assertRaisesRegex(ValueError, "Aktivnost već postoji, nije je moguće dodati"):
            self.graf.dodajAktivnost(Aktivnost("F", ["A", "C"], 1,3,4))


# Sistemsko testiranje
class TestCitavogAlgoritma(unittest.TestCase):
    # primjer 8.6.
    aktivnosti1 = [Aktivnost("A", [], 1, 2, 3), Aktivnost("B", ["A"], 4, 4, 4), Aktivnost("C", ["B"], 4, 5, 12),
                   Aktivnost("D", ["B"], 9, 10, 11), Aktivnost("E", ["B"], 19, 19, 19),
                   Aktivnost("F", ["C", "D"], 12, 12, 12), Aktivnost("G", ["E", "F"], 6, 7, 14),
                   Aktivnost("H", ["E", "F"], 2, 4, 24), Aktivnost("I", ["G"], 2, 4, 6),
                   Aktivnost("J", ["G", "H"], 3, 3, 3)]

    # primjer 8.7.
    aktivnosti2 = [Aktivnost("A", [], 1, 2, 3), Aktivnost("B", [], 2, 3, 4), Aktivnost("C", ["A"], 2, 4, 5),
                   Aktivnost("D", ["B"], 1, 3, 4), Aktivnost("E", ["B"], 3, 4, 5),
                   Aktivnost("F", ["C", "D"], 2, 3, 4), Aktivnost("G", ["C", "D"], 6, 8, 10),
                   Aktivnost("H", ["F"], 4, 6, 7), Aktivnost("I", ["F"], 2, 6, 8),
                   Aktivnost("J", ["E", "G", "H"], 6, 9, 10), Aktivnost("K", ["I"], 1, 2, 3)]

    # primjer 8.8.
    aktivnosti3 = [Aktivnost("A", [], 3, 6, 10), Aktivnost("B", [], 2, 3, 4), Aktivnost("C", [], 2, 2, 2),
                   Aktivnost("D", ["C"], 2, 2, 2), Aktivnost("E", ["A"], 3, 5, 10),
                   Aktivnost("F", ["A"], 1, 1, 2), Aktivnost("G", ["B", "D"], 3, 4, 6),
                   Aktivnost("H", ["E"], 1, 1, 2), Aktivnost("I", ["F", "G"], 3, 4, 5)]

    @staticmethod
    def dodajAktivnosti(graf: Pert, kolekcija: list[Aktivnost]):
        for aktivnost in kolekcija:
            graf.dodajAktivnost(aktivnost)


    # #ova se metoda izvršava prije svakog testa
    # def setUp(self):
    #     self.graf = Pert()
    #     TestCitavogAlgoritma.dodajAktivnosti(self.graf, TestCitavogAlgoritma.aktivnosti1)
    #     self.graf.azurirajGraf()
    #
    # #ova metoda se izvršava nakon svakog testa
    # def tearDown(self):
    #     self.graf=None

    def testTrajanja1(self):
        self.graf = Pert()
        TestCitavogAlgoritma.dodajAktivnosti(self.graf, TestCitavogAlgoritma.aktivnosti1)
        self.graf.azurirajGraf()
        self.assertEqual(40, self.graf.trajanjeProjekta)

    def testProcjeneTrajanja1(self):
        self.graf = Pert()
        TestCitavogAlgoritma.dodajAktivnosti(self.graf, TestCitavogAlgoritma.aktivnosti1)
        self.graf.azurirajGraf()
        # za vjerovatnoću 0.25
        self.assertEqual(38.97, round(self.graf.izracunajProcjenuTrajanjaProjekta(0.25), 2))
        # za vjerovatnoću 0.75
        self.assertEqual(41.03, round(self.graf.izracunajProcjenuTrajanjaProjekta(0.75), 2))
        # za vjerovatnoću 0.9987
        self.assertEqual(44.6, round(self.graf.izracunajProcjenuTrajanjaProjekta(0.9987), 2))

        # ovo je verzija bez skraćivanja
        # # za vjerovatnoću 0.25
        # self.assertEqual(38.95, round(self.graf.izracunajProcjenuTrajanjaProjekta(0.25),2))
        # # za vjerovatnoću 0.75
        # self.assertEqual(41.05, round(self.graf.izracunajProcjenuTrajanjaProjekta(0.75), 2))
        # # za vjerovatnoću 0.9987
        # self.assertEqual(44.71, round(self.graf.izracunajProcjenuTrajanjaProjekta(0.9987), 2))

    def testIzracunajNajduzuProcjenuTrajanjaProjekta1(self):
        self.graf = Pert()
        TestCitavogAlgoritma.dodajAktivnosti(self.graf, TestCitavogAlgoritma.aktivnosti1)
        self.graf.azurirajGraf()
        # za vjerovatnoću 0.25
        self.assertAlmostEqual(38.95, self.graf.izracunajNajduzuProcjenuTrajanjaProjekta(0.25), 2)
        # za vjerovatnoću 0.75
        self.assertAlmostEqual(41.05, self.graf.izracunajNajduzuProcjenuTrajanjaProjekta(0.75), 2)
        # za vjerovatnoću 0.9987
        self.assertAlmostEqual(49.13, self.graf.izracunajNajduzuProcjenuTrajanjaProjekta(0.9987),2)

    def testTrajanja2(self):
        self.graf = Pert()
        TestCitavogAlgoritma.dodajAktivnosti(self.graf, TestCitavogAlgoritma.aktivnosti2)
        self.graf.azurirajGraf()
        self.assertEqual(23.33, round(self.graf.trajanjeProjekta, 2))

    # imaju 2 kritična puta
    def testKriticnogPuta2(self):
        self.graf = Pert()
        TestCitavogAlgoritma.dodajAktivnosti(self.graf, TestCitavogAlgoritma.aktivnosti2)
        self.graf.azurirajGraf()
        # ovo je za verziju bez izbacvanja čvorova
        # ocekivano="A - C - fiktivna - F - H - fiktivna - J\nB - D - fiktivna - F - H - fiktivna - J\n"
        # ovo je za verziju sa izbacivanjem
        ocekivano = "A - C - F - H - fiktivna - J\nB - D - fiktivna - F - H - fiktivna - J\n"
        self.assertEqual(ocekivano, self.graf.dajStirngKriticnihPuteva())

    # test procjene trajanja kada imaju 2 kritična puta
    def testProcjeneTrajanja2(self):
        self.graf = Pert()
        TestCitavogAlgoritma.dodajAktivnosti(self.graf, TestCitavogAlgoritma.aktivnosti2)
        self.graf.azurirajGraf()
        # za vjerovatnoću 0.5
        self.assertEqual(23.33, round(self.graf.izracunajProcjenuTrajanjaProjekta(0.5), 2))
        # za vjerovatnoću 0.75
        self.assertEqual(24.06, round(self.graf.izracunajProcjenuTrajanjaProjekta(0.75), 2))

    def testTrajanja3(self):
        self.graf = Pert()
        TestCitavogAlgoritma.dodajAktivnosti(self.graf, TestCitavogAlgoritma.aktivnosti3)
        self.graf.azurirajGraf()
        self.assertEqual(12.83, round(self.graf.trajanjeProjekta, 2))

    # def testVjerovatnoceZavrsetkaProjektaUPredvidjenomRoku(self):
    def testIzracunajVjerovatnocuZavrsetkaProjekta(self):
        self.graf = Pert()
        TestCitavogAlgoritma.dodajAktivnosti(self.graf, TestCitavogAlgoritma.aktivnosti3)
        self.graf.azurirajGraf()
        self.assertEqual(0.31, round(self.graf.izracunajVjerovatnocuZavrsetkaProjekta(12), 2))
        self.assertEqual(0.76, round(self.graf.izracunajVjerovatnocuZavrsetkaProjekta(14), 2))

    def testIspisaGrafa1(self):
        self.graf = Pert()
        TestCitavogAlgoritma.dodajAktivnosti(self.graf, TestCitavogAlgoritma.aktivnosti1)
        self.graf.azurirajGraf()
        print(self.graf)


if __name__ == '__main__':
    unittest.main()

# todo računanje metrika
# ciklomatska kompleksnost: radon cc pert.py -s
# halstead: radon hal pert.py
