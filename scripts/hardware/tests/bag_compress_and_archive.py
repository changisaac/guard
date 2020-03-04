import rosbag
import os
import subprocess as sp 
from time import gmtime, strftime
import argparse

default_bag_directory = "/home/tamim/bagfiles/"

# Need to make this one a string, presumably 
# because shell=True for this command
cmd_compress = "rosbag compress --output-dir=%s *.bag" 
cmd_archive = (["tar", "cfv", "guard_user_%s_%s.tar"])

def compress(directory, compressed_directory):
	print "CMD: ", cmd_compress
	try:
		print "CHANGING TO DIRECTORY %s" % directory
		os.chdir(directory)
		sp.call("ls")
		print "COMPRESSING BAG FILES"
		sp.call(cmd_compress % compressed_directory, shell=True)
	except:
		print "COMPRESSION FAILED"

	print "COMPRESSION COMPLETE"

def archive(user, directory):
	cmd_archive[2] = cmd_archive[2] % (user, strftime("%Y-%m-%d_%H_%M_%S", gmtime()))

	os.chdir(directory)
	sp.call("ls")
	for filename in os.listdir(directory):
	    if filename.endswith('.bag'):
	        cmd_archive.append(filename)

	print "ARCHIVING INTO: %s" % cmd_archive[2]
	try: 
		sp.call(cmd_archive)
	except:
		print "ARCHIVE FAILED"

def collectArguments():
	parser = argparse.ArgumentParser(description='Compress and archive bag files')
	parser.add_argument('--user', '-u', default='default', help='Name to append on archive')
	parser.add_argument('--directory', '-d', default=default_bag_directory,
						help='Absolute path of directory where bag files are stored')
	args = parser.parse_args()

	return args.user, args.directory

def main():
	user, directory = collectArguments()
	compressed_directory = directory + '/compressed'
	
	compress(directory, compressed_directory)
	archive(user, compressed_directory)

if __name__ == '__main__':
	main()
