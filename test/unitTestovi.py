import unittest
from pert import Pert
from pert import Aktivnost
from pert import Cvor

#todo odrediti najbolji način za testiranje

class MyTestCase(unittest.TestCase):
    #primjer 8.6.
    aktivnosti1=[Aktivnost("A", [], 1, 2, 3), Aktivnost("B", ["A"], 4, 4, 4), Aktivnost("C", ["B"], 4, 5, 12),
                 Aktivnost("D", ["B"], 9, 10, 11), Aktivnost("E", ["B"], 19, 19, 19),
                 Aktivnost("F", ["C", "D"], 12, 12, 12), Aktivnost("G", ["E", "F"], 6, 7, 14),
                 Aktivnost("H", ["E", "F"], 2, 4, 24), Aktivnost("I", ["G"], 2, 4, 6),
                 Aktivnost("J", ["G", "H"], 3, 3, 3)]

    #primjer 8.7.
    aktivnosti2 = [Aktivnost("A", [], 1, 2, 3), Aktivnost("B", [], 2, 3, 4), Aktivnost("C", ["A"], 2,4,5),
                   Aktivnost("D", ["B"], 1,3,4), Aktivnost("E", ["B"], 3,4,5),
                   Aktivnost("F", ["C", "D"], 2,3,4), Aktivnost("G", ["C", "D"], 6,8,10),
                   Aktivnost("H", ["F"], 4,6,7), Aktivnost("I", ["F"], 2,6,8),
                   Aktivnost("J", ["E", "G", "H"], 6,9,10), Aktivnost("K", ["I"], 1,2,3)]

    #primjer 8.8.
    aktivnosti3 = [Aktivnost("A", [], 3,6,10), Aktivnost("B", [], 2,3,4), Aktivnost("C", [], 2,2,2),
                   Aktivnost("D", ["C"], 2,2,2), Aktivnost("E", ["A"], 3,5,10),
                   Aktivnost("F", ["A"], 1,1,2), Aktivnost("G", ["B", "D"], 3,4,6),
                   Aktivnost("H", ["E"], 1,1,2), Aktivnost("I", ["F","G"], 3,4,5)]

    @staticmethod
    def dodajAktivnosti(graf:Pert, kolekcija:list[Aktivnost]):
        for aktivnost in kolekcija:
            graf.dodajAktivnost(aktivnost)

    # #ova se metoda izvršava prije svakog testa
    # def setUp(self):
    #     self.graf = Pert()
    #     MyTestCase.dodajAktivnosti(self.graf, MyTestCase.aktivnosti1)
    #     self.graf.azurirajGraf()
    #
    # #ova metoda se izvršava nakon svakog testa
    # def tearDown(self):
    #     self.graf=None

    def testTrajanja1(self):
        self.graf = Pert()
        MyTestCase.dodajAktivnosti(self.graf, MyTestCase.aktivnosti1)
        self.graf.azurirajGraf()
        self.assertEqual(40, self.graf.trajanjeProjekta)

    def testProcjeneTrajanja1(self):
        self.graf = Pert()
        MyTestCase.dodajAktivnosti(self.graf, MyTestCase.aktivnosti1)
        self.graf.azurirajGraf()
        # za vjerovatnoću 0.25
        self.assertEqual(38.95, round(self.graf.izracunajProcjenuTrajanjaProjekta(0.25),2))
        # za vjerovatnoću 0.75
        self.assertEqual(41.05, round(self.graf.izracunajProcjenuTrajanjaProjekta(0.75), 2))
        # za vjerovatnoću 0.9987
        self.assertEqual(44.71, round(self.graf.izracunajProcjenuTrajanjaProjekta(0.9987), 2))


    def testTrajanja2(self):
        self.graf = Pert()
        MyTestCase.dodajAktivnosti(self.graf, MyTestCase.aktivnosti2)
        self.graf.azurirajGraf()
        self.assertEqual(23.33, round(self.graf.trajanjeProjekta,2))

    #imaju 2 kritična puta
    def testKriticnogPuta2(self):
        self.graf = Pert()
        MyTestCase.dodajAktivnosti(self.graf, MyTestCase.aktivnosti2)
        self.graf.azurirajGraf()
        ocekivano="A - C - fiktivna - F - H - fiktivna - J\nB - D - fiktivna - F - H - fiktivna - J\n"
        self.assertEqual(ocekivano, self.graf.dajStirngKriticnihPuteva())

    #test procjene trajanja kada imaju 2 kritična puta
    def testProcjeneTrajanja2(self):
        self.graf = Pert()
        MyTestCase.dodajAktivnosti(self.graf, MyTestCase.aktivnosti2)
        self.graf.azurirajGraf()
        # za vjerovatnoću 0.5
        self.assertEqual(23.33, round(self.graf.izracunajProcjenuTrajanjaProjekta(0.5), 2))
        # za vjerovatnoću 0.75
        self.assertEqual(24.06, round(self.graf.izracunajProcjenuTrajanjaProjekta(0.75), 2))

    def testTrajanja3(self):
        self.graf = Pert()
        MyTestCase.dodajAktivnosti(self.graf, MyTestCase.aktivnosti3)
        self.graf.azurirajGraf()
        self.assertEqual(12.83, round(self.graf.trajanjeProjekta, 2))

    def testVjerovatnoceZavrsetkaProjektaUPredvidjenomRoku(self):
        self.graf = Pert()
        MyTestCase.dodajAktivnosti(self.graf, MyTestCase.aktivnosti3)
        self.graf.azurirajGraf()
        self.assertEqual(0.31, round(self.graf.izracunajVjerovatnocuZavrsetkaProjekta(12), 2))
        self.assertEqual(0.76, round(self.graf.izracunajVjerovatnocuZavrsetkaProjekta(14), 2))


if __name__ == '__main__':
    unittest.main()
