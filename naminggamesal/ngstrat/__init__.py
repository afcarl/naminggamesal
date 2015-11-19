#!/usr/bin/python
import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from importlib import import_module

from .voc_update import get_voc_update

sns.set(rc={'image.cmap': 'Purples_r'})

#####Classe de base
strat_class={
	'naive':'naive.StratNaive',
	'naive_destructive':'naive.StratNaiveDestructive',

	'success_threshold':'success_threshold.StratSuccessThreshold',
	'success_threshold_corrected':'success_threshold.StratSuccessThresholdCorrected',
	'success_threshold_wise':'success_threshold.StratSuccessThresholdWise',
	'success_threshold_wise_max':'success_threshold.StratSuccessThresholdWiseMax',
	'success_threshold_scores':'success_threshold.StratSuccessThresholdScores',

	'mincounts':'mincounts.StratMinCounts',

	'decision_vector':'decision_vector.StratDecisionVector',
	'decision_vector_gainmax':'decision_vector.StratDecisionVectorGainmax',
	'decision_vector_gainsoftmax':'decision_vector.StratDecisionVectorGainSoftmax',
	'decision_vector_gainsoftmax_hearer':'decision_vector.StratDecisionVectorGainSoftmaxHearer',

	'decision_vector_gainsoftmax_hearer_test':'decision_vector.StratDecisionVectorGainSoftmaxHearerTest',

	'last_result':'last_result.StratLastResult',
	'omniscient':'omniscient.StratOmniscient'
}

def Strategy(strat_type='naive', vu_cfg={'vu_type':'imitation'}, **strat_cfg2):
	tempstr = strat_type
	if tempstr == 'mixed':
		tot = sum(strat_cfg2['proba'])
		r = random.random()*tot
		p=strat_cfg2['proba'][0]
		i=0
		while r>p:
			p += strat_cfg2['proba'][i+1]
			i += 1
		return Strategy(**strat_cfg2['cfg_list'][i])
	if tempstr in strat_class.keys():
		tempstr = strat_class[tempstr]
	templist = tempstr.split('.')
	temppath = '.'.join(templist[:-1])
	tempclass = templist[-1]
	_tempmod = import_module('.'+temppath,package=__name__)
	return getattr(_tempmod,tempclass)(vu_cfg=vu_cfg, **strat_cfg2)


class BaseStrategy(object):

	def __init__(self, vu_cfg, **strat_cfg2):
		#for key, value in strat_cfg2.iteritems():
		#	setattr(self, key, value)
		self.voc_update = get_voc_update(**vu_cfg)

	def update_speaker(self, *args, **kwargs):
		return self.voc_update.update_speaker(*args, **kwargs)

	def update_hearer(self, *args, **kwargs):
		return self.voc_update.update_hearer(*args, **kwargs)

	def get_strattype(self):
		return self._strattype

	def visual(self, voc, mem={}, vtype=None, iterr=100, mlist="all", wlist="all"):
		if mlist=="all":
			mlist=range(0,voc._M)
		if wlist=="all":
			wlist=range(0,voc._W)
		if vtype=="pick_mw":
			tempmat=np.matrix(np.zeros((voc._M,voc._W)))
			for i in range(0,iterr):
				lst=self.pick_mw(voc,mem)
				j=lst[0]
				k=lst[1]
				tempmat[j,k]+=1
			plt.figure()
			plt.title("pick_mw")
			plt.gca().invert_yaxis()
			plt.pcolor(np.array(tempmat),vmin=0,vmax=iterr)
		elif vtype=="pick_m":
			tempmat=np.matrix(np.zeros((voc._M,voc._W)))
			for i in range(0,iterr):
				lst=self.pick_mw(voc,mem)
				j=lst[0]
				for k in range(0,voc._W):
					tempmat[j,k]+=1
			plt.figure()
			plt.title("pick_m")
			plt.gca().invert_yaxis()
			plt.pcolor(np.array(tempmat),vmin=0,vmax=iterr)
		elif vtype=="pick_w":
			tempmat=np.matrix(np.zeros((voc._M,voc._W)))
			for m in mlist:
				for i in range(0,iterr):
					lst=self.pick_w(m,voc,mem)
					j=m
					k=lst
					tempmat[j,k]+=1
			plt.figure()
			plt.title("pick_w")
			plt.gca().invert_yaxis()
			plt.pcolor(np.array(tempmat),vmin=0,vmax=iterr)
		elif vtype=="guess_m":
			tempmat=np.matrix(np.zeros((voc._M,voc._W)))
			for w in wlist:
				for i in range(0,iterr):
					lst=self.guess_m(w,voc,mem)
					j=lst
					k=w
					tempmat[j,k]+=1
			plt.figure()
			plt.title("guess_m")
			plt.gca().invert_yaxis()
			plt.pcolor(np.array(tempmat),vmin=0,vmax=iterr)
		elif vtype==None:
			voc.visual()
		elif vtype=="syn":
			voc.visual(vtype="syn")
		elif vtype=="hom":
			voc.visual(vtype="hom")

	def pick_mw(self):
		pass

	def pick_m(self):
		pass

	def pick_w(self):
		pass

	def guess_m(self):
		pass