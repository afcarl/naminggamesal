#!/usr/bin/python
# -*- coding: latin-1 -*-

#import random
#from ngvoc import *
import os
from copy import deepcopy
import pickle
import random
import matplotlib.pyplot as plt

from .. import ngvoc
from .. import ngstrat_2 as ngstrat

class Agent(object):
	def __init__(self, agent_id, voc_cfg, strat_cfg):
		self._id = agent_id;
		self._vocabulary = ngvoc.Vocabulary(**voc_cfg)
		self._strategy = ngstrat.Strategy(**strat_cfg)

		self._M = self._vocabulary._M
		self._W = self._vocabulary._W

		self.init_memory()
		self.fail = 0
		self.success = 0

	def init_memory(self):
		self._memory=self._strategy.init_memory(self._vocabulary)

	def get_vocabulary_content(self):
		return self._vocabulary.get_content()

	def get_voctype(self):
		return self._vocabulary.get_voctype()

	def get_id(self):
		return self._id

	def __str__(self):
		return str(self._vocabulary)

	def pick_mw(self):
		return self._strategy.pick_mw(self._vocabulary,self._memory)

	def pick_new_m(self):
		return self._strategy.pick_new_m(self._vocabulary,self._memory)

	def guess_m(self,w):
		return self._strategy.guess_m(w,self._vocabulary,self._memory)

	def pick_w(self,m):
		return self._strategy.pick_w(m,self._vocabulary,self._memory)

	def update_hearer(self,ms,w,mh):
		self._strategy.update_hearer(ms,w,mh,self._vocabulary,self._memory)

	def update_speaker(self,ms,w,mh):
		self._strategy.update_speaker(ms,w,mh,self._vocabulary,self._memory)

	def visual(self,vtype=None,iterr=100,mlist="all",wlist="all"):
		self._strategy.visual(self._vocabulary,mem=self._memory,vtype=vtype,iterr=iterr,mlist=mlist,wlist=wlist)







