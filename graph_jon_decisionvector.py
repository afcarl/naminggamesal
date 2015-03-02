#!/usr/bin/python
# -*- coding: latin-1 -*-

from ngmeth import *
import my_functions
from scipy import optimize as sciopt
import random
import matplotlib.pyplot as plt
import multiprocessing
import custom_graph
import copy

MULTI_PROCESSING=0
NB_PROCESS=2

voctype="sparse"
M=8
W=8
nbagents=8
step=1

nb_iter=4
Tmax=[500,1000,2000]


X=range(1,M)


#OPERATION=pop_ize(Nlink)


def MESURE(pop):
	return 1-(entropypop(pop)/float(entropypop_max(pop)))






def function_r(param_list):
	param=param_list[0]
	progress_info={"progress_info":str(param_list[1])+"  "+str(param)}
	decvec=[1]+[1]*min(param,M-1)+[0]*(M-min(param,M-1))
	strat={"strattype":"decisionvector","decvec":decvec}
	temppop=Population(voctype,strat,nbagents,M,W)
	T=0
	result=[]
	for i in Tmax:
		progress_info_temp=copy.deepcopy(progress_info)
		progress_info_temp["progress_info"]=progress_info_temp["progress_info"]+"  T:"+str(i)+"/"+str(Tmax[-1])
		temppop.play_game(i-T,**progress_info_temp)
		T=i
		result.append(MESURE(temppop))
	return result

RANGE_PARAM_avec_iter=[]
for i in range(nb_iter):
	for j in range(len(X)):
		RANGE_PARAM_avec_iter.append([X[j],i])

result_list=[]
if MULTI_PROCESSING and __name__=="__main__":
	proc_pool=multiprocessing.Pool(processes=NB_PROCESS)
	result_list=proc_pool.map_async(function_r,RANGE_PARAM_avec_iter).get(9999999)
else:
	for j in RANGE_PARAM_avec_iter:
		result_list.append(function_r(j))


tempgraph=custom_graph.CustomGraph(X,ymin=0,ymax=1,xmin=0,xmax=M)
tempgraph.empty()

for i in range(nb_iter):

	for k in range(len(Tmax)):
		Y=[]
		for j in range(len(X)):
			decal=len(X)*i
			i1=decal+j
			i2=k
			Y.append(result_list[i1][i2])
		tempgraph2=custom_graph.CustomGraph(X,Y,Yoptions=[{"label":("Tmax="+str(Tmax[k]))}])
		tempgraph.add_graph(copy.deepcopy(tempgraph2))




print tempgraph.Yoptions
tempgraph=tempgraph.wise_merge()
tempgraph.std=1
tempgraph.title="Graph suggere par Jon, entropypop, decisionvector, M="+str(M)+" W="+str(W)+" N="+str(nbagents)+" iter="+str(nb_iter)
tempgraph.show()
tempgraph.write_files()










# return custom_graph.CustomGraph(X,Y,xmin=0,xmax=1,Yoptions={"label":str(AAAAAAAAAAAA)})



# tempgraph=graph_list[0]
# for j in range(0,nb_iter):
# 	tempgraph.add_graph(graph_list[j])

# tempgraph.std=1
# tempgraph.merge()
# tempgraph.show()

raw_input("pressing enter will end program and close graphs")

#X1=np.array(range(1,10))*0.1