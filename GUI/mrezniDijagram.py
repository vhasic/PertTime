from pert import Aktivnost
from pert import Pert

# libraries
# import pandas as pd
# import numpy as np
# import graphviz
import networkx as nx
import matplotlib.pyplot as plt

if __name__ == "__main__":
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

    #
    G = nx.DiGraph()

    # ovo je dictionary sa labelama
    labele = {}
    for cvor in graf.cvorovi:
        G.add_node(cvor.brojCvora)
        labele[cvor.brojCvora] = str(cvor.brojCvora) + " (" + str(cvor.najranijeVrijeme) + ", " + str(
            cvor.najkasnijeVrijeme) + ")"

    #
    edgeLabels = {}
    # todo kako dodati labele za aktivnosti i isprekidane fiktivne aktivnosti
    for aktivnost in graf.aktivnosti:
        # style = "solid"
        # if aktivnost.naziv == "fiktivna":
        #     style = "dashed"
        u = aktivnost.pocetniCvor.brojCvora
        v = aktivnost.krajnjiCvor.brojCvora
        G.add_edge(u, v, naziv=aktivnost.naziv)
        if aktivnost.naziv != "fiktivna":
            edgeLabels[(u, v)] = aktivnost.naziv + " (" + str(aktivnost.trajannje) + ")"
        else:
            # za fiktivne nije bitan naziv
            edgeLabels[(u, v)] = str(aktivnost.trajannje)

    # pos = nx.nx_agraph.graphviz_layout(G)
    # nx.draw(G, pos, labels=labele, with_labels=True, font_size=8)

    # pos = nx.spring_layout(G)
    # pos = nx.spring_layout(G, k=0.5, iterations=20)

    pos = nx.planar_layout(G)
    nx.draw(G, pos, labels=labele, with_labels=True, font_size=8)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edgeLabels, font_size=8)

    # pos = nx.planar_layout(G)
    # nx.draw(G, pos, labels=labele, with_labels=True, font_size=8)
    # ivice=nx.draw_networkx_edges(G,pos)
    # for ivica in ivice:
    #     ivica.set_linestyle('dotted')
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=edgeLabels, font_size=8)

    plt.show()
