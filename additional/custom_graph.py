#!/usr/bin/python
import sys
try:
	if sys.version_info.major == 2:
		import Tkinter
	else:
		import tkinter
except ImportError:
	import matplotlib
	matplotlib.use('Agg')
	sys.stderr.write('Tkinter not installed, loading matplotlib and pyplot with Agg backend\n')

import matplotlib.pyplot as plt
import time
import numpy as np
import pickle
import copy

import matplotlib
import seaborn as sns
#sns.set(rc={'image.cmap': 'Purples_r'})

sns.set_style('darkgrid')
matplotlib.rcParams['pdf.fonttype'] = 42  #set font type to true type, avoids possible incompatibility while submitting papers
matplotlib.rcParams['ps.fonttype'] = 42

def load_graph(filename):
	with open(filename, 'rb') as fichier:
		mon_depickler=pickle.Unpickler(fichier)
		tempgr=mon_depickler.load()
	return tempgr


class CustomGraph(object):
	def __init__(self,Y=None,X=None,**kwargs):
		self.keepwinopen=0
		self.sort=1
		self.filename="graph"+time.strftime("%Y%m%d%H%M%S", time.localtime())
		if "filename" in list(kwargs.keys()):
			self.filename=kwargs["filename"]
		self.title = self.filename
		self.xlabel = "X"
		self.ylabel = "Y"
		self.alpha = 0.3

		self.Yoptions = [{}]
		self.legendoptions = {}
		self.legend_permut = []

		self.loglog = False
		self.semilog = False
		self.loglog_basex = 10
		self.loglog_basey = 10

		self.xmin = None
		self.xmax = None
		self.ymin = None
		self.ymax = None

		self.std = False

		if Y is None:
			self._Y = []
		else:
			self._Y = [Y]
		self.stdvec=[0]*len(Y)

		if X is None:
			self._X = [list(range(len(Y)))]
		else:
			self._X = [X]


		self.extensions=["eps","png","pdf"]

		for key,value in kwargs.items():
			setattr(self,key,value)

		self.stdvec=[self.stdvec]

		self.init_time=time.strftime("%Y%m%d%H%M%S", time.localtime())
		self.modif_time=time.strftime("%Y%m%d%H%M%S", time.localtime())

	def show(self):
		plt.ion()
		fig = plt.gcf()
		self.draw()
		plt.show()
		return fig

	def save(self,*path):
		if path:
			out_path=path[0]
		else:
			out_path="graphs/"
		with open(out_path+self.filename+".b", 'wb') as fichier:
			mon_pickler=pickle.Pickler(fichier)
			mon_pickler.dump(self)

	def write_files(self,*path):
		backend = plt.get_backend()
		plt.switch_backend('Agg')
		if len(path)!=0:
			out_path=path[0]
		else:
			out_path=""

		self.save(out_path)
		self.draw()
		for extension in self.extensions:
			plt.savefig(out_path+self.filename+"."+extension,format=extension,bbox_inches='tight')
		plt.switch_backend(backend)

	def draw(self):

		#colormap=['blue','black','green','red','yellow','cyan','magenta']
		#colormap=['black','green','red','blue','yellow','cyan','magenta']
		#colormap=['blue','red','green','black','yellow','cyan','magenta']
		#colormap=['black','green','blue','red','yellow','cyan','magenta']
		#colormap=['darkolivegreen','green','darkorange','red','yellow','cyan','magenta']


		#plt.figure()
		plt.ion()
		plt.cla()
		plt.clf()
		current_palette=sns.color_palette()
		for i in range(0,len(self._Y)):

			Xtemp=copy.deepcopy(self._X[i])
			Ytemp=copy.deepcopy(self._Y[i])
			stdtemp=copy.deepcopy(self.stdvec[i])
			if self.sort: # WARNING!!!!! No X value should appear 2 times -> bug to solve
				tempdic={}
				for j in range(0,len(Xtemp)):
					tempdic[Xtemp[j]]=[Ytemp[j],stdtemp[j]]
				temptup=sorted(tempdic.items())
				for j in range(0,len(temptup)):
					Xtemp[j]=temptup[j][0]
					Ytemp[j]=temptup[j][1][0]
					stdtemp[j]=temptup[j][1][1]

			base_line = plt.plot(Xtemp,Ytemp,**self.Yoptions[i])[0]
			if self.loglog:
				plt.xscale('symlog',basex=self.loglog_basex)
				plt.yscale('symlog',basex=self.loglog_basey)
			elif self.semilog:
				plt.xscale('symlog',basex=self.loglog_basex)
			if self.std:
				Ytempmin=[0]*len(Ytemp)
				Ytempmax=[0]*len(Ytemp)
				for j in range(0,len(Ytemp)):
					Ytempmax[j]=Ytemp[j]+stdtemp[j]
					Ytempmin[j]=Ytemp[j]-stdtemp[j]
				if 'color' in list(self.Yoptions[i].keys()):
					plt.fill_between(Xtemp,Ytempmin,Ytempmax, alpha=self.alpha,**self.Yoptions[i])
				else:
					plt.fill_between(Xtemp,Ytempmin,Ytempmax, alpha=self.alpha, facecolor=base_line.get_color(), **self.Yoptions[i])

		plt.xlabel(self.xlabel)
		plt.ylabel(self.ylabel)
		plt.title(self.title)

		if self.xmin is not None:
			plt.xlim(xmin=self.xmin)
		if self.xmax is not None:
			plt.xlim(xmax=self.xmax)
		if self.ymin is not None:
			plt.ylim(ymin=self.ymin)
		if self.ymax is not None:
			plt.ylim(ymax=self.ymax)

		handles, labels = plt.axes().get_legend_handles_labels()
		handles2, labels2 = [], []
		for tr in range(len(self.legend_permut)):
			handles2.append(handles[self.legend_permut[tr]])
			#handles2[self.legend_permut[tr]] = handles[tr]
			labels2.append(labels[self.legend_permut[tr]])
			#labels2[self.legend_permut[tr]] = labels[tr]



		plt.legend(handles2, labels2, **self.legendoptions)

		#plt.legend(bbox_to_anchor=(0,0,0.55,0.8))
		#plt.legend(bbox_to_anchor=(0,0,0.5,1))
		#
		#plt.legend(bbox_to_anchor=(0,0,1,0.7))
		#plt.legend(bbox_to_anchor=(0,0,1,0.54))
		if hasattr(self, 'fontsize'):
			matplotlib.rcParams['font.size'] = self.fontsize
			matplotlib.rcParams['xtick.labelsize'] = self.fontsize
			matplotlib.rcParams['ytick.labelsize'] = self.fontsize
			matplotlib.rcParams['axes.titlesize'] = self.fontsize
			matplotlib.rcParams['axes.labelsize'] = self.fontsize
			matplotlib.rcParams['legend.fontsize'] = self.fontsize
		if hasattr(self, 'rcparams'):
			for key,value in self.rcparams:
				matplotlib.rcParams[key] = value
		plt.draw()


	def add_graph(self,other_graph):
		self._X=self._X+other_graph._X
		self._Y=self._Y+other_graph._Y
		self.Yoptions=self.Yoptions+other_graph.Yoptions
		self.stdvec=self.stdvec+other_graph.stdvec

	def complete_with(self,other_graph, mix=True, remove_duplicates=False):
		for i in range(0,len(self._X)):
			if mix and not self._X[-1]<other_graph._X[0]:
				X = copy.deepcopy(self._X[i])
				Y = copy.deepcopy(self._Y[i])
				stdvec = copy.deepcopy(self.stdvec[i])
				Xind = 0
				oXind = 0
				self._X[i] = []
				self._Y[i] = []
				self.stdvec[i] = []
				while Xind < len(X) and oXind < len(other_graph._X[i]):
					if X[Xind] < other_graph._X[i][oXind]:
						self._X[i].append(X[Xind])
						self._Y[i].append(Y[Xind])
						self.stdvec[i].append(stdvec[Xind])
						Xind += 1
					elif X[Xind] > other_graph._X[i][oXind]:
						self._X[i].append(other_graph._X[i][oXind])
						self._Y[i].append(other_graph._Y[i][oXind])
						self.stdvec[i].append(other_graph.stdvec[i][oXind])
						oXind += 1
					else:
						self._X[i].append(X[Xind])
						self._Y[i].append(Y[Xind])
						self.stdvec[i].append(stdvec[Xind])
						Xind += 1
						oXind += 1
			else:
				self._X[i]=list(copy.deepcopy(self._X[i]))+list(copy.deepcopy(other_graph._X[i]))
				self._Y[i]=list(copy.deepcopy(self._Y[i]))+list(copy.deepcopy(other_graph._Y[i]))
				self.stdvec[i]=list(copy.deepcopy(self.stdvec[i]))+list(copy.deepcopy(other_graph.stdvec[i]))
			if remove_duplicates:
				X = copy.deepcopy(self._X[i])
				Y = copy.deepcopy(self._Y[i])
				stdvec = copy.deepcopy(self.stdvec[i])
				self._X[i] = []
				self._Y[i] = []
				self.stdvec[i] = []
				for j in range(len(X)):
					if X[j] not in self._X[i]:
						self._X[i].append(X[j])
						self._Y[i].append(Y[j])
						self.stdvec[i].append(stdvec[j])
		self.modif_time=time.strftime("%Y%m%d%H%M%S", time.localtime())

#	def complete_with(self,other_graph):
#		for i in range(0,len(self._X)):
#			self._X[i]=range(0, len(self._X[i])+len(other_graph._X[i]))
#			self._Y[i]=list(copy.deepcopy(self._Y[i]))+list(copy.deepcopy(other_graph._Y[i]))
#			self.stdvec[i]=list(copy.deepcopy(self.stdvec[i]))+list(copy.deepcopy(other_graph.stdvec[i]))
#		self.modif_time=time.strftime("%Y%m%d%H%M%S", time.localtime())

	def merge(self):
		#Yarray=np.array(self._Y)
		#stdarray=np.array(self.stdvec)
		Xcopy = copy.deepcopy(self._X)
		Ycopy = copy.deepcopy(self._Y)
		stdcopy = copy.deepcopy(self.stdvec)
		stdtemp = []
		Ytemp = []
		#Xtemp = []
		self.Yoptions=[self.Yoptions[0]]
		self.std=1
		Ydict = {}
		for j in range(len(self._Y)):
			for i in range(len(self._Y[j])):
				if Xcopy[j][i] in list(Ydict.keys()):
					Ydict[Xcopy[j][i]].append(Ycopy[j][i])
				else:
					Ydict[Xcopy[j][i]] = [Ycopy[j][i]]
		Xlist = list(Ydict.keys())
		Xlist.sort()
		for x in Xlist:
			Ylist = Ydict[x]
			Ytemp.append(np.mean(Ylist))
			stdtemp.append(np.std(Ylist))


		#max_length = max([len(self._Y[j]) for j in range(len(self._Y))])
		#for i in range(max_length):
		#	Ylist = [Ycopy[j][i] for j in range(len(Ycopy)) if len(Ycopy[j])>i]
		#	Ytemp.append(np.mean(Ylist))
		#	stdtemp.append(np.std(Ylist))
		#	#Ytemp.append(np.mean(list(Yarray[:,i])))
		#	#stdtemp.append(np.std(list(Yarray[:,i])))
		self._Y = [Ytemp]
		self.stdvec = [stdtemp]
		self._X = [Xlist]
		self.modif_time = time.strftime("%Y%m%d%H%M%S", time.localtime())



	def wise_merge(self):
		param_list=[]
		for i in range(len(self.Yoptions)):
			param_list.append(self.Yoptions[i]["label"])
		param_values={}
		for ind,param in enumerate(param_list):
			if param not in list(param_values.keys()):
				param_values[param]=copy.deepcopy(self)
				param_values[param]._X=[self._X[ind]]
				param_values[param]._Y=[self._Y[ind]]
				param_values[param].Yoptions=[self.Yoptions[ind]]
			else:
				tempgraph=copy.deepcopy(self)
				tempgraph._X=[self._X[ind]]
				tempgraph._Y=[self._Y[ind]]
				tempgraph.Yoptions=[self.Yoptions[ind]]
				param_values[param].add_graph(copy.deepcopy(tempgraph))
		tempgraph=copy.deepcopy(self)
		tempgraph._X=[]
		tempgraph._Y=[]
		tempgraph.Yoptions=[]
		tempgraph.stdvec=[]
		for key in list(param_values.keys()):
			param_values[key].merge()
			tempgraph.add_graph(param_values[key])
		self.modif_time=time.strftime("%Y%m%d%H%M%S", time.localtime())
		return tempgraph

	def empty(self):
		self._Y=[]
		self._X=[]
		self.Yoptions=[]
		self.stdvec=[]
		self.modif_time=time.strftime("%Y%m%d%H%M%S", time.localtime())


	def func_of(self,graph2):
		newgraph=copy.deepcopy(self)
		for i in range(0,len(newgraph._X)):
			newgraph._X[i]=graph2._Y[i]
			newgraph.xlabel=graph2.title[6:]
			newgraph.title=self.title+"_func_of_"+newgraph.xlabel
		return newgraph
