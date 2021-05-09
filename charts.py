from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt

#todo ovo preurediti tako da radi za moj graf
def createPertChart(graph, startTimes, completionTimes, slackTimes):
    g = nx.DiGraph()
    labelsDict = {}
    for parent in graph:
        for child in graph[parent]:
            # parentStr = 'TE={} TL={} R={}'.format(startTimes[parent], completionTimes[parent], slackTimes[parent])
            # childStr = 'TE={} TL={} R={}'.format(startTimes[child], completionTimes[child], slackTimes[child])
            parentStr = '{}/{}/{}'.format(startTimes[parent], completionTimes[parent], slackTimes[parent])
            childStr = '{}/{}/{}'.format(startTimes[child], completionTimes[child], slackTimes[child])
            labelsDict[parent] = parentStr
            labelsDict[child] = childStr
            g.add_edge(parent, child, color='black')
    # pos = nx.shell_layout(g)
    pos = nx.planar_layout(g)
    for task in startTimes:
        x, y = pos[task]
        plt.text(x, y + 0.1, s=labelsDict[task], bbox=dict(facecolor='red', alpha=0.5), horizontalalignment='center')
    print(nx.info(g))

    edges = g.edges()
    colors = [g[u][v]['color'] for u, v in edges]

    nx.draw(g, pos, with_labels=True, edge_color=colors)
    plt.savefig('pert.png', bbox_inches='tight')
    plt.show()


def createGanttChart(startTimes, completionTimes, durations, slackTimes):
    fig, ax = plt.subplots()
    y_values = sorted(startTimes.keys(), key=lambda x: startTimes[x])
    y_start = 5
    y_height = 5
    for value in y_values:
        ax.broken_barh([(startTimes[value], durations[value])], (y_start, y_height), facecolors='blue')
        ax.broken_barh([(completionTimes[value], slackTimes[value])], (y_start, y_height), facecolors='red')
        ax.text(completionTimes[value] + slackTimes[value] + 0.5, y_start + y_height / 2, value)
        y_start += 10
    ax.set_xlim(0, max(completionTimes.values()) + 5)
    ax.set_ylim(len(durations) * 10)
    ax.set_xlabel('Time')
    ax.set_ylabel('Tasks')
    i = 0
    y_ticks = []
    while i < len(durations) * 10:
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