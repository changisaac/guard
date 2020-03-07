from bag_compress_and_archive import BagArchiver
import os
import boto3

data_directory = "/home/forest/data/"
ignored_directories = "list.txt"
to_upload_directories = "to_upload.txt"

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

def upload_data(s3, user, files_to_upload, paths_to_read, dir_tracker):
	with open(dir_tracker) as f:
		for line in f:
			paths_to_read.append(line.rstrip()) 

	for path in paths_to_read:
		print "PATH", path
		for root, dirs, files in os.walk(path):
			files_to_upload.append(files)

		print "FILES TO UPLOAD", files_to_upload

		file_to_upload = files_to_upload[0][0]

		print "FILE TO UPLOAD: ", file_to_upload

		path_and_file = path + '/' + file_to_upload
		print "PATH AND FILE: ", path_and_file
		
		os.chdir(path)

		files_to_upload = []

        try:
            s3.meta.client.upload_file(path_and_file, forestai, ('rawdata/' + user + '/' + file_to_upload))
           
            print "UPLOADED SUCCESSFULLY!" 
            # If upload is successful, then we want to remove this from the 
            # list of files to upload. We also want to add the directory to list.txt
            with open(dir_tracker, 'r+') as f:
                lines = f.readlines()
                for line in lines:
                    if line.rstrip() != path:
                        f.write(line) 
                f.truncate()
        except:
            print "UNABLE TO UPLOAD FILE" % path_and_file

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
	
	# with open(to_upload_directories, "r+") as to_upload:
	#	archive_folders(list_of_directories, bagArchiver, file_tracker=to_upload)

	# List objects
	# client = boto3.client('s3')  
	# for key in client.list_objects(Bucket=forestai)['Contents']:
	# 	print(key['Key'])

	s3 = boto3.resource('s3')
	
	upload_data(s3, user, files_to_upload, paths_to_read, to_upload_directories)	



if __name__ == '__main__':
	main()
