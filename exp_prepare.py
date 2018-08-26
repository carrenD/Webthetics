import os, sys
import csv
import numpy as np
from random import shuffle

def walkDirWithExensions(image_folder, extensions):
    image_list = []
    for (dirpath, dirnames, filenames) in os.walk(image_folder):
		for filename in filenames:
			result_file_path = os.path.join(dirpath, filename)
			if os.path.isfile(result_file_path) and (any(filename.endswith(item) for item in extensions )):
				image_list.append(result_file_path)
    return image_list

def collectUserRating(csv_file):
	# collect user rating of webpages from csv file
	rating_list = {}
	with open(csv_file, 'rb') as csvfile:
		reader = csv.reader(csvfile)
		reader.next()
		i = 0
		for row in reader:
			image_name = str(row[1].strip())
			rating = row[79].strip()
			if not image_name in rating_list:
				rating_list[image_name] = [float(rating)]
			else:
				rating_list[image_name].append(float(rating))
	return rating_list
	
def generateListAll():
	# get webpage rating list, per image name as dict key, all user rating as values
	rate_file = '.\\data\\ae_only_unambiguous_1000.csv'
	rating_list = collectUserRating(rate_file)
	
	result_folder = '.\\results\\'
	if not os.path.exists(result_folder):
		os.mkdir(result_folder)

	# get webpage image list
	img_folder = '.\\data\\'
	extensions = ['png']
	image_list = walkDirWithExensions(img_folder, extensions)
	rated_image_list = []
	for image in image_list:
		csv_key = image.split('\\')[-2] + '_' + image.split('\\')[-1].split('.')[0]
		if csv_key in rating_list:
			rated_image_list.append(image)

	shuffle(rated_image_list) # to random shuffle the whole dataset
	train_list = rated_image_list[0:360]
	valid_list = rated_image_list[360:300]
	test_list = rated_image_list[300:398]

	with open(os.path.join(result_folder, 'train_list.txt'), 'w') as f:
		for image in train_list:
			csv_key = image.split('\\')[-2] + '_' + image.split('\\')[-1].split('.')[0]
			if csv_key in rating_list:
				for rating in rating_list[csv_key]:
					dummy = rating / 0.5 # to deal with *.5 rating cases, since caffe requires integer labels
					if dummy%2 == 0:
						f.write(image.split('\\')[-2] + '\\' + image.split('\\')[-1])
						f.write(' ' + str(int(rating)))
						f.write('\n')
					else:
						rng = np.random.RandomState(12345)
						ratio = int(np.random.randint(2, size=1))
						f.write(image.split('\\')[-2] + '\\' + image.split('\\')[-1])
						f.write(' ' + str(int(rating)+1*ratio))
						f.write('\n')
					
	with open(os.path.join(result_folder, 'valid_list.txt'), 'w') as f:
		for image in valid_list:
			csv_key = image.split('\\')[-2] + '_' + image.split('\\')[-1].split('.')[0]
			if csv_key in rating_list:
				f.write(image.split('\\')[-2] + '\\' + image.split('\\')[-1])
				f.write(' ' + str(int(np.round(np.mean(rating_list[csv_key])))))
				f.write('\n')
	
	with open(os.path.join(result_folder, 'test_list_eva.txt'), 'w') as f:
		for image in test_list:
			csv_key = image.split('\\')[-2] + '_' + image.split('\\')[-1].split('.')[0]
			if csv_key in rating_list:
				f.write(image.split('\\')[-2] + '\\' + image.split('\\')[-1])
				f.write(' ' + str(np.round(np.mean(rating_list[csv_key]),2)))
				f.write('\n')
				
	with open(os.path.join(result_folder, 'test_list.txt'), 'w') as f:
		for image in test_list:
			csv_key = image.split('\\')[-2] + '_' + image.split('\\')[-1].split('.')[0]
			if csv_key in rating_list:
				f.write(image.split('\\')[-2] + '\\' + image.split('\\')[-1])
				f.write(' ' + str(int(np.round(np.mean(rating_list[csv_key])))))
				f.write('\n')

if __name__ == "__main__":
	try:
		# To random generate training, validation and test dataset
		generateListAll()
	except KeyboardInterrupt:
		sys.exit(0)
