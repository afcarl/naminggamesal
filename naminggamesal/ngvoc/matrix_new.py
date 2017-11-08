#!/usr/bin/python

import random
import numpy as np
import copy
import scipy
from scipy import sparse

from . import BaseVocabulary,BaseVocabularyElaborated
from . import voc_cache, del_cache


class VocMatrixNew(BaseVocabularyElaborated):

	def init_empty_content(self,option='m'):
		return np.zeros((len(self.get_accessible_meanings()),len(self.get_accessible_words())))

	def get_KM(self):
		return len(self._content_m)

	def get_KW(self):
		return len(self._content_w)

	def get_alterable_shallow_copy(self):
		return copy.deepcopy(self)
		#return AlterableShallowCopyVoc2DictDict(voc=self)

	#def inherit_from: to split a meaning or a word

	#@voc_cache
	def get_known_words(self,m=None,option=None):
		if m is not None:
			m_idx = self.meaning_indexes[m]
		if m is None:
			return list(set(self.get_accessible_words())-set(self.unknown_words))
		elif option is None:
			selection = self._content_m[m_idx,:]
			ans = self.get_coords(option=option,mat=selection,m_idx=m_idx)
			#ans = list(set(list(selection.nonzero()[0])))
			return [self.indexes_word[www[1]] for www in ans]
		elif option == 'max':
			selection = self._content_m[m_idx,:]
			#nz = selection.nonzero()
			ans = self.get_coords(option=option,mat=selection)
			#ans = list(set(list(np.argwhere(selection == np.amax(selection[nz])).reshape((-1)))))
			return [self.indexes_word[www[1]] for www in ans]
		elif option == 'min':
			selection = self._content_m[m_idx,:]
			#nz = selection.nonzero()
			ans = self.get_coords(option=option,mat=selection)
			#ans = list(set(list(np.argwhere(selection == np.amin(selection[nz])).reshape((-1)))))
			return [self.indexes_word[www[1]] for www in ans]


	#@voc_cache
	def get_known_meanings(self,w=None,option=None):
		if w is not None:
			w_idx = self.word_indexes[w]
		if w is None:
			return list(set(self.get_accessible_meanings())-set(self.unknown_meanings))
		elif option is None:
			selection = self._content_w[:,w_idx]
			ans = self.get_coords(option=option,mat=selection,w_idx=w_idx)
			#ans = list(set(list(selection.nonzero()[0])))
			return [self.indexes_meaning[mmm[0]] for mmm in ans]
		elif option == 'max':
			selection = self._content_w[:,w_idx]
			#nz = selection.nonzero()
			ans = self.get_coords(option=option,mat=selection)
			#ans = list(set(list(np.argwhere(selection == np.amax(selection[nz])).reshape((-1)))))
			return [self.indexes_meaning[mmm[0]] for mmm in ans]
		elif option == 'min':
			selection = self._content_w[:,w_idx]
			#nz = selection.nonzero()
			ans = self.get_coords(option=option,mat=selection)
			#ans = list(set(list(np.argwhere(selection == np.amin(selection[nz])).reshape((-1)))))
			return [self.indexes_meaning[mmm[0]] for mmm in ans]

	#@voc_cache
	def get_known_meanings_weights(self,w):
		pass

	#@voc_cache
	def get_known_words_weights(self,m):
		pass

	#@voc_cache
	def get_known_meanings_weights_values(self,w):
		selection = self._content_w[w,:]
		nz = selection.nonzero()
		ans = list(selection[nz])
		return ans

	#@voc_cache
	def get_known_words_weights_values(self,m):
		selection = self._content_m[m,:]
		nz = selection.nonzero()
		ans = list(selection[nz])
		return ans

	#@voc_cache
	def get_known_meanings_weights_indexes(self,w):
		pass

	#@voc_cache
	def get_known_words_weights_indexes(self,m):
		pass

	@del_cache
	def add(self,m,w,val=1,context=[],content_type='both'):
		assert m in self.get_accessible_meanings()
		assert w in self.get_accessible_words()
		#if hasattr(self,'valmax') and val > self.valmax:
		#	val = self.valmax
		if val <= 0:
			self.rm(m,w,content_type=content_type)
		else:
			if content_type == 'm':
				m_idx = self.meaning_indexes[m]
				w_idx = self.word_indexes[w]
				self._content_m[m_idx,w_idx] = val
				if m in self.unknown_meanings:
					self.unknown_meanings.remove(m)
				#if w in self.unknown_words:
				#	self.unknown_words.remove(w)
			elif content_type == 'w':
				m_idx = self.meaning_indexes[m]
				w_idx = self.word_indexes[w]
				self._content_w[m_idx,w_idx] = val
				#if m in self.unknown_meanings:
				#	self.unknown_meanings.remove(m)
				if w in self.unknown_words:
					self.unknown_words.remove(w)
			elif content_type == 'both':
				self.add(m=m,w=w,val=val,context=context,content_type='m')
				self.add(m=m,w=w,val=val,context=context,content_type='w')
			else:
				raise ValueError('unknown content type:'+str(content_type))

	@del_cache
	def rm(self,m,w,content_type='both'):
		assert m in self.get_accessible_meanings()
		assert w in self.get_accessible_words()
		if content_type == 'm':
			m_idx = self.meaning_indexes[m]
			w_idx = self.word_indexes[w]
			self._content_m[m_idx,w_idx] = 0
		elif content_type == 'w':
			m_idx = self.meaning_indexes[m]
			w_idx = self.word_indexes[w]
			self._content_w[m_idx,w_idx] = 0
		elif content_type == 'both':
			self.rm(m=m,w=w,content_type='m')
			self.rm(m=m,w=w,content_type='w')
		else:
			raise ValueError('unknown content type:'+str(content_type))

	def get_value(self,m,w,content_type='m'):
		m_idx = self.meaning_indexes[m]
		w_idx = self.word_indexes[w]
		if content_type == 'm':
			return self._content_m[m_idx,w_idx]
		if content_type == 'w':
			return self._content_w[m_idx,w_idx]
		else:
			raise ValueError('content type nopt recognized')

	def rm_syn(self,m,w,content_type='both'):
		for i in self.get_known_words(m=m):
			if i!=w:
				self.rm(m,i,content_type=content_type)

	def rm_hom(self,m,w,content_type='both'):
		for i in self.get_known_meanings(w=w):
			if i!=m:
				self.rm(i,w,content_type=content_type)

	def discover_meanings(self,m_list):
		m_list_bis = BaseVocabularyElaborated.discover_meanings(self,m_list=m_list)
		if not hasattr(self,'meaning_indexes'):
			self.meaning_indexes = {}
			self.indexes_meaning = {}
		max_ind = len(list(self.meaning_indexes.keys()))-1
		for mm in m_list_bis:
			max_ind += 1
			self.meaning_indexes[mm] = max_ind
			self.indexes_meaning[max_ind] = mm
		self.update_vocshape()
		return m_list_bis


	def discover_words(self,w_list):
		w_list_bis = BaseVocabularyElaborated.discover_words(self,w_list=w_list)
		if not hasattr(self,'word_indexes'):
			self.word_indexes = {}
			self.indexes_word = {}
		max_ind = len(list(self.word_indexes.keys()))-1
		for ww in w_list_bis:
			max_ind += 1
			self.word_indexes[ww] = max_ind
			self.indexes_word[max_ind] = ww
		self.update_vocshape()
		return w_list_bis

	def update_vocshape(self):
		M = len(self.get_accessible_meanings())
		W = len(self.get_accessible_words())
		new_w = self.init_empty_content()
		new_m = self.init_empty_content()
		M1,W1 = self._content_w.shape
		M2,W2 = self._content_m.shape
		if M1*W1 != 0:
			new_w[:(M-M1),:(W-W1)] = self._content_w
		if M2*W2 != 0:
			new_w[:(M-M2),:(W-W2)] = self._content_m
		self._content_w = new_w
		self._content_m = new_m

	def get_coords(self,mat,option=None,w_idx=None,m_idx=None):
		nz = mat.nonzero()
		if not nz[0].size:
			return []
		if option is None:
			return self.get_coords_none(mat,nz=nz,w_idx=w_idx,m_idx=m_idx)
		elif option == 'max':
			return self.get_coords_max(mat,nz=nz)
		elif option == 'min':
			return self.get_coords_min(mat,nz=nz)
		elif option == 'minofmaxw':
			return self.get_coords_minofmaxw(mat,nz=nz)
		elif option == 'minofmaxm':
			return self.get_coords_minofmaxm(mat,nz=nz)

	def get_coords_none(self,mat,nz=None,w_idx=None,m_idx=None):
		if nz is None:
			nz = mat.nonzero()
		if w_idx is not None:
			coords = [(nn,w_idx) for nn in nz[0]]
		elif m_idx is not None:
			coords = [(m_idx,nn) for nn in nz[0]]
		else:
			coords = nz[0]
		return coords

	def get_coords_max(self,mat,nz=None):
		if nz is None:
			nz = mat.nonzero()
		coords = np.argwhere(mat == np.amax(mat[nz]))
		coords = coords.reshape((-1,2))
		return coords

	def get_coords_min(self,mat,nz=None):
		if nz is None:
			nz = mat.nonzero()
		coords = np.argwhere(mat == np.amin(mat[nz]))
		coords = coords.reshape((-1,2))
		return coords

	def get_coords_minofmaxw(self,mat,nz=None):
		best_scores = mat.max(axis=0)
		val = np.amin(best_scores)
		coords = np.argwhere(best_scores == val)
		coords = coords.reshape((-1,2))
		return coords

	def get_coords_minofmaxm(self,mat,nz=None):
		best_scores = mat.max(axis=1)
		val = np.amin(best_scores)
		coords = np.argwhere(best_scores == val)
		coords = coords.reshape((-1,2))
		return coords



class VocSparseNew(VocMatrixNew):

	def init_empty_content(self,option='m'):
		if option == 'm':
			return sparse.csr_matrix((len(self.get_accessible_meanings()),len(self.get_accessible_words())))
		elif option == 'w':
			return sparse.csc_matrix((len(self.get_accessible_meanings()),len(self.get_accessible_words())))
		else:
			raise ValueError('no such option: '+str(option))



	def get_coords_none(self,mat,nz=None,w_idx=None,m_idx=None):
		if nz is None:
			nz = mat.nonzero()
		coords = [(nz[0][i],nz[1][i]) for i in range(len(nz[0]))] #tolist??
		return coords

	def get_coords_max(self,mat,nz=None):
		if nz is None:
			nz = mat.nonzero()
		coords = [(nz[0][i[0]],nz[1][i[0]]) for i in np.argwhere(mat.data == mat.data.max()) if mat.data.any()]
		return coords

	def get_coords_min(self,mat,nz=None):
		if nz is None:
			nz = mat.nonzero()
		coords = [(nz[0][i[0]],nz[1][i[0]]) for i in np.argwhere(mat.data == mat.data.min()) if mat.data.any()]
		return coords

	def get_coords_minofmaxm(self,mat,nz=None):
		if nz is None:
			nz = mat.nonzero()
		meanings = self.get_known_meanings(option=None)
		best_scores = np.zeros(len(meanings))
		for i in range(len(nz[0])):
			m = nz[0][i]
			w = nz[1][i]
			index_m = np.argwhere(meanings == m).reshape((-1))[0]
			best_scores[index_m] = max(best_scores[index_m],mat[m,w])
		val = np.amin(best_scores)
		coords_m = np.argwhere(best_scores == val).reshape((-1))
		coords = []
		for m_i in coords_m:
			coords += [(m_i,w_i) for w_i in self.get_known_words(m=m_i,option='max')]
		return coords

	def get_coords_minofmaxw(self,mat,nz=None):
		if nz is None:
			nz = mat.nonzero()
		words = self.get_known_words(option=None)
		best_scores = np.zeros(len(words))
		for i in range(len(nz[0])):
			m = nz[0][i]
			w = nz[1][i]
			index_w = np.argwhere(words == w).reshape((-1))[0]
			best_scores[index_w] = max(best_scores[index_w],mat[m,w])
		val = np.amin(best_scores)
		coords_w = np.argwhere(best_scores == val).reshape((-1))
		coords = []
		for w_i in coords_w:
			coords += [(m_i,w_i) for m_i in self.get_known_meanings(w=w_i,option='max')]
		return coords