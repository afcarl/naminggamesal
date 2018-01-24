from . import MemoryPolicy
import numpy as np
import copy
from ...ngmeth_utils.srtheo_utils import srtheo_voc

class SuccessMatrixMP(MemoryPolicy):

	def init_memory(self,mem,voc):
		assert not 'success_matrix' in list(mem.keys())
		mem['success_matrix'] = np.zeros((self.nb_boxes,self.nb_boxes,2))

	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context):
		x,y = self.get_coords(context)
		if bool_succ:
			mem['success_matrix'][x,y,0] += 1
		else:
			mem['success_matrix'][x,y,1] += 1


class PastInterMP(MemoryPolicy):

	def init_memory(self,mem,voc):
		assert not 'past_interactions' in list(mem.keys())
		mem['past_interactions'] = []

	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context):
		past_int = mem['past_interactions']
		d = abs(context[0]-context[1])
		c = (context[0]+context[1])/2.
		mem['past_interactions'] = past_int[-self.past_window:]+[(d, c, bool_succ)]



class LastResultMP(MemoryPolicy):

	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context=[]):
		if bool_succ:
			mem["result"]=1
		else:
			mem["result"]=0

	def init_memory(self,mem,voc):

		assert not 'result' in list(mem.keys())
		mem["result"]=1

class ProbaSuccessIncrease(MemoryPolicy):#!! only a cache

	#def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context=[]):
	#	m_rm_list = list(  set([ms]) | set(voc.get_known_meanings(w=w)) ) not removing here because voc is already updated, hence lists of ms and ws to be removed are not always known

	def init_memory(self,mem,voc):
		assert not 'proba_of_success_increase' in list(mem.keys())
		mem['proba_of_success_increase'] = dict()

class SuccessCountPerMMP(MemoryPolicy):


	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context=[]):
		if role=='speaker':
			m1=ms
		else:
			m1=ms#mh justification: getting information from the other's vocabulary for the hearer
		if bool_succ:
			try:
				mem["success_m"][m1] += 1
			except KeyError:
				mem["success_m"][m1] = 1
		else:
			try:
				mem["fail_m"][m1] += 1
			except KeyError:
				mem["fail_m"][m1] = 1

	def init_memory(self,mem,voc):
		assert not 'success_m' in list(mem.keys())
		assert not 'fail_m' in list(mem.keys())
		if voc is not None and hasattr(voc,'_content'):
			mem["success_m"] = np.zeros(voc.get_M())#[0]*voc._M
			mem["fail_m"] = np.zeros(voc.get_M())#[0]*voc._M
		else:
			mem["success_m"] = dict()
			mem["fail_m"] = dict()



class TimeDecreaseSuccessCountPerMMP(SuccessCountPerMMP):

	def __init__(self,mem_type,time_scale=100):
		MemoryPolicy.__init__(self,mem_type=mem_type)
		self.time_scale = time_scale
		if self.time_scale == 0:
			self.factor = 0.
		else:
			self.factor = np.exp(-1./self.time_scale)

	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context=[]):
		if role=='speaker':
			m1=ms
		else:
			m1=ms#mh justification: getting information from the other's vocabulary for the hearer
		if m1 in list(mem["success_m"].keys()):
			for a in [mem["success_m"][m1],mem["fail_m"][m1]]:
				a *= self.factor

		if bool_succ:
			try:
				mem["success_m"][m1] += 1
			except KeyError:
				mem["success_m"][m1] = 1
		else:
			try:
				mem["fail_m"][m1] += 1
			except KeyError:
				mem["fail_m"][m1] = 1



class SuccessCountPerMWMP(MemoryPolicy):
	def init_memory(self,mem,voc):

		assert not 'success_mw' in list(mem.keys())
		assert not 'fail_mw' in list(mem.keys())
		mem["success_mw"] = np.zeros((voc._M, voc._W))#not adapted to growing m and w spaces, and init not 'voc is None'-proof
		mem["fail_mw"] = np.zeros((voc._M, voc._W))

	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context=[]):
		if role=='speaker':
			m1 = ms
		else:
			m1 =ms#mh justification: getting information from the other's vocabulary for the hearer
		if bool_succ:
			mem["success_mw"][m1, w]+=1.
		else:
			mem["fail_mw"][m1, w]+=1.

class SuccessCountMP(MemoryPolicy):

	def init_memory(self,mem,voc):
		assert not 'success' in list(mem.keys())
		assert not 'fail' in list(mem.keys())
		mem['success'] = 0
		mem['fail'] = 0

	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context=[]):
		if bool_succ:
			mem['success'] += 1
		else:
			mem['fail'] += 1


class TimeWeightedSuccessCountPerMWMP(SuccessCountPerMWMP):

	def __init__(self,mem_type,time_scale=100):
		MemoryPolicy.__init__(self,mem_type=mem_type)
		self.time_scale = time_scale
		self.increment = 1.
		if time_scale == 0.:
			self.factor = 0.
		else:
			self.factor = np.exp(1./self.time_scale)


	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context=[]):
		if role == 'speaker':
			m1 = ms
		else:
			m1 = ms#mh justification: getting information from the other's vocabulary for the hearer
		if bool_succ:
			mem["success_mw"][m1, w] += self.increment
		else:
			mem["fail_mw"][m1, w] += self.increment
		self.increment *= self.factor

class TimeDecreaseSuccessCountPerMWMP(TimeWeightedSuccessCountPerMWMP):

	def __init__(self,mem_type,time_scale=100,epsilon=0.01):
		MemoryPolicy.__init__(self,mem_type=mem_type)
		self.time_scale = time_scale
		if time_scale == 0.:
			self.factor = 0.
		else:
			self.factor = np.exp(1./self.time_scale)
		self.epsilon = epsilon


	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context=[]):
		if role == 'speaker':
			m1 = ms
		else:
			m1 = ms#mh justification: getting information from the other's vocabulary for the hearer
		previous_val = mem["success_mw"][m1, w],mem["fail_mw"][m1, w]
		for a in [mem["success_mw"][:,w],mem["fail_mw"][:,w],mem["success_mw"][m1,:],mem["fail_mw"][m1,:]]:
			a *= self.factor
			a[:] = np.where(a>self.epsilon,a,0.)
			if hasattr(a,'eliminate_zeros'):
				a.eliminate_zeros()
		if bool_succ:
			mem["success_mw"][m1, w] = previous_val[0]*self.factor + 1.
		else:
			mem["fail_mw"][m1, w] = previous_val[1]*self.factor + 1.


class InteractionCounts(MemoryPolicy):

	def __init__(self,mem_type,time_scale=100,epsilon=0.):
		MemoryPolicy.__init__(self,mem_type=mem_type)
		self.time_scale = time_scale
		if time_scale == 0.:
			self.factor = 0.
		else:
			self.factor = np.exp(-1./self.time_scale)
		self.epsilon = epsilon
		self.valmax = 1


	def init_memory(self,mem,voc):
		if voc is None:
			assert not 'interact_count_voc' in list(mem.keys())
			mem['interact_count_voc'] = None
		elif hasattr(voc,'_content'):
			assert not 'interact_count_m' in list(mem.keys())
			assert not 'interact_count_w' in list(mem.keys())
			mem['interact_count_m'] = np.zeros((voc._M,voc._W))
			mem['interact_count_w'] = np.zeros((voc._M,voc._W))
		else:
			assert not 'interact_count_voc' in list(mem.keys())
			mem['interact_count_voc'] = voc.__class__(start='empty',normalized=True)

	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context=[]):
		if hasattr(voc,'_content'):
			for a in [mem["interact_count_m"][ms,:],mem["interact_count_w"][:,w]]:
				a *= float(self.factor)
				a[:] = np.where(a>self.epsilon,a,0.)
				if hasattr(a,'eliminate_zeros'):
					a.eliminate_zeros()
			if self.time_scale > 0.:
				mem['interact_count_w'][ms,w] += 1.-self.factor
				mem['interact_count_m'][ms,w] += 1.-self.factor
		else:
			if ms in mem['interact_count_voc'].get_known_meanings():
				for w1 in mem['interact_count_voc'].get_known_words(m=ms):#_content_m[ms].keys():
					temp_val = mem['interact_count_voc'].get_value(ms,w1,content_type='m')
					mem['interact_count_voc'].add(m=ms,w=w1,content_type='m',val=temp_val*self.factor)
			if w in mem['interact_count_voc'].get_known_words():
				for m1 in mem['interact_count_voc'].get_known_meanings(w=w):#_content_w[w].keys():
					temp_val = mem['interact_count_voc'].get_value(m1,w,content_type='w')
					mem['interact_count_voc'].add(m=m1,w=w,content_type='w',val=temp_val*self.factor)
			if self.time_scale > 0.:
				mem['interact_count_voc'].add_value(ms,w,val=1.-self.factor,content_type='both')


	def change_time_scale(self,new_time_scale):
		self.time_scale = new_time_scale
		if time_scale == 0.:
			self.factor = 0.
		else:
			self.factor = np.exp(1./self.time_scale)

	def rebuild_global_mem(self,pop,mem):
		v = pop._agentlist[0]._vocabulary.__class__(start='empty',normalized=True)
		for ag in pop._agentlist:
			v += ag._vocabulary
		v = v/len(pop._agentlist)
		v.is_normalized = True
		mem['interact_count_voc'] = v/len(pop._agentlist)

	def clean(self,mem):
		mem['interact_count_voc'] = None


class InteractionCountsSlidingWindow(InteractionCounts):

	def __init__(self,mem_type,time_scale=100):
		MemoryPolicy.__init__(self,mem_type=mem_type)
		self.time_scale = time_scale

	def init_memory(self,mem,voc):
		InteractionCounts.init_memory(self,mem,voc)
		assert not 'past_interactions_sliding_window' in list(mem.keys())
		mem['past_interactions_sliding_window'] = []

	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context=[]):
		while len(mem['past_interactions_sliding_window'])>max(0,self.time_scale-1):
			m0,w0,val = mem['past_interactions_sliding_window'].pop(0)
			if hasattr(voc,'_content'):
				mem['interact_count_w'][m0,w0] = max(mem['interact_count_w'][m0,w0] - val , 0)
				mem['interact_count_m'][m0,w0] = max(mem['interact_count_m'][m0,w0] - val , 0)
			else:
				mem['interact_count_voc'].add_value(m0,w0,-val,content_type='both')

		if self.time_scale > 0:
			mem['past_interactions_sliding_window'].append((ms,w,1./self.time_scale))
			if hasattr(voc,'_content'):
				mem['interact_count_w'][ms,w] += 1./self.time_scale
				mem['interact_count_m'][ms,w] += 1./self.time_scale
			else:
				mem['interact_count_voc'].add_value(ms,w,1./self.time_scale,content_type='both')

	def change_time_scale(self,new_time_scale):
		self.time_scale = new_time_scale


class InteractionCountsSlidingWindowLocal(InteractionCountsSlidingWindow):

	def init_memory(self,mem,voc):
		InteractionCounts.init_memory(self,mem,voc)
		assert not 'past_interactions_sliding_window_local' in list(mem.keys())
		mem['past_interactions_sliding_window_local'] = {'m':{},'w':{}}

	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context=[]):
		if self.time_scale > 0:
			if not ms in list(mem['past_interactions_sliding_window_local']['m'].keys()):
				mem['past_interactions_sliding_window_local']['m'][ms] = []
			if not w in list(mem['past_interactions_sliding_window_local']['w'].keys()):
				mem['past_interactions_sliding_window_local']['w'][w] = []
			mem['past_interactions_sliding_window_local']['m'][ms].append((w,1./self.time_scale))
			mem['past_interactions_sliding_window_local']['w'][w].append((ms,1./self.time_scale))
			if hasattr(voc,'_content'):
				mem['interact_count_w'][ms,w] += 1./self.time_scale
				mem['interact_count_m'][ms,w] += 1./self.time_scale
			else:
				mem['interact_count_voc'].add_value(ms,w,1./self.time_scale,content_type='both')

		while ms in list(mem['past_interactions_sliding_window_local']['m'].keys()) and len(mem['past_interactions_sliding_window_local']['m'][ms])>self.time_scale:
			w0,valm = mem['past_interactions_sliding_window_local']['m'][ms].pop(0)
			if hasattr(voc,'_content'):
				mem['interact_count_m'][ms,w0] = max(mem['interact_count_m'][ms,w0] - valm , 0)
			else:
				mem['interact_count_voc'].add_value(ms,w0,-valm,content_type='m')

		while w in list(mem['past_interactions_sliding_window_local']['w'].keys()) and len(mem['past_interactions_sliding_window_local']['w'][w])>self.time_scale:
			m0,valw = mem['past_interactions_sliding_window_local']['w'][w].pop(0)
			if hasattr(voc,'_content'):
				mem['interact_count_w'][m0,w] = max(mem['interact_count_w'][m0,w] - valw , 0)
			else:
				mem['interact_count_voc'].add_value(m0,w,-valw,content_type='w')

		if self.time_scale == 0:
			if ms in list(mem['past_interactions_sliding_window_local']['m'].keys()):
				del mem['past_interactions_sliding_window_local']['m'][ms]
			if w in list(mem['past_interactions_sliding_window_local']['w'].keys()):
				del mem['past_interactions_sliding_window_local']['w'][w]


	def change_time_scale(self,new_time_scale):
		self.time_scale = new_time_scale


class BetaMAB(MemoryPolicy):

	def __init__(self,mem_type,hierarchical=False):
		MemoryPolicy.__init__(self,mem_type=mem_type)
		self.hierarchical = hierarchical

	def init_memory(self,mem,voc):
		MemoryPolicy.init_memory(self,mem,voc)
		assert not 'bandit' in list(mem.keys())
		if self.hierarchical:
			mem['bandit'] = {'arms':{'arm_explo':[1,1],'arm_exploit':[1,1],'others':{}},'old_rewards':0.}
		else:
			mem['bandit'] = {'arms':{'arm_explo':[1,1],'others':{}},'old_rewards':0.}


	def val_update(self,ms,w,mh,voc,mem,role,bool_succ,context=[]):
		if hasattr(voc,'_content'):
			new_val = srtheo_voc(voc,voc2_m=mem['interact_count_m'],voc2_w=mem['interact_count_w'])
		else:
			new_val = srtheo_voc(voc,voc2=mem['interact_count_voc'])
		delta_reward = 0.5* ( 1 + new_val - mem['bandit']['old_rewards']) # value between -1 and 1 becomes between 0 and 1
		mem['bandit']['old_rewards'] = new_val
		return delta_reward

	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context=[]):
		delta_reward = self.val_update(ms=ms,w=w,mh=mh,voc=voc,mem=mem,role=role,bool_succ=bool_succ,context=context)
		for m in voc.get_unknown_meanings():
			if m in list(mem['bandit']['arms']['others'].keys()):
				del mem['bandit']['arms']['others'][m]
		if ms not in list(mem['bandit']['arms']['others'].keys()):
			mem['bandit']['arms']['arm_explo'][0] += delta_reward
			mem['bandit']['arms']['arm_explo'][1] += 1. - delta_reward
			mem['bandit']['arms']['others'][ms] = copy.deepcopy(mem['bandit']['arms']['arm_explo'])
		else:
			mem['bandit']['arms']['others'][ms][0] += delta_reward
			mem['bandit']['arms']['others'][ms][1] += 1. - delta_reward



class BetaMABBis(BetaMAB):
	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context=[]):
		delta_reward = self.val_update(ms=ms,w=w,mh=mh,voc=voc,mem=mem,role=role,bool_succ=bool_succ,context=context)
		for m in voc.get_unknown_meanings():
			if m in list(mem['bandit']['arms']['others'].keys()):
				del mem['bandit']['arms']['others'][m]
		if ms not in list(mem['bandit']['arms']['others'].keys()):
			mem['bandit']['arms']['arm_explo'][0] += delta_reward
			mem['bandit']['arms']['arm_explo'][1] += 1. - delta_reward
			mem['bandit']['arms']['others'][ms] = [1.+delta_reward,2.-delta_reward]
		else:
			mem['bandit']['arms']['others'][ms][0] += delta_reward
			mem['bandit']['arms']['others'][ms][1] += 1. - delta_reward

class BetaMABTer(BetaMAB):
	def update_memory(self,ms,w,mh,voc,mem,role,bool_succ,context=[]):
		delta_reward = self.val_update(ms=ms,w=w,mh=mh,voc=voc,mem=mem,role=role,bool_succ=bool_succ,context=context)
		for m in voc.get_unknown_meanings():
			if m in list(mem['bandit']['arms']['others'].keys()):
				del mem['bandit']['arms']['others'][m]
		if ms not in list(mem['bandit']['arms']['others'].keys()):
			if role == 'speaker':
				mem['bandit']['arms']['arm_explo'][0] += delta_reward
				mem['bandit']['arms']['arm_explo'][1] += 1. - delta_reward
			mem['bandit']['arms']['others'][ms] = [1.+delta_reward,2.-delta_reward]
		else:
			mem['bandit']['arms']['others'][ms][0] += delta_reward
			mem['bandit']['arms']['others'][ms][1] += 1. - delta_reward

class SuccessMAB(BetaMAB):

	def val_update(self,ms,w,mh,voc,mem,role,bool_succ,context=[]):
		if bool_succ:
			return 1
		else:
			return 0
