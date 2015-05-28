from rejection import RejectionSampling
from weighting import LikelyhoodWeighting
from particlefilter import ParticleFiltering


def main():

	# avg = 0
	# for i in xrange(0, 10):
	# 	rs = RejectionSampling("inference.txt")
	# 	rst = rs.run()
	# 	avg += rst[1]
	# print avg/10.0

	# avg = 0
	# for i in xrange(0, 10):
	# 	lw = LikelyhoodWeighting("inference.txt")
	# 	rst = lw.run()
	# 	avg += rst[1]
	# print avg/10.0

	avg = 0
	for i in xrange(0, 30):
		rf = ParticleFiltering("umbrellas.txt")
		rst = rf.run()
		avg += rst[1]
	print avg/30.0



if __name__ == '__main__':
	main()
