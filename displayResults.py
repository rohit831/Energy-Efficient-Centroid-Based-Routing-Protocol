# display all the nodes in all the clusters
def display_energy(clusters):
    for c in clusters:
        for n in c.nodes:
            fprint(n.curr_energy, endchar=" ")
        fprint("")
    fprint("")


#  display all the nodes in a particular cluster
def display_nodes(nodes):
    for n in nodes:
        fprint(n.x, " ")
    fprint("")


# prints the message to the file
def fprint(message, endchar='\n'):
    with open("testlog.txt", 'a') as f:
        print(message, file=f, end=endchar)
