from api import get_friends
from igraph import Graph, plot
import numpy as np

def get_network(users_ids, as_edgelist=True):
    labels = [0] # чтобы не выдавал ошибку при построении графф, если он несвязан
    edges = []
    id2num = {}
    for i in range(len(users_ids)):
        id2num.update({users_ids[i]:i+1}) # создаём координаты
        labels.append(i) # добавляем их в список
    for id in users_ids:
        try:
            friends = get_friends(id, "sex") # перебираем id друзей друзей
            edges.append((0, id2num[id]))
            for fr in friends: # перебираем друга из друзей друзей
                if fr["id"] in users_ids: # если друг есть в списке users_ids, то создаём ребро
                    edges.append((id2num[id], id2num[fr["id"]]))
        except:
            pass
    plot_graph((labels, edges))
    if as_edgelist:
        return edges
    else:
        matrix = []  
        for k in range(len(users_ids)):
            matrix.append([])
            for j in range(len(users_ids)):
                matrix[k].append(0)
        for edge in edges:
            i, j = edge
            matrix[i][j] = 1
            matrix[j][i] = 1
        return matrix

def plot_graph(graph):
    vertices, edges = graph
    g = Graph(vertex_attrs={"label":vertices},
              edges=edges, directed=False)
    communities = g.community_edge_betweenness(directed=False)
    clusters = communities.as_clustering()
    print(clusters)
    g.simplify(multiple=True, loops=True)
    # Задаем стиль отображения графа
    N = len(vertices)
    visual_style = {}
    visual_style["layout"] = g.layout_fruchterman_reingold(
        maxiter=1000,
        area=N**3,
        repulserad=N**3)

    # Отрисовываем граф
    plot(g, **visual_style)
    



if __name__ == "__main__":
    ids = [id["id"] for id in get_friends(383328527, fields = "sex")]
    print(get_network(ids))
