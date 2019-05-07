class Network(object):
    def __init__(self, length=int(100), width=int(100), base_x=int(110), base_y=int(110),
                 number_of_nodes=int(20), pckt_len=int(4000), init_energy=float(0.5), trans_energy=float(50*0.000000001),
                 rec_energy=float(50*0.000000001),
                 fs_energy=float(10*0.000000000001), mp_energy=float(0.0013*0.000000000001), agg_energy=float(5*0.000000001),
                 no_of_clusters=int(2), max_distance=int(20), threshold=int(20)):
        self.length = length    # length of the network
        self.width = width      # width of the network
        self.base_x = base_x    # the x coordinate of the base station
        self.base_y = base_y    # the y coordinate of the base station
        self.number_of_nodes = number_of_nodes     # number of nodes in each cluster initially
        self.pckt_len = pckt_len   # length of the packet
        self.init_energy = init_energy   # initial energy
        self.trans_energy = trans_energy  # transmission energy
        self.rec_energy = rec_energy   # reception energy
        self.fs_energy = fs_energy  # free space energy
        self.mp_energy = mp_energy  # multipath energy
        self.agg_energy = agg_energy  # aggregation energy
        self.no_of_clusters = no_of_clusters  # no of clusters
        self.max_distance = max_distance  # maximum distance of communication
        self.threshold = threshold

