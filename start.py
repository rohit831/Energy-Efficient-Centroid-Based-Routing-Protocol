import random
import matplotlib
import matplotlib.pyplot as plt
from newNetwork import Network
from newCluster import Cluster
from clusterCoordinator import select_cluster_coordinator
from EnergyConsumption import *
from DeadNodes import check_and_fix_dead_nodes
from displayResults import *

# list of all the clusters
clusters = []
node_architecture = []


# function which uniformly and randomly deploy nodes in a given rectangle area
def deploy_nodes(x, y, length, width, num_of_nodes):
    nodes = []
    for i in range(0, num_of_nodes):
        nodes.append((random.uniform(x+0.01, x + length), random.uniform(y, y + width)))
    node_architecture.append(nodes)


# deploy all the nodes randomly in each cluster
def create_node_architecture(network_architecture):
    width = network_architecture.width/network_architecture.no_of_clusters
    y = 0
    for i in range(0, network_architecture.no_of_clusters):
        deploy_nodes(0, y, network_architecture.length, width, network_architecture.number_of_nodes)


# deploying every cluster based on the given network architecture
def deploy_clusters(network_architecture):
    # assigning width of every cluster
    width = network_architecture.width/network_architecture.no_of_clusters
    y = 0
    for i in range(0, network_architecture.no_of_clusters):
        clusters.append(Cluster(0, y, network_architecture.length, width, network_architecture))
        y = y + width


# function for displaying a particular cluster
def display_cluster(i):
    x_vals, y_vals = zip(*[(float(t.x), float(t.y)) for t in clusters[i].nodes])

    # Colors indicate node type
    # black - Normal node
    # red - Relay node
    # yellow - Cluster Head
    # Green - Cluster coordinator
    colors = ['black', 'red', 'yellow', 'green']
    plt.scatter(x_vals, y_vals, c=[t.node_type for t in clusters[i].nodes],
                cmap=matplotlib.colors.ListedColormap(colors), marker="*", s=35)
    plt.show()


# function to start simulation of single round of energy consumption
def start_round(network_architecture):
    normal_node_energy_consumption(network_architecture, clusters)
    relay_node_energy_consumption(network_architecture, clusters)
    cluster_head_energy_consumption(network_architecture, clusters)
    cluster_coordinator_energy_consumption(network_architecture, clusters)


def main():
    # creating a new network
    network_architecture = Network()
    fprint("Network created")

    # deploying all the clusters
    deploy_clusters(network_architecture)
    fprint("Network deployed")

    # Selecting cluster coordinator for each cluster above it
    select_cluster_coordinator(clusters)
    fprint("Cluster coordinator selected")

    display_energy(clusters)
    # start_round(network_architecture)
    # display_energy(clusters)

    num_rounds = 0
    continue_simulating = True
    # iterate while the condition for simulation remains true
    while continue_simulating and num_rounds <= 1000:
        fprint("Round " + str(num_rounds) + " started.")
        start_round(network_architecture)
        if check_and_fix_dead_nodes(clusters):
            for i in range(0, network_architecture.no_of_clusters):
                if clusters[i].available_nodes == 0:
                    fprint("Cluster " + str(i) + " has 0 available nodes. Stopping further simulation.")
                    continue_simulating = False
                    break
                clusters[i].assign_relay_nodes(network_architecture)
                clusters[i].select_cluster_head()
            select_cluster_coordinator(clusters)
        num_rounds += 1
    display_energy(clusters)
    print("The network lasted for a total of " + str(num_rounds) + " rounds.")


# calling the main function to start the simulation
main()
