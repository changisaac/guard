from bag_compress_and_archive import BagArchiver
import os
import boto3
import botocore

data_directory = "/home/tamim/data/"
ignored_directories = "uploaded_datasets.txt"
to_upload_directories = "datasets_to_upload.txt"
forestai = 'forestai-guard'
local_copy_location = "/home/tamim/data/download/"

def download(s3, filename, downloadname, file_tracker=None):
	try:
		file = os.path.basename(os.path.normpath(filename))
		downloadname = filename.split(file)[0]
		# TODO: Change 'test' to the first subdirectory in bucket
		downloadpath = downloadname.split('test/')[1]
		if not os.path.exists(local_copy_location + downloadpath):
			os.makedirs(local_copy_location + downloadpath)
		full_download_path = local_copy_location + downloadpath

		print "Downloading file from %s" % filename
		print "Downloading file to %s" % full_download_path
		s3.Bucket(forestai).download_file(filename, full_download_path + '/' + file)

		if file_tracker is not None:
			file_tracker.write(full_download_path + file + '\n')
	except botocore.exceptions.ClientError as e:
	    if e.response['Error']['Code'] == "404":
	        print("The object does not exist.")
	    else:
	        raise

def download_data(s3, list_of_s3_locations, file_tracker=None):
	for list in list_of_s3_locations:
		for filename in list:
			download(s3, filename, local_copy_location, file_tracker=file_tracker)

def start_download(list_of_s3_locations):
	s3 = boto3.resource('s3')
	# archive_directory = data_directory + "archive"
	# unarchive_directory = data_directory + "unarchive"
	# bagArchiver = BagArchiver(user=user, directory=data_directory, archive_directory=archive_directory, 
	# 						   unarchive_directory=unarchive_directory)
	
	list_of_s3_locations = [['test/user1/1583536661790281234/0.jpg', 'test/user1/1583536661790281234/1.jpg']]

	os.chdir(local_copy_location)
	if os.path.isfile('downloaded_files.txt'):
		print "File exists...!"
	else:
	    print "File does not exist"
	    open('downloaded_files.txt', 'a').close()
	    print "Created file %s" % 'downloaded_files'
	
	with open('downloaded_files.txt', 'a') as f:
		download_data(s3, list_of_s3_locations, file_tracker=f)

def main():
	# user, directory, archive_directory, unarchive_directory = collectArguments()
	print "HI"
	
	# format of directory: processed/user1/ts/*.jpegs

	# download the images, then tar, and then reupload into 

	# give me 2D array, list of locations of s3 

	# zip them up together 

	# how am I going to receive the 2D list? return the lines of jpegs, send second post req - the actual query
	# line1, 2 and 3 -> 






if __name__ == '__main__':
	main()