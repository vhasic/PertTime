import unittest
from pert import Pert
from pert import Aktivnost
from pert import Cvor


# todo odrediti najbolji način za testiranje

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
        Cvor.brojac=0
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
        c=Cvor(1)
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
        self.assertEqual(self.aktivnost.rezervaAktivnosti,0)
        c1 = Cvor(1)
        c1.najranijeVrijeme=4
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
        pass









#Sistemsko testiranje
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

    def testVjerovatnoceZavrsetkaProjektaUPredvidjenomRoku(self):
        self.graf = Pert()
        TestCitavogAlgoritma.dodajAktivnosti(self.graf, TestCitavogAlgoritma.aktivnosti3)
        self.graf.azurirajGraf()
        self.assertEqual(0.31, round(self.graf.izracunajVjerovatnocuZavrsetkaProjekta(12), 2))
        self.assertEqual(0.76, round(self.graf.izracunajVjerovatnocuZavrsetkaProjekta(14), 2))

if __name__ == '__main__':
    unittest.main()
