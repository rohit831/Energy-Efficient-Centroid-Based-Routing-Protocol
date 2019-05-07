import random

class Node(object):
    def __init__(self, x, y):
        self.x = x,
        self.y = y


nodes = []

def main():
    for i in range(0, 15):
        nodes.append(Node(random.uniform(0.01, 50)))