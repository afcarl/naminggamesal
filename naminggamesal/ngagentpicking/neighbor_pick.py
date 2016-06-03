#!/usr/bin/python

from .random_pick import RandomPick
import random
import numpy as np
import networkx as nx

##########

class NeighborPick(RandomPick):
	def pick_hearer(self, speaker, pop):
		return pop._topology.get_neighbor(speaker,pop=pop)