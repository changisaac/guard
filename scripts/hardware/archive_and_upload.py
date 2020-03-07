from bag_compress_and_archive import BagArchiver
import os
import boto3

data_directory = "/home/tamim/data/"
ignored_directories = "uploaded_datasets.txt"
to_upload_directories = "datasets_to_upload.txt"

forestai = 'forestai-guard'

def collectArguments():
	parser = argparse.ArgumentParser(description='Compress and archive bag files')
	parser.add_argument('--user', '-u', default='default', help='Name to append on archive')
	parser.add_argument('--directory', '-d', default=default_bag_directory,
						help='Absolute path of directory where bag files are stored')
	parser.add_argument('--archive', '-a', default=default_archive_directory,
		                help='Absolute path of directory where archives should be stored')
	parser.add_argument('--unarchive', '-n', default=default_unarchive_directory,
		                help='Absolute path of directory where unarchived files should be stored')
	args = parser.parse_args()

	return args.user, args.directory, args.archive, args.unarchive

def collect_directories(list_of_directories, list_of_uploads):
	os.chdir(data_directory)
	for root, dirs, files in os.walk(data_directory):
		list_of_directories.append(dirs)

	# for some reason the above creates a list inside a list with empty
	# elements. We only want the first element which contains the directory names
	list_of_directories = list_of_directories[0]

	with open(ignored_directories) as f:
		for line in f:
			list_of_uploads.append(line.rstrip()) 

	print "LIST OF UPLOADS: ", list_of_uploads

	# Remove the directories that are already uploaded
	for upload in list_of_uploads:
		if upload in list_of_directories:
			list_of_directories.remove(upload)

	print "NEW LIST OF DIRECTORIES:", list_of_directories

	return list_of_directories, list_of_uploads

def archive_data(directory, bagArchiver, file_tracker=None):
	# Go to archive to create a location to move the tar file
	print "DIRECTORY TO ARCHIVE: ", directory

	os.chdir(bagArchiver.archive_directory)
	bagArchiver.create_directory(directory)

	# Go back to the data direcotry
	os.chdir(data_directory)

	print "CURRENT DIRECTORY: ", os.path.abspath(os.getcwd())

	# Change the bag directory to be where the dataset is stored. This will also
	# Create a directory to store the compressed files
	bagArchiver.change_bag_directory(data_directory + directory)
	bagArchiver.change_compressed_bag_directory(bagArchiver.directory + '/compressed')

	# Go into dataset directory
	os.chdir(bagArchiver.directory)
	archive_directory = os.path.abspath(os.getcwd())
	print "CURRENT DIRECTORY: ", archive_directory

	# Compresse dataset and move to /compressed directory
	bagArchiver.compress()

	print "MOVING COMPRESSED FILES INTO: ", bagArchiver.archive_directory
	# Archive dataset and move to /archive/dataset# directory
	bagArchiver.archive(subdirectory='/%s' % directory)	

	if file_tracker is not None:
		print "Saving to file file_tracker"
		file_tracker.write(bagArchiver.archive_directory + '/' + directory + '\n')
		file_tracker.flush()

	# End by going back to the main data directory
	os.chdir(data_directory)

def archive_folders(list_of_directories, bagArchiver, file_tracker=None):
	for directory in list_of_directories:
		print file_tracker
		archive_data(directory, bagArchiver, file_tracker=file_tracker)

def upload_data(s3, user, files_to_upload, paths_to_read, file_upload_tracker):
	lines_to_erase = []
	with open(file_upload_tracker) as f:
		for line in f:
			paths_to_read.append(line.rstrip()) 

	for path in paths_to_read:
		print "PATH", path
		for root, dirs, files in os.walk(path):
			files_to_upload.append(files)

		# Manipulate the strings to get the path of the tar.gz file
		print "FILES TO UPLOAD", files_to_upload

		file_to_upload = files_to_upload[0][0]

		print "FILE TO UPLOAD: ", file_to_upload

		path_and_file = path + '/' + file_to_upload
		print "PATH AND FILE: ", path_and_file
		
		try:
			s3.meta.client.upload_file(path_and_file, forestai, ('rawdata/' + user + '/' + file_to_upload))
			print "UPLOADED SUCCESSFULLY!" 
			lines_to_erase.append(path)
		except:
			pass

		files_to_upload = []

	print "LINES TO ERASE: ", lines_to_erase

	update_file_trackers(lines_to_erase, file_archive_tracker=ignored_directories, 
						file_upload_tracker=file_upload_tracker)
	

def update_file_trackers(lines_to_update, file_archive_tracker=None, file_upload_tracker=None):
	if file_upload_tracker is not None:
		# Open in read + write mode to replace lines
		with open(file_upload_tracker, 'r+') as f:
			f.seek(0)
			lines = f.readlines()
			for line in lines:
				if line.rstrip() in lines_to_update:
					f.write('')
			f.truncate(0)

	if file_archive_tracker is not None:
		# Open in append mode to add on to the end
		with open(file_archive_tracker, 'a') as f:
			for line in lines_to_update:
				line = os.path.basename(os.path.normpath(line))
				f.write(line + '\n')

def main():
	# user, directory, archive_directory, unarchive_directory = collectArguments()
	user = "tamim"
	archive_directory = data_directory + "archive"
	unarchive_directory = data_directory + "unarchive"
	bagArchiver = BagArchiver(user=user, directory=data_directory, archive_directory=archive_directory, 
							   unarchive_directory=unarchive_directory)
	
	list_of_directories = []
	list_of_uploads = []
	files_to_upload = []
	paths_to_read = []
	list_of_directories, list_of_uploads = collect_directories(list_of_directories, list_of_uploads)

	print "Beginning archiving process...: "
	bagArchiver.create_directory(archive_directory)
	bagArchiver.create_directory(unarchive_directory)

	os.chdir(data_directory)
	
	with open(to_upload_directories, "r+") as to_upload:
		archive_folders(list_of_directories, bagArchiver, file_tracker=to_upload)

	print "Beginning uploading process...:"

	s3 = boto3.resource('s3')
	upload_data(s3, user, files_to_upload, paths_to_read, to_upload_directories)	

if __name__ == '__main__':
	main()