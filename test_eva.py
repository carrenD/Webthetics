import sys
from PIL import Image
import caffe

import itertools
from scipy.stats import pearsonr

def evaPearsonr(gt, pred):
	return pearsonr(gt, pred)

def getGT(gt_file):
	gt = []
	images = []
	for line in open(gt_file, 'r'):
		fle, rating = line.strip().split()
		gt.append(float(rating))
		images.append(fle)
	return gt, images

def infe():
	net = caffe.Net('webthetics.prototxt','.\\model\\webthetics.caffemodel', caffe.TEST)
	net.forward()
	rating = net.blobs['fc8'].data
	loss = net.blobs['loss'].data

	gt_file = '.\\data\\test_list_eva.txt'
	gt, images = getGT(gt_file)
	pred = list(itertools.chain.from_iterable(rating))
	eva = evaPearsonr(gt, pred)

	print eva
	print 'Pearsonr: {}, p-value: {}, loss: {}'.format(eva[0], eva[1], loss)
		

if __name__ == '__main__':
	try:
		infe()
	except KeyboardInterrupt:
		sys.exit(0)
