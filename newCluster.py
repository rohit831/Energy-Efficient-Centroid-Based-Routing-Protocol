import random
import numpy as np

# Class which represents a single Node
class Node(object):
    def __init__(self, x, y, init_energy=float(0.5)):
        self.x = x
        self.y = y
        self.init_energy = init_energy
        self.curr_energy = init_energy
        self.node_type = int(0)
        self.dead_node = int(0)


# Class representing a particular cluster
class Cluster(object):
    def __init__(self, x, y, length, width, network_architecture):
        self.nodes = []  # List of all the nodes in a cluster
        self.cluster_head = None  # cluster head index
        self.relay_nodes = []  # tuple(relay nodes index, no of nodes under it)
        self.cluster_coords = []  # cluster coordinators index
        self.available_nodes = network_architecture.number_of_nodes  # no of available nodes

        # deployment and assigning relay nodes
        self.deploy_nodes(x, y, length, width, network_architecture)

        # sorting all the nodes in increasing order of x-axis
        self.nodes.sort(key=lambda t: t.x, reverse=False)

        # assign relay nodes based on centroid algorithm
        self.assign_relay_nodes(network_architecture)

        # select cluster head based on the relay nodes selected
        self.select_cluster_head()

    # deploys the nodes in the network architecture
    def deploy_nodes(self, x, y, length, width, network_architecture):
        for i in range(0, network_architecture.number_of_nodes):
            # applying random fn to generate coordinates of a node
            self.nodes.append(Node(random.uniform(x+0.01, x+length), random.uniform(y+0.01, y+width),
                                   network_architecture.init_energy))

    # assigns relay nodes based on the given network architecture
    def assign_relay_nodes(self, network_architecture):
        start=0
        end = 0

        while end < self.available_nodes:
            min_val = self.nodes[start].x
            while end < self.available_nodes and self.nodes[end].x - min_val <= network_architecture.threshold:
                end = end + 1

            #  select a relay nodes for nodes lying between start and end in self.nodes
            self.select_relay_node(start, end)
            start = end

    # select a relay node based on the start and end index provided
    def select_relay_node(self, start, end):
        relay_x = 0.0
        relay_y = 0.0
        available_nodes = []

        for t in range(start, end):
            relay_x += (self.nodes[t].curr_energy * self.nodes[t].x) / self.nodes[t].init_energy
            relay_y += (self.nodes[t].curr_energy * self.nodes[t].y) / self.nodes[t].init_energy
            available_nodes.append((self.nodes[t].x, self.nodes[t].y))

        relay_x = relay_x / (end - start)
        relay_y = relay_y / (end - start)
        relay_node = (relay_x, relay_y)

        index = -1
        dist = 9999999
        for ind, n in enumerate(available_nodes):
            if distance(relay_node, n) <= dist:
                dist = distance(relay_node, n)
                index = ind

        #  marking the node as relay node
        self.nodes[index + start].node_type = 1
        self.relay_nodes.append((index + start, end - start))

    # selects a cluster head based on given network architecture
    def select_cluster_head(self):
        cluster_x = 0.0
        cluster_y = 0.0

        # Applying the centroid algorithm
        for node in self.relay_nodes:
            cluster_x += (self.nodes[node[0]].curr_energy * self.nodes[node[0]].x) / self.nodes[node[0]].init_energy
            cluster_y += (self.nodes[node[0]].curr_energy * self.nodes[node[0]].y) / self.nodes[node[0]].init_energy

        cluster_x = cluster_x / len(self.relay_nodes)
        cluster_y = cluster_y / len(self.relay_nodes)
        cluster_node = (cluster_x, cluster_y)

        index = -1
        dist = 9999999
        for ind in range(0, self.available_nodes):
            if distance(cluster_node, (self.nodes[ind].x, self.nodes[ind].y)) <= dist:
                dist = distance(cluster_node, (self.nodes[ind].x, self.nodes[ind].y))
                index = ind

        # upgrading the node to act as Relay node
        self.nodes[index].node_type = 2
        self.cluster_head = index


# It gives us the eucledian distance between two points
def distance(pt_1, pt_2):
    pt_1 = np.array((pt_1[0], pt_1[1]))
    pt_2 = np.array((pt_2[0], pt_2[1]))
    return np.linalg.norm(pt_1-pt_2)


