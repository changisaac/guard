from bag_compress_and_archive import BagArchiver
import os

data_directory = "/home/tamim/data/"
ignored_directories = "list.txt"

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

def archive_data(list_of_directories, bagArchiver):
	for directory in list_of_directories:
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

		print "CURRENT DIRECTORY: ", os.path.abspath(os.getcwd())

		# Compresse dataset and move to /compressed directory
		bagArchiver.compress()


		print "MOVING COMPRESSED FILES INTO: ", bagArchiver.archive_directory
		# Archive dataset and move to /archive/dataset# directory
		bagArchiver.archive(subdirectory='/%s' % directory)

	# End by going back to the main data directory
	os.chdir(data_directory)

def main():
	# user, directory, archive_directory, unarchive_directory= collectArguments()
	user = "tamim"
	archive_directory = "/home/tamim/data/archive"
	unarchive_directory = "/home/tamim/data/unarchive"

	bagArchiver = BagArchiver(user=user, directory=data_directory, archive_directory=archive_directory, 
							   unarchive_directory=unarchive_directory)
	
	list_of_directories = []
	list_of_uploads = []
	list_of_directories, list_of_uploads = collect_directories(list_of_directories, list_of_uploads)

	print "Beginning archiving process...: "
	bagArchiver.create_directory(archive_directory)
	bagArchiver.create_directory(unarchive_directory)

	archive_data(list_of_directories, bagArchiver)

if __name__ == '__main__':
	main()