import rosbag
import os
import subprocess as sp 
from time import gmtime, strftime
import argparse

default_bag_directory = "/home/tamim/bagfiles/"
default_archive_directory = "/home/tamim/archive"
default_unarchive_directory = "/home/tamim/unarchive"

# Need to make this one a string, presumably 
# because shell=True for this command
cmd_compress = "rosbag compress --output-dir=%s *.bag" 
cmd_archive = (["tar", "czfv", "guard_user_%s_%s.tar.gz"])
cmd_decompress = "rosbag decompress --output-dir=decompressed *.bag"
cmd_unarchive = (["tar", "-xzvf"])
cmd_mv_archive = (["mv"])
cmd_mv_unarchive = (["cp"])

CMD_FILE_IDX = 2

class Bag_Archiver():
	def __init__(self, user="default", directory=default_bag_directory, 
				 archive_directory=default_archive_directory, unarchive_directory=default_unarchive_directory):
		self.user = user
		self.directory = directory
		self.archive_directory = archive_directory
		self.unarchive_directory = unarchive_directory
		self.compressed_directory = self.directory + '/compressed'

	def change_user(new_user):
		self.user = new_user

	def change_bag_directory(new_directory):
		self.directory = new_directory
		self.compressed_directory = self.directory + '/compressed'

	def change_archive_directory(new_archive_directory):
		self.archive_directory = new_archive_directory

	def change_unarchive_directory(new_unarchive_directory):
		self.unarchive_directory = new_unarchive_directory

	def find_directory(self, directory):
		if os.path.isfile(directory):
			return True
		return False
	
	def create_directory(self, directory):
		try:
			os.mkdir(directory)
		except OSError:
			print "Creation of directory %s failed" % directory
		else:
			print "Successfully created the directory %s " % directory
    
	def compress(self):
		try:
			os.chdir(self.directory)
			print "COMPRESSING BAG FILES"
			sp.call(cmd_compress % self.compressed_directory, shell=True)
		except:
			print "COMPRESSION FAILED"

		print "COMPRESSION COMPLETE"

	def archive(self):
		cmd_archive[CMD_FILE_IDX] = cmd_archive[CMD_FILE_IDX] % (self.user, strftime("%Y-%m-%d_%H_%M_%S", gmtime()))
	
		# Set the archive filename and directory it should be moved to
		cmd_mv_archive.append(cmd_archive[CMD_FILE_IDX])
		cmd_mv_archive.append(self.archive_directory)

		# Select all the files to archive
		os.chdir(self.compressed_directory)
		for filename in os.listdir(self.directory):
		    if filename.endswith('.bag'):
		        cmd_archive.append(filename)

		print "ARCHIVING INTO: %s" % cmd_archive[CMD_FILE_IDX]
		try: 
			sp.call(cmd_archive)
		except:
			print "ARCHIVE FAILED"

        # Move archive to archive folder
		try:
			sp.call(cmd_mv_archive)
			cmd_mv_unarchive = ["mv"]
		except:
			print "COULD NOT MOVE ARCHIVE"
    
	def unarchive(self, filename):
		# Go to archive directory for copying
		file_dir = filename.split('.')[0]
		os.chdir(self.archive_directory)
		# Move the file to unarchive location
		cmd_mv_unarchive.append(filename)
		cmd_mv_unarchive.append(self.unarchive_directory)

		try:
			sp.call(cmd_mv_unarchive)
		except:
			print "COULD NOT MOVE ARCHIVE"

		# Go to unarchive directory
		os.chdir(self.unarchive_directory)

		# Create a directory based on filename of the file
		if not self.find_directory(file_dir):
			print "DIRECTORY DOESNT EXIST"
			self.create_directory(file_dir)

		cmd_mv_unarchive[0] = "mv"
		cmd_mv_unarchive[CMD_FILE_IDX] = cmd_mv_unarchive[CMD_FILE_IDX] + '/' + file_dir

		# Move the archive to subdirectory with its name
		try:
			sp.call(cmd_mv_unarchive)
		except:
			print "COULD NOT MOVE ARCHIVE to /%s" % filename
		else:
			print "SUCCESSFULLY MOVED ARCHIVE to %s" % (self.unarchive_directory + "/" + file_dir)

		# Unarchive the file 
		try:
			print "UNARCHIVING FILE!"
			os.chdir(self.unarchive_directory + '/' + file_dir)
			cmd_unarchive.append(filename)
			sp.call(cmd_unarchive)
		except:
			print "COULD NOT UNARCHIVE"

	def decompress(self, directory=None):
		if directory is not None:
			os.chdir(directory)

		try:
			if not self.find_directory('decompressed'):
				self.create_directory('decompressed')
			print "DECOMPRESSING BAG FILES"
			sp.call(cmd_decompress, shell=True)
		except:
			print "DECOMPRESSION FAILED"
		print "DECOMPRESSION COMPLETE"

	def unarchive_and_decompress(self, filename):
		self.unarchive(filename)
		self.decompress()

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

def main():
	user, directory, archive_directory, unarchive_directory= collectArguments()
	bagArchiver = Bag_Archiver(user=user, directory=directory, archive_directory=archive_directory, 
							   unarchive_directory=unarchive_directory)
	# bagArchiver.compress()
	# bagArchiver.archive()

	bagArchiver.unarchive_and_decompress("guard_user_default_2020-03-05_04_45_01.tar.gz")

if __name__ == '__main__':
	main()