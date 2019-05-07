import math
import numpy as np
from displayResults import *


# Function to depict energy consumption of normal nodes in a single round of operation
def normal_node_energy_consumption(network_architecture, clusters):
    d0 = math.sqrt(network_architecture.fs_energy / network_architecture.mp_energy)
    ETX = network_architecture.trans_energy
    ERX = network_architecture.rec_energy
    EDA = network_architecture.agg_energy
    Emp = network_architecture.mp_energy
    Efs = network_architecture.fs_energy
    packet_length = network_architecture.pckt_len

    for c in clusters:
        tmp = c.relay_nodes[0][1]
        relay_no = 0
        for n in range(0, c.available_nodes):
            if n >= tmp:
                relay_no = relay_no + 1
                tmp = tmp + c.relay_nodes[relay_no][1]
            if c.nodes[n].node_type == 0:
                dist = distance(c.nodes[n], c.nodes[c.relay_nodes[relay_no][0]])

                if dist > d0:
                    c.nodes[n].curr_energy = c.nodes[n].curr_energy - packet_length * ETX + Emp * packet_length * (
                            dist ** 4)
                else:
                    c.nodes[n].curr_energy = c.nodes[n].curr_energy - packet_length * ETX + Efs * packet_length * (
                                dist ** 2)
                if dist > 0:
                    c.nodes[c.relay_nodes[relay_no][0]].curr_energy = c.nodes[c.relay_nodes[relay_no][0]].curr_energy -\
                                                                      ((ERX + EDA) * packet_length)


# Function to depict energy consumption of relay nodes in a single round of operation
def relay_node_energy_consumption(network_architecture, clusters):
    d0 = math.sqrt(network_architecture.fs_energy/network_architecture.mp_energy)
    ETX = network_architecture.trans_energy
    ERX = network_architecture.rec_energy
    EDA = network_architecture.agg_energy
    Emp = network_architecture.mp_energy
    Efs = network_architecture.fs_energy
    packet_length = network_architecture.pckt_len

    for c in clusters:
        for r in c.relay_nodes:
            dist = distance(c.nodes[r[0]], c.nodes[c.cluster_head])
            energy = c.nodes[r[0]].curr_energy
            if dist >= d0:
                c.nodes[r[0]].curr_energy = energy - ((ETX + EDA)*packet_length + Emp * packet_length * (dist ** 4))
            else:
                c.nodes[r[0]].curr_energy = energy - ((ETX + EDA)*packet_length + Efs * packet_length * (dist ** 2))
            c.nodes[r[0]].curr_energy = c.nodes[r[0]].curr_energy - packet_length * ERX * r[1]


# Function to depict energy consumption of cluster head in single round of operation
def cluster_head_energy_consumption(network_architecture, clusters):
    d0 = math.sqrt(network_architecture.fs_energy/network_architecture.mp_energy)
    ETX = network_architecture.trans_energy
    ERX = network_architecture.rec_energy
    EDA = network_architecture.agg_energy
    Emp = network_architecture.mp_energy
    Efs = network_architecture.fs_energy
    packet_length = network_architecture.pckt_len

    # traversing all the clusters leaving the last cluster since it communicates directly with the base station
    for c in range(0, network_architecture.no_of_clusters - 1):
        tup = clusters[c].cluster_coords[0]
        dist = distance(clusters[c].nodes[clusters[c].cluster_head], clusters[tup[0]].nodes[tup[1]])
        energy = clusters[c].nodes[clusters[c].cluster_head].curr_energy
        if dist >= d0:
            clusters[c].nodes[clusters[c].cluster_head].curr_energy = energy -\
                                    ((ETX + EDA)*packet_length + Emp * packet_length * (dist ** 4))
        else:
            clusters[c].nodes[clusters[c].cluster_head].curr_energy = energy\
                                                    - ((ETX + EDA)*packet_length + Efs * packet_length * (dist ** 2))
        clusters[c].nodes[clusters[c].cluster_head].curr_energy = clusters[c].nodes[clusters[c].cluster_head].curr_energy\
                                                        - packet_length * ERX * len(clusters[c].relay_nodes)

    # energy consumption for last cluster
    ind = network_architecture.no_of_clusters - 1

    base_station = (network_architecture.base_x, network_architecture.base_y)
    cluster_head = (clusters[ind].nodes[clusters[ind].cluster_head].x, clusters[ind].nodes[clusters[ind].cluster_head].y)

    # distance between cluster head and the base station
    dist = distance_pts(base_station, cluster_head)
    # curr energy of the cluster head
    energy = clusters[ind].nodes[clusters[ind].cluster_head].curr_energy
    if dist >= d0:
        clusters[ind].nodes[clusters[ind].cluster_head].curr_energy = energy - \
                                        ((ETX + EDA) * packet_length + Emp * packet_length * (dist ** 4))
    else:
        clusters[ind].nodes[clusters[ind].cluster_head].curr_energy = energy \
                                            - ((ETX + EDA) * packet_length + Efs * packet_length * (dist ** 2))
    clusters[ind].nodes[clusters[ind].cluster_head].curr_energy = clusters[ind].nodes[clusters[ind].cluster_head].curr_energy \
                                                              - packet_length * ERX * len(clusters[ind].relay_nodes)


# Function to depict energy consumption of Cluster coordinator in single round of operation
def cluster_coordinator_energy_consumption(network_architecture, clusters):
    d0 = math.sqrt(network_architecture.fs_energy / network_architecture.mp_energy)
    ETX = network_architecture.trans_energy
    ERX = network_architecture.rec_energy
    EDA = network_architecture.agg_energy
    Emp = network_architecture.mp_energy
    Efs = network_architecture.fs_energy
    packet_length = network_architecture.pckt_len

    for ind, c in enumerate(clusters):
        # last cluster don't have a cluster coordinator
        if ind == len(clusters)-1:
            break
        no_of_coords = len(c.cluster_coords)
        for i in range(0, no_of_coords-1):
            node1 = clusters[c.cluster_coords[i][0]].nodes[c.cluster_coords[i][1]]
            node2 = clusters[c.cluster_coords[i+1][0]].nodes[c.cluster_coords[i+1][1]]
            dist = distance(node1, node2)
            energy = node1.curr_energy
            if dist >= d0:
                clusters[c.cluster_coords[i][0]].nodes[c.cluster_coords[i][1]].curr_energy = energy - \
                                            ((ETX + EDA) * packet_length + Emp * packet_length * (dist ** 4))
            else:
                clusters[c.cluster_coords[i][0]].nodes[c.cluster_coords[i][1]].curr_energy = energy -\
                                                    ((ETX + EDA) * packet_length + Efs * packet_length * (dist ** 2))
            clusters[c.cluster_coords[i][0]].nodes[c.cluster_coords[i][1]].curr_energy = \
                clusters[c.cluster_coords[i][0]].nodes[c.cluster_coords[i][1]].curr_energy - packet_length * ERX
        # index of last cluster coordinator
        no_of_coords = no_of_coords - 1
        base_station = (network_architecture.base_x, network_architecture.base_y)
        cluster_coord = clusters[c.cluster_coords[no_of_coords][0]].nodes[c.cluster_coords[no_of_coords][1]]
        node = (cluster_coord.x, cluster_coord.y)
        dist = distance_pts(base_station, node)
        energy = cluster_coord.curr_energy
        if dist >= d0:
            clusters[c.cluster_coords[no_of_coords][0]].nodes[c.cluster_coords[no_of_coords][1]].curr_energy = energy - \
                        ((ETX + EDA) * packet_length + Emp * packet_length * (dist ** 4))
        else:
            clusters[c.cluster_coords[no_of_coords][0]].nodes[c.cluster_coords[no_of_coords][1]].curr_energy = energy - \
                                                    ((ETX + EDA) * packet_length + Efs * packet_length * (dist ** 2))
        clusters[c.cluster_coords[no_of_coords][0]].nodes[c.cluster_coords[no_of_coords][1]].curr_energy =\
            clusters[c.cluster_coords[no_of_coords][0]].nodes[c.cluster_coords[no_of_coords][1]].curr_energy - \
            packet_length * ERX


# It gives us the eucledian distance between two points
def distance(node_1, node_2):
    pt_1 = (node_1.x, node_1.y)
    pt_2 = (node_2.x, node_2.y)
    pt_1 = np.array((pt_1[0], pt_1[1]))
    pt_2 = np.array((pt_2[0], pt_2[1]))
    return np.linalg.norm(pt_1-pt_2)


# It gives us the eucledian distance between two points
def distance_pts(pt_1, pt_2):
    pt_1 = np.array((pt_1[0], pt_1[1]))
    pt_2 = np.array((pt_2[0], pt_2[1]))
    return np.linalg.norm(pt_1-pt_2)
