#!/usr/bin/python
import Bid, Slot

class Auction:
	'This class represents an auction of multiple ad slots to multiple advertisers'
	query = ""
	bids = []

	def __init__(self, term, bids1=[]):
		self.query = term
		
		for b in bids1:
			j=0
			#print (len(self.bids))
			while j < len(self.bids) and float(b.value) < float(self.bids[j].value):
				j+=1
			self.bids.insert(j,b)

	'''
	This method accepts a Vector of slots and fills it with the results
	of a VCG auction. The competition for those slots is specified in the bids Vector.
	@param slots a Vector of Slots, which (on entry) specifies only the clickThruRates
	and (on exit) also specifies the name of the bidder who won that slot,
	the price said bidder must pay,
	and the expected profit for the bidder.  
	'''
	def executeVCG(self,slots):
		totalSlots = len(slots) - 1
		bidNo = min(len(self.bids), len(slots)) - 1 #total number of bidders that can win a slot
		while bidNo >= 0:
			slots[bidNo].bidder = self.bids[bidNo].name
			trueValue = slots[bidNo].clickThruRate * self.bids[bidNo].value
			if bidNo+1 <= (len(self.bids)-1) and bidNo+1 <= totalSlots: #control cases when the No. of slots is different to the No. of bidders
				slots[bidNo].price = self.calculateVCG(slots[bidNo].clickThruRate,
														slots[bidNo+1].clickThruRate,
														self.bids[bidNo+1].value,
														slots[bidNo+1].price)

			elif (len(self.bids)-1) > totalSlots or bidNo+1 == totalSlots: #calculate VCG for looser
				slots[bidNo].price = self.calculateVCG(slots[bidNo].clickThruRate, 0, self.bids[bidNo+1].value, 0)

			slots[bidNo].profit = trueValue - slots[bidNo].price
			bidNo-=1

	'''
	Calculate the VCG value for the advertiser i that witn a slot. 
		It is based on the 2nd price auction scheme but it also charges the harm winning
		advertiser impose on the others.

	@param ctr 		Click Trough Rate of the assigned slot
	@param ctrSP	Click Trough Rate that the 2nd bidder is willing to pay
	@param bidSP	Bid value that 2nd bidder use on the auction
	@param priceSP	Price that 2nd has to pay
	'''
	def calculateVCG(self, ctr, ctrSP, bidSP, priceSP):
		return ( (ctr - ctrSP) * bidSP ) + priceSP
