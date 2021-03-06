from . import VocUpdate

class Frequency(VocUpdate):

	def update_hearer(self,ms,w,mh,voc,mem,bool_succ, context=[]):
		y = 1./(2 - voc.get_value(ms, w)) # y = 1 - 1/(f+1)
		y = min(1,y)
		y = max(0,y)
		voc.add(ms,w,y,context=context) # f <- f+1
		voc.finish_update()

	def update_speaker(self,ms,w,mh,voc,mem,bool_succ, context=[]):
		voc.finish_update()
