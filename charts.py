from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt


def createPertChart(veze, najranijaVremena, najkasnijaVremena, rezerveCvorova):
    """
    Kreira pert graf i spašava ga kao sliku 'pert.png'.

    :param veze: Dictionary oblika {pocetniCvor:(krajnjiCvor,nazivAktivnostiKojaIhPovezuje)}
    :param najranijaVremena: Dictionary oblika {cvor:najranijeVrijeme}
    :param najkasnijaVremena: Dictionary oblika {cvor:najkasnijeVrijeme}
    :param rezerveCvorova: Dictionary oblika {cvor:rezerva}
    """
    g = nx.DiGraph()
    labelsDict = {}
    edgeLabels = {}
    for pocetniCvor in veze:
        for par in veze[pocetniCvor]:
            krajnjiCvor = par[0]
            parentStr = '{}|{}|{}'.format(najranijaVremena[pocetniCvor], najkasnijaVremena[pocetniCvor], rezerveCvorova[pocetniCvor])
            childStr = '{}|{}|{}'.format(najranijaVremena[krajnjiCvor], najkasnijaVremena[krajnjiCvor], rezerveCvorova[krajnjiCvor])
            labelsDict[pocetniCvor] = parentStr
            labelsDict[krajnjiCvor] = childStr
            g.add_edge(pocetniCvor, krajnjiCvor, color='black')
            if par[1]!="fiktivna":
                edgeLabels[pocetniCvor, krajnjiCvor] = par[1]
            else:
                edgeLabels[pocetniCvor, krajnjiCvor] = '0'
    # pos = nx.shell_layout(g)
    pos = nx.planar_layout(g)
    for task in najranijaVremena:
        x, y = pos[task]
        plt.text(x, y + 0.1, s=labelsDict[task], bbox=dict(facecolor='red', alpha=0.5), horizontalalignment='center')
    print(nx.info(g))

    edges = g.edges()
    colors = [g[u][v]['color'] for u, v in edges]

    nx.draw(g, pos, with_labels=True, edge_color=colors)
    nx.draw_networkx_edge_labels(g, pos, edge_labels=edgeLabels, font_size=8)
    plt.savefig('pert.png', bbox_inches='tight')
    plt.show()


def createGanttChart(vremenaPocetka, vremenaZavrsetka, trajanja, rezerve):
    """
    Kreira gantogram i spašava ga kao sliku 'gantt.png'.

    :param vremenaPocetka: Dictionary oblika {nazivAktivnosti:vrijemePocetka}
    :param vremenaZavrsetka: Dictionary oblika {nazivAktivnosti:vrijemeZavrsetka}
    :param trajanja: Dictionary oblika {nazivAktivnosti:trajanje}
    :param rezerve: Dictionary oblika {nazivAktivnosti:rezerva}
    """
    fig, ax = plt.subplots()
    # nazivi aktivnosti sortirani prema vremenu početka, od najranijeg do najkasnijeg početka
    y_values = sorted(vremenaPocetka.keys(), key=lambda x: vremenaPocetka[x])
    y_start = 5
    y_height = 5
    for nazivAktivnosti in y_values:
        # plavom je prikazano trajanje aktivnosti (u tom periodu se aktivnost izvršava)
        ax.broken_barh([(vremenaPocetka[nazivAktivnosti], trajanja[nazivAktivnosti])], (y_start, y_height), facecolors='blue')
        # crvenom je prikazana rezerva aktivnosti
        ax.broken_barh([(vremenaZavrsetka[nazivAktivnosti] - rezerve[nazivAktivnosti], rezerve[nazivAktivnosti])], (y_start, y_height), facecolors='red')
        # ax.broken_barh([(vremenaZavrsetka[nazivAktivnosti], rezerve[nazivAktivnosti])], (y_start, y_height), facecolors='red')
        # Naziv aktivnosti se prikazuje na udaljenosti 0.5 od kraja linije
        ax.text(vremenaZavrsetka[nazivAktivnosti] + 0.5, y_start + y_height / 2, nazivAktivnosti)
        # ax.text(vremenaZavrsetka[nazivAktivnosti] + rezerve[nazivAktivnosti] + 0.5, y_start + y_height / 2, nazivAktivnosti)
        y_start += 10
    ax.set_xlim(0, max(vremenaZavrsetka.values()) + 5)
    ax.set_ylim(len(trajanja) * 10)
    ax.set_xlabel('Vrijeme')
    ax.set_ylabel('Aktivnosti')
    i = 0
    y_ticks = []
    while i < len(trajanja) * 10:
        y_ticks.append(i)
        i += 10
    ax.set_yticks(y_ticks)
    plt.tick_params(
        axis='y',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        left='off',  # ticks along the top edge are off
        labelleft='off')  # labels along the bottom edge are off
    plt.savefig('gantt.png', bbox_inches='tight')
    plt.show()
