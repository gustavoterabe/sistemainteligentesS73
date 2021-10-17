
class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()  

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]


class Graph():
    def __init__(self) -> None:
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost = 0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()

if __name__ == '__main__':

    g = graphCities.Graph()

    places = ['source','p1','p2','p3','p4','p5','p6','p7','p8','p9','p10','p11']

    for p in places:
        g.add_vertex(p)

    dist = {}
    dist['source'] =    [10, 120,220,310,390,460,520,570,610,640,660]
    dist['p1'] =        [20, 130,230,320,400,470,530,580,620,650]
    dist['p2'] =        [30, 140,240,330,410,480,540,590,630]
    dist['p3'] =        [40, 150,250,340,420,490,550,600]
    dist['p4'] =        [50, 160,260,350,430,500,560]
    dist['p5'] =        [60, 170,270,360,440,510]
    dist['p6'] =        [70, 180,280,370,450]
    dist['p7'] =        [80, 190,290,380]
    dist['p8'] =        [90, 200,300]
    dist['p9'] =        [100,210]
    dist['p10'] =       [110]
    dist['p11'] =       []

    for i, city in enumerate(g.vert_dict):
        for j, cc in enumerate(dist):
            if j > i:
                g.add_edge(city, cc, dist[city][j-i-1])
                
    for v in g:
        for w in v.get_connections():
            vid = v.get_id()
            wid = w.get_id()
            print (f"{vid} , {wid}, {v.get_weight(w)}")
