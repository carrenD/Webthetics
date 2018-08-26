import os, sys
from PIL import Image
import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib
import caffe
import itertools
from scipy import ndimage
import cv2

from scipy.stats import pearsonr


def getGT(gt_file):
	gt = []
	images = []
	for line in open(gt_file, 'r'):
		fle, rating = line.strip().split()
		gt.append(float(rating))
		images.append(fle)
	return gt, images


def random_small_occlusion_image(size=50):
	# in paper, the size was set as 10, 20, 30, 40, 50
	data_path = '.\\data\\'
	occlusion_path = '.\\data\\data_occlusion_' + str(size) + 'x' + str(size) + 'x100\\'
	if not os.path.exists(occlusion_path):
		os.makedirs(occlusion_path)
		os.makedirs(occlusion_path + 'english')
		os.makedirs(occlusion_path + 'foreign')
		os.makedirs(occlusion_path + 'grayscale')

	with open('.\\data\\test_list_eva.txt', 'r') as f:
		for line in f:
			image, rate = line.strip().split()
			img_path = os.path.join(data_path, image.split('\\')[0], image.split('\\')[1])
			print img_path
			img = Image.open(img_path, 'r')
			pixels = img.load()
			for occlusion_num in xrange(100): # make 100 small block occlusions
				start_width = random.randint(0,img.size[0]-size)
				start_height = random.randint(0,img.size[1]-size)
				for i in xrange(start_width, start_width+size):
					for j in xrange(start_height, start_height+size):
						pixels[i,j] = 0
			img.save(os.path.join(occlusion_path, image.split('\\')[0], image.split('\\')[1])) 


def large_occlusion_image(size=500):
	# in paper, the size was set as 100, 200, 300, 400, 500
	data_path = '.\\data\\'
	occlusion_path = '.\\data\\data_occlusion_' + str(size) + 'x' + str(size) + '\\'
	if not os.path.exists(occlusion_path):
		os.makedirs(occlusion_path)
		os.makedirs(occlusion_path + 'english')
		os.makedirs(occlusion_path + 'foreign')
		os.makedirs(occlusion_path + 'grayscale')
	with open('.\\data\\test_list_eva.txt', 'r') as f:
		for line in f:
			image, rate = line.strip().split()
			img_path = os.path.join(data_path, image.split('\\')[0], image.split('\\')[1])
			print img_path
			img = Image.open(img_path, 'r')
			pixels = img.load()
			start_width = random.randint(0,img.size[0]-size)
			start_height = random.randint(0,img.size[1]-size)
			for i in xrange(start_width, start_width+size):
				for j in xrange(start_height, start_height+size):
					pixels[i,j] = 0
			img.save(os.path.join(occlusion_path, image.split('\\')[0], image.split('\\')[1])) 


def occlusion_ratio_vertival(ratio=50):
	# in paper, the rato was set as 10, 20, 30, 40, 50
	# this function can be adapted to occlude left, right and middle part of the webpage
	data_path = '.\\data\\'
	occlusion_path = '.\\data\\data_occlusion_middle_ver_' + str(ratio)+ '%\\'
	if not os.path.exists(occlusion_path):
		os.makedirs(occlusion_path)
		os.makedirs(occlusion_path + 'english')
		os.makedirs(occlusion_path + 'foreign')
		os.makedirs(occlusion_path + 'grayscale')
	with open('.\\data\\test_list_eva.txt', 'r') as f:
		for line in f:
			image, rate = line.strip().split()
			img_path = os.path.join(data_path, image.split('\\')[0], image.split('\\')[1])
			print img_path
			img = Image.open(img_path, 'r')
			pixels = img.load()
			start_width = img.size[0]/2
			step = (ratio/10) * img.size[0]/10
			for i in xrange(start_width-step/2, start_width+step/2):
				for j in xrange(img.size[1]):
					# pixels[i,j] = 0               # left: for i in xrange(start_width, start_width+step)
					# pixels[img.size[0]-1-i,j] = 0 # right: for i in xrange(start_width, start_width+step)
					pixels[i,j] = 0                 # middle: xrange(start_width-step/2, start_width+step/2) 
			img.save(os.path.join(occlusion_path, image.split('\\')[0], image.split('\\')[1])) 


def occlusion_ratio_horizontal(ratio=50):
	# in paper, the rato was set as 10, 20, 30, 40, 50
	# this function can be adapted to occlude top, down and middle part of the webpage
	data_path = '.\\data\\'
	occlusion_path = '.\\data\\data_occlusion_middle_hor_' + str(ratio) + '%\\'
	if not os.path.exists(occlusion_path):
		os.makedirs(occlusion_path)
		os.makedirs(occlusion_path + 'english')
		os.makedirs(occlusion_path + 'foreign')
		os.makedirs(occlusion_path + 'grayscale')
	with open('.\\data\\test_list_eva.txt', 'r') as f:
		for line in f:
			image, rate = line.strip().split()
			img_path = os.path.join(data_path, image.split('\\')[0], image.split('\\')[1])
			print img_path
			img = Image.open(img_path, 'r')
			pixels = img.load()
			start_height = img.size[1]/2
			step = (ratio/10) * img.size[1]/10
			for i in xrange(img.size[0]):
				for j in xrange(start_height-step/2, start_height+step/2):
					pixels[i,j] = 0
			img.save(os.path.join(occlusion_path, image.split('\\')[0], image.split('\\')[1])) 


def low_frequency_pass():
	# filter out the low frequency contents
	data_path = '.\\data\\'
	occlusion_path = '.\\data\\data_occlusion_low_frequency_pass\\'
	if not os.path.exists(occlusion_path):
		os.makedirs(occlusion_path)
		os.makedirs(occlusion_path + 'english')
		os.makedirs(occlusion_path + 'foreign')
		os.makedirs(occlusion_path + 'grayscale')
	with open('.\\data\\test_list_eva.txt', 'r') as f:
		for line in f:
			image, rate = line.strip().split()
			img_path = os.path.join(data_path, image.split('\\')[0], image.split('\\')[1])
			img = Image.open(img_path, 'r')
			data = np.array(img)
			kernel = np.array([[1./25, 1./25, 1./25, 1./25, 1./25],
			                   [1./25, 1./25, 1./25, 1./25, 1./25],
			                   [1./25, 1./25, 1./25, 1./25, 1./25],
			                   [1./25, 1./25, 1./25, 1./25, 1./25],
			                   [1./25, 1./25, 1./25, 1./25, 1./25]])
			data[:,:,0] = ndimage.convolve(data[:,:,0], kernel)
			data[:,:,1] = ndimage.convolve(data[:,:,1], kernel)
			data[:,:,2] = ndimage.convolve(data[:,:,2], kernel)

			lowpass_img = Image.fromarray(data)
			lowpass_img.save(os.path.join(occlusion_path, image.split('\\')[0], image.split('\\')[1]))
			

def high_frequency_pass():
	# enhance the high frequency content within the webpage
	data_path = '.\\data\\'
	occlusion_path = '.\\data\\data_occlusion_high_frequency_pass\\'
	if not os.path.exists(occlusion_path):
		os.makedirs(occlusion_path)
		os.makedirs(occlusion_path + 'english')
		os.makedirs(occlusion_path + 'foreign')
		os.makedirs(occlusion_path + 'grayscale')
	with open('.\\data\\test_list_eva.txt', 'r') as f:
		for line in f:
			image, rate = line.strip().split()
			img_path = os.path.join(data_path, image.split('\\')[0], image.split('\\')[1])
			print img_path
			img = Image.open(img_path, 'r')
			data = np.array(img)
			data = cv2.Laplacian(data,cv2.CV_64F)

			highpass_img = Image.fromarray((data*255).astype('uint8')+np.array(img))
			highpass_img.save(os.path.join(occlusion_path, image.split('\\')[0], image.split('\\')[1]))


def infe():
	# need to change the path in the .prototxt file, to specify which test dataset to use
	# the pre-trained webthetics model was saved under model_zoo folder
	net = caffe.Net('webthetics.prototxt','..\\model\\webthetics.caffemodel', caffe.TEST)
	net.forward()
	rating = net.blobs['fc8'].data
	loss = net.blobs['loss'].data

	gt_file = '.\\data\\test_list_eva.txt'
	gt, images = getGT(gt_file)
	pred = list(itertools.chain.from_iterable(rating))
	eva = pearsonr(gt, pred)
	print eva

def main():
	# random_small_occlusion_image()
	# large_occlusion_image()
	# occlusion_ratio_vertival()
	# occlusion_ratio_horizontal()
	# low_frequency_pass()
	# high_frequency_pass()
	infe()

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		sys.exit(0)
