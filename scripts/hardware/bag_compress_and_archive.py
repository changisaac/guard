import rosbag
import os
import subprocess as sp 
from time import gmtime, strftime
import argparse

default_bag_directory = "/home/tamim/bagfiles/"
default_archive_directory = "/home/tamim/archive"

# Need to make this one a string, presumably 
# because shell=True for this command
cmd_compress = "rosbag compress --output-dir=%s *.bag" 
cmd_archive = (["tar", "cfv", "guard_user_%s_%s.tar"])
cmd_mv_archive = (["mv"])

CMD_FILE_IDX = 2

class Bag_Archiver():
	def __init__(self, user="default", directory=default_bag_directory, 
				 archive_directory=default_archive_directory):
		self.user = user
		self.directory = directory
		self.archive_directory = archive_directory
		self.compressed_directory = self.directory + '/compressed'

	def change_user(new_user):
		self.user = new_user

	def change_directory(new_directory):
		self.directory = new_directory
		self.compressed_directory = self.directory + '/compressed'

	def change_archive_directory(new_archive_directory):
		self.archive_directory = new_archive_directory

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

		print "ARCHIVING INTO: %s" % cmd_archive[2]
		try: 
			sp.call(cmd_archive)
		except:
			print "ARCHIVE FAILED"

		# Move archive to archive folder
		try:
			sp.call(cmd_mv_archive)
		except:
			print "COULD NOT MOVE ARCHIVE"

def collectArguments():
	parser = argparse.ArgumentParser(description='Compress and archive bag files')
	parser.add_argument('--user', '-u', default='default', help='Name to append on archive')
	parser.add_argument('--directory', '-d', default=default_bag_directory,
						help='Absolute path of directory where bag files are stored')
	parser.add_argument('--archive', '-a', default=default_archive_directory,
		                help='Absolute path of directory where archives should be stored')
	args = parser.parse_args()

	return args.user, args.directory, args.archive

def main():
	user, directory, archive_directory = collectArguments()
	bagArchiver = Bag_Archiver(user=user, directory=directory, archive_directory=archive_directory)

	bagArchiver.compress()
	bagArchiver.archive()
	
if __name__ == '__main__':
	main()