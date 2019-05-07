import numpy as np


def select_cluster_coordinator(clusters):
    n = len(clusters)
    for i in range(0, n-1):
        for j in range(i+1, n):
            #  assign cluster coordinator for CH of ith cluster in jth cluster
            assign_cluster_coordinator(clusters[i].nodes[clusters[i].cluster_head], i, clusters, j)


def assign_cluster_coordinator(head, head_cluster_no, clusters, cluster_no):
    min_val = 99999
    index = -1
    for ind in range(0, clusters[cluster_no].available_nodes):
        if distance(head, clusters[cluster_no].nodes[ind])/clusters[cluster_no].nodes[ind].curr_energy <= min_val:
            min_val = distance(head, clusters[cluster_no].nodes[ind])/clusters[cluster_no].nodes[ind].curr_energy
            index = ind

    # assigning that node as cluster coordinator
    clusters[cluster_no].nodes[index].node_type = 3
    clusters[head_cluster_no].cluster_coords.append((cluster_no, index))


# It gives us the eucledian distance between two points
def distance(node_1, node_2):
    pt_1 = (node_1.x, node_1.y)
    pt_2 = (node_2.x, node_2.y)
    pt_1 = np.array((pt_1[0], pt_1[1]))
    pt_2 = np.array((pt_2[0], pt_2[1]))
    return np.linalg.norm(pt_1-pt_2)