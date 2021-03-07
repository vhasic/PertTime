import unittest
from pert import Pert
from pert import Aktivnost
from pert import Cvor


class MyTestCase(unittest.TestCase):
    def testTrajanja1(self):
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
        graf.azurirajGraf()
        self.assertEqual(40, graf.trajanjeProjekta)


if __name__ == '__main__':
    unittest.main()
