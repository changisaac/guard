import rosbag
import os
import subprocess as sp 
from time import gmtime, strftime

bag_directory = "/home/tamim/bagfiles/"
compressed_bag_directory = "/home/tamim/bagfiles/compressed"

# Need to make this one a string, presumably because 
# shell=True for this command
cmd_compress = "rosbag compress --output-dir=%s *.bag" % compressed_bag_directory 
cmd_archive = (["tar", "cfv", "ros_bags_%s.tar"])

# print "CHANGING DIRECTORY TO: %s" % bag_directory

print "CMD: ", cmd_compress
try:
	os.chdir(bag_directory)
	sp.call("ls")
	print "COMPRESSING BAG FILES"
	sp.call(cmd_compress, shell=True)
except:
	print "FAILED"

print "COMPRESSION COMPLETE"

cmd_archive[2] = cmd_archive[2] % strftime("%Y-%m-%d_%H_%M_%S", gmtime())

for filename in os.listdir(compressed_bag_directory):
    if filename.endswith(".bag"):
        cmd_archive.append(filename)

print "CMD: ", cmd_archive
print "ARCHIVING INTO: %s" % cmd_archive[2]
sp.call(cmd_archive)