#!/usr/bin/python
import copy
import numpy as np
import math
import random
import networkx as nx

import additional.custom_func as custom_func
import additional.custom_graph as custom_graph
from .ngpop import Population

def pop_ize(func):
	def out_func(pop,**kwargs):
		tempNlist=[]
		agentlist=pop._agentlist
		for i in range(0,len(agentlist)):
			tempNlist.append(func(agentlist[i]))
			mean=np.mean(tempNlist)
			std=np.std(tempNlist)
		return [mean,std,tempNlist]
	out_func.__name__=func.__name__+"_moyen"
	return out_func



############################	LEVEL AGENT ############################

#### 	INPUT:		agent , **progress_info
####	OUTPUT:		[mean,std,(tempNlist)]

#	FUNC_BIS=pop_ize(FUNC)
#graphconfig={}
#	custom_FUNC=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)

#########Nlink##########

def Nlink(agent,**kwargs):
	return np.sum(agent.get_vocabulary_content())

def Nlink_max(pop):
	return pop._M * pop._W

def Nlink_min(pop):
	return 0


FUNC=Nlink
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":Nlink_min}#,"ymax":Nlink_max}
custom_Nlink =custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)


#########success_rate##########

def success_rate(agent,**kwargs):
	if agent.success+agent.fail!=0:
		return agent.success/float(agent.success+agent.fail)
	else:
		return 0

def success_rate_max(pop):
	return 1

def success_rate_min(pop):
	return 0

FUNC=success_rate
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":success_rate_min,"ymax":success_rate_max}
custom_success_rate=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)

#########Ncat_percept##########

def Ncat_percept(agent,**kwargs):
	return len(agent._vocabulary._content_coding)

def Ncat_percept_max(pop):
	return 1

def Ncat_percept_min(pop):
	return 0

FUNC=Ncat_percept
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":Ncat_percept_min}#,"ymax":Ncat_percept_max}
custom_Ncat_percept=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)

#########Ncat_semantic##########

def Ncat_semantic(agent,**kwargs):
	n = 0
	data = None
	for iv in sorted(agent._vocabulary._content_coding):
		if data != iv.data:
			data = iv.data
			n += 1
	return n

def Ncat_semantic_max(pop):
	return 1

def Ncat_semantic_min(pop):
	return 0

FUNC=Ncat_semantic
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":Ncat_semantic_min}#,"ymax":Ncat_semantic_max}
custom_Ncat_semantic=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)


#########N_words##########

def N_words(agent,**kwargs):
	return len(agent._vocabulary._content_decoding.keys())

def N_words_max(pop):
	return 1

def N_words_min(pop):
	return 0

FUNC=N_words
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":N_words_min}#,"ymax":N_words_max}
custom_N_words=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)


#########cat_synonymy##########

def cat_synonymy(agent,**kwargs):
	n = 0
	w = 0
	for iv in sorted(agent._vocabulary._content_coding):
		w += len(iv.data)
		n += 1
	return w / float(n)

def cat_synonymy_max(pop):
	return 1

def cat_synonymy_min(pop):
	return 0

FUNC=cat_synonymy
FUNC_BIS=pop_ize(FUNC)
graphconfig={"ymin":cat_synonymy_min}#,"ymax":cat_synonymy_max}
custom_cat_synonymy=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)


#########entropy##########

def tempentropy(MM,WW):
	a=0
	for i in range(int(WW-MM+1),int(WW+1)):
		a+=np.log2(i)
	return a

def entropy(agent,**kwargs):
	m=len(agent._vocabulary.get_known_meanings())
	return tempentropy(agent._M-m,agent._W-m)

def entropy_max(pop):
	return tempentropy(pop._M,pop._W)

def entropy_min(pop):
	return 0

FUNC=entropy
FUNC_BIS=pop_ize(FUNC)
entropy_moyen=pop_ize(FUNC)
graphconfig={"ymin":entropy_min,"ymax":entropy_max}
custom_entropy=custom_func.CustomFunc(FUNC_BIS,"agent",**graphconfig)

#########entropy_moyen_norm##########


def entropy_moyen_norm(pop,**kwargs):
	return 1.-(entropy_moyen(pop)[0]/entropy_max(pop))

def entropy_moyen_norm_max(pop):
	return 1

def entropy_moyen_norm_min(pop):
	return 0

FUNC=entropy_moyen_norm
graphconfig={"ymin":entropy_moyen_norm_min,"ymax":entropy_moyen_norm_max}
custom_entropy_moyen_norm=custom_func.CustomFunc(FUNC,"population",**graphconfig)


############################	LEVEL POPULATION ############################

#### 	INPUT:		pop, **progress_info
####	OUTPUT:		value

#graphconfig={}
#	custom_FUNC=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########Nlinksurs##########

def Nlinksurs(pop,**kwargs):
	tempmat=np.matrix(np.ones((pop._M,pop._W)))
	for agent in pop._agentlist:
		tempmat=np.multiply(tempmat,agent._vocabulary.get_content())
	return np.sum(tempmat)

def Nlinksurs_max(pop):
	return pop._M

def Nlinksurs_min(pop):
	return 0

FUNC=Nlinksurs
graphconfig={"ymin":Nlinksurs_min,"ymax":Nlinksurs_max}
custom_Nlinksurs=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########Nlinksurs_couples##########

def Nlinksurs_couples(pop,**kwargs):
	tempvalues = []
	for j in range(100):
		agent1_id=pop.pick_speaker()
		agent2_id=pop.pick_hearer(agent1_id)
		agent1=pop._agentlist[pop.get_index_from_id(agent1_id)]
		agent2=pop._agentlist[pop.get_index_from_id(agent2_id)]
		tempm = np.linalg.matrix_rank(np.multiply(agent1.get_vocabulary_content(),agent2.get_vocabulary_content()))
		tempvalues.append(tempm)
	return np.mean(tempvalues)

def Nlinksurs_couples_max(pop):
	return pop._M

def Nlinksurs_couples_min(pop):
	return 0

FUNC=Nlinksurs_couples
graphconfig={"ymin":Nlinksurs_couples_min,"ymax":Nlinksurs_couples_max}
custom_Nlinksurs_couples=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########entropypop##########

def entropypop(pop,**kwargs):
	m=Nlinksurs(pop)
	return tempentropy(pop._M-m,pop._W-m)

def entropypop_max(pop):
	return tempentropy(pop._M,pop._W)

def entropypop_min(pop):
	return 0

FUNC=entropypop
graphconfig={"ymin":entropypop_min,"ymax":entropypop_max}
custom_entropypop=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########entropypopnorm##########


def entropypop_norm(pop,**kwargs):
	return 1-(entropypop(pop)/entropypop_max(pop))

def entropypop_norm_max(pop):
	return 1

def entropypop_norm_min(pop):
	return 0

FUNC=entropypop_norm
graphconfig={"ymin":entropypop_norm_min,"ymax":entropypop_norm_max}
custom_entropypop_norm=custom_func.CustomFunc(FUNC,"population",**graphconfig)


#########entropycouplesold##########

def entropycouples_old(pop,**kwargs):
	tempvalues=[]
	for j in range(100):
		agent1_id=pop.pick_speaker()
		agent2_id=pop.pick_hearer(agent1_id)
		agent1=pop._agentlist[pop.get_index_from_id(agent1_id)]
		agent2=pop._agentlist[pop.get_index_from_id(agent2_id)]
		if pop._strat_cfg["strat_type"][-5:]=="_real":
			voc1=agent1._vocabulary.get_content()
			voc2=agent2._vocabulary.get_content()
			tempm=0
			for m in range(pop._M):
				for w in range(pop._W):
					test1= voc1[m,w] and voc2[m,w]
					test1=test1 and agent1._vocabulary.get_known_meanings(w)==[m]
					test1=test1 and agent2._vocabulary.get_known_meanings(w)==[m]
					test1=test1 and agent1._vocabulary.get_known_words(m)==[w]
					test1=test1 and agent2._vocabulary.get_known_words(m)==[w]
					if test1:
						tempm+=1
		else:
			tempmat=np.multiply(agent1._vocabulary.get_content(),agent2._vocabulary.get_content())
			tempm=np.sum(tempmat)
		tempvalues.append(tempentropy(pop._M-tempm,pop._W-tempm))
	return np.mean(tempvalues)

def entropycouples_old_max(pop):
	return tempentropy(pop._M,pop._W)

def entropycouples_old_min(pop):
	return 0

FUNC=entropycouples_old
graphconfig={"ymin":entropycouples_old_min,"ymax":entropycouples_old_max}
custom_entropycouples_old=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########entropycouplesoldnorm##########


def entropycouples_old_norm(pop,**kwargs):
	return 1-(entropycouples(pop)/entropycouples_max(pop))

def entropycouples_old_norm_max(pop):
	return 1

def entropycouples_old_norm_min(pop):
	return 0

FUNC=entropycouples_old_norm
graphconfig={"ymin":entropycouples_old_norm_min,"ymax":entropycouples_old_norm_max}
custom_entropycouples_old_norm=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########N_words_pop##########


def N_words_pop(pop,**kwargs):
	words = set()
	for ag in pop._agentlist:
		for w in ag._vocabulary._content_decoding.keys():
			words.add(w)
	return len(words)

def N_words_pop_max(pop):
	return 1

def N_words_pop_min(pop):
	return 0

FUNC=N_words_pop
graphconfig={"ymin":N_words_pop_min}#,"ymax":entropycouples_old_norm_max}
custom_N_words_pop=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########distance_used##########


def distance_used(pop,**kwargs):
	return abs(pop._lastgameinfo[-1][0]-pop._lastgameinfo[-1][1])

def distance_used_max(pop):
	return 1

def distance_used_min(pop):
	return 0

FUNC=distance_used
graphconfig={"ymin":distance_used_min}#,"ymax":entropycouples_old_norm_max}
custom_distance_used=custom_func.CustomFunc(FUNC,"population",**graphconfig)



#########actual_successrate##########


def actual_successrate(pop,**kwargs):
	s = 0
	f = 0
	for info in pop._past:
		if info[3]:
			s += 1
		else:
			f += 1
	print s
	print f
	if not s:
		return 0
	else:
		return s/float(s+f)

def actual_successrate_max(pop):
	return 1

def actual_successrate_min(pop):
	return 0

FUNC=actual_successrate
graphconfig={"ymin":actual_successrate_min}#,"ymax":entropycouples_old_norm_max}
custom_actual_successrate=custom_func.CustomFunc(FUNC,"population",**graphconfig)


#########entropycouples##########

def entropycouples(pop,**kwargs):
	tempvalues=[]
	for j in range(100):
		agent1_id=pop.pick_speaker()
		agent2_id=pop.pick_hearer(agent1_id)
		agent1=pop._agentlist[pop.get_index_from_id(agent1_id)]
		agent2=pop._agentlist[pop.get_index_from_id(agent2_id)]
		tempm = np.linalg.matrix_rank(np.multiply(agent1.get_vocabulary_content(),agent2.get_vocabulary_content()))
		tempvalues.append(tempentropy(pop._M-tempm,pop._W-tempm))
	return np.mean(tempvalues)

def entropycouples_max(pop):
	return tempentropy(pop._M,pop._W)

def entropycouples_min(pop):
	return 0

FUNC=entropycouples
graphconfig={"ymin":entropycouples_min,"ymax":entropycouples_max}
custom_entropycouples=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########entropycouplesnorm##########


def entropycouples_norm(pop,**kwargs):
	return 1-(entropycouples(pop)/entropycouples_max(pop))

def entropycouples_norm_max(pop):
	return 1

def entropycouples_norm_min(pop):
	return 0

FUNC=entropycouples_norm
graphconfig={"ymin":entropycouples_norm_min,"ymax":entropycouples_norm_max}
custom_entropycouples_norm=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########srtheo##########

def srtheo(pop,**kwargs):
	fail=0
	succ=0
	for i in range(100):
		agent1_id = pop.pick_speaker()
		agent2_id = pop.pick_hearer(agent1_id)
		agent1 = pop._agentlist[pop.get_index_from_id(agent1_id)]
		agent2 = pop._agentlist[pop.get_index_from_id(agent2_id)]
		ms = agent1._vocabulary.get_random_m()
		w = agent1._vocabulary.get_random_known_w(m=ms)
		mh = agent2._vocabulary.get_random_known_m(w=w)
		agent1._vocabulary.del_cache()
		agent2._vocabulary.del_cache()
		if agent2.eval_success(ms=ms, w=w, mh=mh):
			succ += 1
		else:
			fail += 1
	return succ/float(succ+fail)

def srtheo_max(pop):
	return 1

def srtheo_min(pop):
	return 0

FUNC=srtheo
graphconfig={"ymin":srtheo_min,"ymax":srtheo_max}
custom_srtheo=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########srtheo_cat##########
from .ngstrat.naive import StratNaiveCategoryPlosOne
strat_srtheo_cat = StratNaiveCategoryPlosOne()
def srtheo_cat(pop,**kwargs):
	fail=0
	succ=0
	for i in range(100):
		agent1_id = pop.pick_speaker()
		agent2_id = pop.pick_hearer(agent1_id)
		agent1 = pop._agentlist[pop.get_index_from_id(agent1_id)]
		agent2 = pop._agentlist[pop.get_index_from_id(agent2_id)]
		v1 = agent1._vocabulary
		v2 = agent2._vocabulary
		ct = agent1._sensoryapparatus.context_gen(env=pop.env, diff=True, size=2).next()
		#ms = random.choice(ct)
		ms = strat_srtheo_cat.pick_m(v1,agent1._memory,ct)
		w = strat_srtheo_cat.pick_w(ms,v1,agent1._memory,ct)
		mh = strat_srtheo_cat.guess_m(w,v2,agent2._memory,ct)


		#ct_maxinf = max([-1] + [m for m in ct if m < ms])
		#ct_minsup = min([2] + [m for m in ct if m > ms])
		#iv = v1.get_category(ms)
		#if iv.begin < ct_maxinf or iv.end >= ct_minsup:
		#	w = v1.get_new_unknown_w()
		#else:
		#	w = v1.get_random_known_w(m=ms)
#
#		#ml = []
#		#for m in ct:
#		#	if w in v2.get_known_words(m):
#		#		ml.append(m)
#		#if not ml:
#		#	mh = None
#		#else:
#		#	mh = random.choice(ml)
		##print ct, ms, iv, ct_maxinf, ct_minsup, w, v2.get_known_words(ms), ml, mh
		if agent2.eval_success(ms=ms, w=w, mh=mh,context=ct):
			succ += 1
		else:
			fail += 1
		v1.del_cache()
		v2.del_cache()
	return succ/float(succ+fail)

def srtheo_cat_max(pop):
	return 1

def srtheo_cat_min(pop):
	return 0

FUNC=srtheo_cat
graphconfig={"ymin":srtheo_cat_min,"ymax":srtheo_cat_max}
custom_srtheo_cat=custom_func.CustomFunc(FUNC,"population",**graphconfig)

###############""srtheo as used in epirob08 paper#############
def srtheo2(pop,**kwargs):
	C = np.zeros((pop._W,pop._M))
	best_scores = np.zeros((pop._M,pop._size))
	for ag in range(len(pop._agentlist)):
		for m in range(pop._M):
			best_scores[m,ag] = np.amax(pop._agentlist[ag]._vocabulary._content[m,:])
	n_meanings_used = 0
	for a in range(pop._size):
		for meaning in range(pop._M):
			score = best_scores[meaning,a]
			if score > 0:
				n_meanings_used += 1
				words = pop._agentlist[a]._vocabulary.get_known_words(m=meaning,option='max')
				if words:
					word = words[0]
					C[word,meaning] += 1
	C = C/float(pop._size)
	n_meanings_used = n_meanings_used/float(pop._size)

	D = np.zeros((pop._W,pop._M))
	best_scores = np.zeros((pop._W,pop._size))
	for ag in range(len(pop._agentlist)):
		for w in range(pop._W):
			best_scores[w,ag] = np.amax(pop._agentlist[ag]._vocabulary._content[:,w])
	n_words_used = 0
	for a in range(pop._size):
		for word in range(pop._W):
			score = best_scores[word,a]
			if score > 0:
				n_words_used += 1
				meanings = pop._agentlist[a]._vocabulary.get_known_meanings(w=word,option='max')
				if meanings:
					meaning = meanings[0]
					D[word,meaning] += 1.
	D = D/float(pop._size)
	n_words_used = n_words_used/float(pop._size)

	return sum(sum(np.multiply(C,D)))/float(pop._M)


def srtheo2_max(pop):
	return 1

def srtheo2_min(pop):
	return 0

FUNC=srtheo2
graphconfig={"ymin":srtheo2_min,"ymax":srtheo2_max}
custom_srtheo2=custom_func.CustomFunc(FUNC,"population",**graphconfig)

###############""srtheo as used in epirob08 paper#############
def srtheo3(pop,**kwargs):
	C = np.zeros((pop._W,pop._M))
	best_scores = np.zeros((pop._M,pop._size))
	for ag in range(len(pop._agentlist)):
		for m in range(pop._M):
			best_scores[m,ag] = np.amax(pop._agentlist[ag]._vocabulary._content[m,:])
	n_meanings_used = 0
	for a in range(pop._size):
		for meaning in range(pop._M):
			score = best_scores[meaning,a]
			if score > 0:
				n_meanings_used += 1
				words = pop._agentlist[a]._vocabulary.get_known_words(m=meaning,option='max')
				#word = word[0]
				#C[word,meaning] += 1
				if words:
					for word in words:
						C[word,meaning] += 1./len(words)
	C = C/float(pop._size)
	n_meanings_used = n_meanings_used/float(pop._size)

	D = np.zeros((pop._W,pop._M))
	best_scores = np.zeros((pop._W,pop._size))
	for ag in range(len(pop._agentlist)):
		for w in range(pop._W):
			best_scores[w,ag] = np.amax(pop._agentlist[ag]._vocabulary._content[:,w])
	n_words_used = 0
	for a in range(pop._size):
		for word in range(pop._W):
			score = best_scores[word,a]
			if score > 0:
				n_words_used += 1
				meanings = pop._agentlist[a]._vocabulary.get_known_meanings(w=word,option='max')
				#meaning = meaning[0]
				#D[word,meaning] += 1
				if meanings:
					for meaning in meanings:
						D[word,meaning] += 1./len(meanings)
	D = D/float(pop._size)
	n_words_used = n_words_used/float(pop._size)

	return sum(sum(np.multiply(C,D)))/float(pop._M)


def srtheo3_max(pop):
	return 1

def srtheo3_min(pop):
	return 0

FUNC=srtheo3
graphconfig={"ymin":srtheo3_min,"ymax":srtheo3_max}
custom_srtheo3=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########entropydistrib##########

def entropydistrib(pop,**kwargs):
	tempmat=np.matrix(np.zeros((pop._M,pop._W)))
	for ag in pop._agentlist:
		tempmat=tempmat+ag._vocabulary.get_content()
	ans=0
	for m in range(pop._M):
		temp=pop._size
		for w in range(pop._W):
			temp=temp-tempmat[m,w]
		for w in range(pop._W):
			tempmat[m,w]=(tempmat[m,w]+temp/pop._W)/pop._size
			if tempmat[m,w]!=0:
				ans-=tempmat[m,w]*np.log2(tempmat[m,w])
	return ans

def entropydistrib_max(pop):
	return pop._M*np.log2(pop._W)

def entropydistrib_min(pop):
	return 0

FUNC=entropydistrib
graphconfig={"ymin":entropydistrib_min,"ymax":entropydistrib_max}
custom_entropydistrib=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########overlap##########

def overlap(pop,**kwargs):
	n_r = min((pop._size**2),100)
	overlap_val = 0
	for i in range(n_r):
		agent1_id = pop.pick_speaker()
		agent2_id = pop.pick_hearer(agent1_id)
		ag1 = pop._agentlist[pop.get_index_from_id(agent1_id)]
		ag2 = pop._agentlist[pop.get_index_from_id(agent2_id)]


		ivt1 = []
		for iv in sorted(ag1._vocabulary._content_coding):
			ivt1.append(iv.begin)
		ivt1.append(1.)
		ivt2 = []
		for iv in sorted(ag2._vocabulary._content_coding):
			ivt2.append(iv.begin)
		ivt2.append(1.)
		ivt1.sort()
		ivt2.sort()
		ivto = sorted(ivt1 + ivt2)
		ovsum1 =  sum([(ivt1[k+1]-ivt1[k])**2 for k in range(len(ivt1)-1)])
		ovsum2 =  sum([(ivt2[k+1]-ivt2[k])**2 for k in range(len(ivt2)-1)])
		ovsumo =  sum([(ivto[k+1]-ivto[k])**2 for k in range(len(ivto)-1)])

#		ivt1 = copy.deepcopy(ag1._vocabulary._content_coding)
#		ivt2 = copy.deepcopy(ag2._vocabulary._content_coding)
#		ivto = copy.deepcopy(ag1._vocabulary._content_coding)
#		ivto.union(ivt2)
#		ivto.split_overlaps()
#		ivto.merge_overlaps()
#		ovsum1 =  sum([(iv.end - iv.begin)**2 for iv in ivt1])
#		ovsum2 =  sum([(iv.end - iv.begin)**2 for iv in ivt2])
#		ovsumo =  sum([(iv.end - iv.begin)**2 for iv in ivto])
		overlap_val += (2*ovsumo/float(ovsum1 + ovsum2))
	return overlap_val / float(n_r)

def overlap_max(pop):
	return 1

def overlap_min(pop):
	return 0

FUNC=overlap
graphconfig={"ymin":overlap_min,"ymax":overlap_max}
custom_overlap=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########overlap_semantic##########

def overlap_semantic(pop,**kwargs):
	n_r = min((pop._size**2)/2,100)
	overlap_val = 0
	for i in range(n_r):
		agent1_id = pop.pick_speaker()
		agent2_id = pop.pick_hearer(agent1_id)
		ag1 = pop._agentlist[pop.get_index_from_id(agent1_id)]
		ag2 = pop._agentlist[pop.get_index_from_id(agent2_id)]
		ivt1 = []
		data = None
		for iv in sorted(ag1._vocabulary._content_coding):
			if iv.data != data:
				ivt1.append(iv.begin)
		ivt1.append(1.)
		ivt2 = []
		data = None
		for iv in sorted(ag2._vocabulary._content_coding):
			if iv.data != data:
				ivt2.append(iv.begin)
		ivt2.append(1.)
		ivto = sorted(ivt1 + ivt2)
		ovsum1 =  sum([(ivt1[k+1]-ivt1[k])**2 for k in range(len(ivt1)-1)])
		ovsum2 =  sum([(ivt2[k+1]-ivt2[k])**2 for k in range(len(ivt2)-1)])
		ovsumo =  sum([(ivto[k+1]-ivto[k])**2 for k in range(len(ivto)-1)])
		overlap_val += (2*ovsumo/float(ovsum1 + ovsum2))
	return overlap_val / float(n_r)

def overlap_semantic_max(pop):
	return 1

def overlap_semantic_min(pop):
	return 0

FUNC=overlap_semantic
graphconfig={"ymin":overlap_semantic_min,"ymax":overlap_semantic_max}
custom_overlap_semantic=custom_func.CustomFunc(FUNC,"population",**graphconfig)

#########weight_over_degree##########

def weight_over_degree(pop,**kwargs):
	G = build_nx_graph(pop._agentlist)
	values = []
	for ag in pop._agentlist:
		weight = 0
		for ed in G.edges(ag._id):
			weight += ed['weight']
		if weight != 0 :
			values.append(weight/G.degree(ag._id))
		else:
			values.append(0)
	return mean(values)

def weight_over_degree_max(pop):
	return 1

def weight_over_degree_min(pop):
	return 0


FUNC=weight_over_degree
graphconfig={"ymin":weight_over_degree_min,"ymax":weight_over_degree_max}
custom_weight_over_degree =custom_func.CustomFunc(FUNC,"population",**graphconfig)

############################	LEVEL TIME ############################

#### 	INPUT:		expe, **progress_info
####	OUTPUT:		vector (size same as _T)

#graphconfig={}
#	custom_FUNC=custom_func.CustomFunc(FUNC,"experiment",**graphconfig)

#########interactions_per_agent##########

def interactions_per_agent(exp,**kwargs):
	return list(np.array(exp._T)*2./exp._poplist[0]._size)

def interactions_per_agent_max(exp):
	return max(exp._T)*2./exp._poplist[0]._size

def interactions_per_agent_min(exp):
	return min(exp._T)*2./exp._poplist[0]._size


FUNC=interactions_per_agent
graphconfig={"ymin":interactions_per_agent_min,"ymax":interactions_per_agent_max}
custom_interactions_per_agent =custom_func.CustomFunc(FUNC,"time",**graphconfig)


############################	LEVEL EXPE ############################

#### 	INPUT:		expe, **progress_info
####	OUTPUT:		value

#graphconfig={}
#	custom_FUNC=custom_func.CustomFunc(FUNC,"experiment",**graphconfig)




################################################################




################  AUTRES    ####################################

def m_limit_theorique(M,W):
	return (-((M+W-1.)/2.)+math.sqrt((M+W-1.)**2/4.+2.*M*W))/2.

def decvec_from_MW(M,W):
	decvec=[]
	m=m_limit_theorique(M,W)
	for i in range(0,M+1):
		if i<=m:
			decvec.append(1)
		else:
			decvec.append(0)
	return decvec



def decvectest_from_MW(M,W):
	decvec=[]
	m0=0
	for i in range(0,M+1):
		dm=i-m0
		pp=(M-i)/float(M)*(W-i)/float(W)
		pm=i/float(M)*(i-1.)/float(W)
		print pp
		print pm
		print " "
		if pm<=pp:
			decvec.append(1)
		else:
			decvec.append(0)
	return decvec

def decvec2_from_MW(M,W):
	decvec=[]
	m0=0
	for i in range(0,M+1):
		dm=i-m0
		pp=(M-i)/float(M)*(W-i)/float(W-dm)
		pm=m0/float(M)*(m0-1.)/float(W-dm)
		print pp
		print pm
		print " "
		if pm<=pp:
			decvec.append(1)
			m0+=1
		else:
			decvec.append(0)
	return decvec


def decvec3_from_MW(M,W):
	decvec=[]
	for i in range(0,M):
		pp=(M-i)/float(M)*(W-i)/float(W)
		pm=i/float(M)*(i-1.)/float(W)
		Gp=np.log2(W-i)
		Gm=np.log2(W-i+1)
		if pm*Gm<=pp*Gp:
			decvec.append(1)
		else:
			decvec.append(0)
	decvec.append(0)
	return decvec


def decvec3_softmax_from_MW(M,W,Temp):
	decvec=[]
	for i in range(0,M):
		pp=(M-i)/float(M)*(W-i)/float(W)
		pm=i/float(M)*(i-1.)/float(W)
		Gp=np.log2(W-i)
		Gm=np.log2(W-i+1)
		P1 = np.exp(pp*Gp/Temp)
		P2 = np.exp(-pm*Gm/Temp)
		decvec.append(P1/(P1+P2))
	decvec.append(0)
	return decvec


def decvec4_softmax_from_MW(M,W,Temp):
	decvec=[1.]
	for i in range(1,M):
		pp=(M-i)/float(M)*(W-i)/float(W)
		pm=i/float(M)*(i-1.)/float(W)
		Gp=np.log2(W-i)
		Gm=np.log2(W-i+1)
		P1 = np.exp(pp*Gp/Temp)
		P2 = np.exp(pm*Gm/Temp)
		p=P1/(P1+P2)
		if np.isnan(p):
			if pm*Gm<=pp*Gp:
				p=1.
			else:
				p=0.
		decvec.append(p)
	decvec.append(0.)
	return decvec

def decvec5_softmax_from_MW(M,W,Temp):
	decvec=[1.]
	for i in range(1,M):
		pp=(W-i)/float(W)
		pm=(i*(i-1)+(M-i)*(i-1))/float(M*W)
		Gp=np.log2(W-i)
		Gm=np.log2(W-i+1)
		P1 = np.exp(pp*Gp/Temp)
		P2 = np.exp(pm*Gm/Temp)
		p=P2/(P1+P2)
		if np.isnan(p):
			if pm*Gm>=pp*Gp:
				p=1.
			else:
				p=0.
		decvec.append(p)
	decvec.append(0.)
	return decvec

def decvectest_softmax_from_MW(M,W,Temp):
	decvec=[1.]
	for i in range(1,M):
		pp=(W-i)/float(W)
		pm=(i*(i-1)+(M-i)*(i-1))/float(M*W)
		Gp=np.log2(W-i)
		Gm=-np.log2(W-i+1)
		P1 = np.exp(pp*Gp/Temp)
		P2 = np.exp(pm*Gm/Temp)
		p=P2/(P1+P2)
		if np.isnan(p):
			if pm*Gm>=pp*Gp:
				p=1.
			else:
				p=0.
		decvec.append(p)
	decvec.append(0.)
	return decvec

def decvec_full_explo(M,W):
	decvec = [1.]
	for i in range(1,M):
		decvec.append(1.)
	decvec.append(0.)


def decvec_full_teach(M,W):
	decvec = [1.]
	for i in range(1,M):
		decvec.append(0.)
	decvec.append(0.)

############################################################################
#NETWORKX TOOLS

def build_nx_graph(agent_list):
	G = nx.Graph()
	for ag in agent_list:
		tempm = np.sum(ag._vocabulary.get_content())
		G.add_node(ag._id,size=1.-(tempentropy(ag._M-tempm, ag._W-tempm)/tempentropy(ag._M, ag._W)))
	list_length = len(agent_list)
	for i in range(list_length):
		agent1 = agent_list[i]
		for j in range(i+1,list_length):
			agent2 = agent_list[j]
			tempmat = np.multiply(agent1._vocabulary.get_content(), agent2._vocabulary.get_content())
			tempm = np.sum(tempmat)
			weight = 1.-(tempentropy(agent1._M-tempm, agent1._W-tempm)/tempentropy(agent1._M, agent1._W))
			if weight != 0:
				G.add_edge(agent1._id,agent2._id,weight=weight)
	return G

def degree_distrib(pop,**kwargs):
	G = build_nx_graph(pop._agentlist)
	return custom_graph.CustomGraph(nx.degree_histogram(G))

def edgevalue_distrib(pop,**kwargs):
	G = build_nx_graph(pop._agentlist)
	dict_XY = {}
	for ed in G.edges:
		weight = ed['weight']
		if weight in dict_XY.keys():
			dict_XY[weight] += 1
		else:
			dict_XY[weight] = 1
	for key, value in dict_XY.items():
		X.append(key)
		Y.append(value)
	return custom_graph.CustomGraph(X=X,Y=Y)




