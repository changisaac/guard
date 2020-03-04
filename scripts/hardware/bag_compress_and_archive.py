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

def collectArguments():
	parser = argparse.ArgumentParser(description='Compress and archive bag files')
	parser.add_argument('--user', '-u', default='default', help='Name to append on archive')
	parser.add_argument('--directory', '-d', default=default_bag_directory,
						help='Absolute path of directory where bag files are stored')
	parser.add_argument('--archive', '-a', default=default_archive_directory,
		                help='Absolute path of directory where archives should be stored')
	args = parser.parse_args()

	return args.user, args.directory, args.archive

def compress(directory, compressed_directory):
	try:
		os.chdir(directory)
		print "COMPRESSING BAG FILES"
		sp.call(cmd_compress % compressed_directory, shell=True)
	except:
		print "COMPRESSION FAILED"

	print "COMPRESSION COMPLETE"

def archive(user, directory, archive_directory):
	cmd_archive[CMD_FILE_IDX] = cmd_archive[CMD_FILE_IDX] % (user, strftime("%Y-%m-%d_%H_%M_%S", gmtime()))
	
	# Set the archive filename and directory it should be moved to
	cmd_mv_archive.append(cmd_archive[CMD_FILE_IDX])
	cmd_mv_archive.append(archive_directory)

	# Select all the files to archive
	os.chdir(directory)
	for filename in os.listdir(directory):
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

def main():
	user, directory, archive_directory = collectArguments()
	compressed_directory = directory + '/compressed'

	compress(directory, compressed_directory)
	archive(user, compressed_directory, archive_directory)

if __name__ == '__main__':
	main()