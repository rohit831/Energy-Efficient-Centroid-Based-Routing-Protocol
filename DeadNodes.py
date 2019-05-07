from displayResults import *


# Function to check for dead nodes and fix them to end of the list
def check_and_fix_dead_nodes(clusters):
    is_dead=False
    # iterating over all the clusters
    no_of_clusters = len(clusters)
    for c in range(0, no_of_clusters):
        n = clusters[c].available_nodes - 1
        u = n
        flag = False
        while n >= 0:
            #  If it satisfies the criteria for dead node
            if clusters[c].nodes[n].curr_energy < 0.05:
                flag = True
                if clusters[c].nodes[n].node_type != 0:
                    is_dead = True
                    fprint(" DEAD NODE - (Cluster no, node no) - (" + str(c) + "," + str(n) + ")")
                    # print(clusters[c].nodes[n].curr_energy)
                temp = clusters[c].nodes[u]
                clusters[c].nodes[n].dead_node = 1
                clusters[c].nodes[u] = clusters[c].nodes[n]
                clusters[c].nodes[n] = temp
                n -= 1
                u -= 1
            else:
                n -= 1
        if flag:
            clusters[c].available_nodes = u+1
            # clusters[c].nodes=clusters[c].nodes[0:clusters[c].available_nodes].sort(key=lambda t: t.x, reverse=False)\
            #                     + clusters[c].nodes[clusters[c].available_nodes:]
            fprint("Before sorting")
            display_nodes(clusters[c].nodes)
            clusters[c].nodes[0:clusters[c].available_nodes] = \
                sorted(clusters[c].nodes[0:clusters[c].available_nodes], key=lambda t: t.x, reverse=False)
            fprint("After sorting")
            display_nodes(clusters[c].nodes)

    if is_dead:
        # assign all the nodes as normal nodes
        assign_normal_nodes(clusters)
    return is_dead


# Assigning  all the nodes as normal nodes since recalculation needs to be done
def assign_normal_nodes(clusters):
    n = len(clusters)
    for i in range(0, n):
        for ind in range(0, clusters[i].available_nodes):
            clusters[i].nodes[ind].node_type = 0
