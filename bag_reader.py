import rosbag, sys, csv
import time
import string
import cv
import os #for file management make directory
import shutil #for file management, copy file
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

count = 0
print 'Reading Bag File'
bag = rosbag.Bag(sys.argv[1])
bagName = bag.filename
folder = string.rstrip(bagName, ".bag")
print 'Creating output directory'
try:	#else already exists
	os.makedirs(folder)
except:
	pass
try:	#else already exists
	os.makedirs(folder+"/camera")
except:
	pass
      
print 'Extracting IMU data'
filename = folder + '/imu.dat'
start_rec = False
with open(filename, 'w') as csvfile:
	filewriter = csv.writer(csvfile, delimiter = ',')
	timestr = ["timestamp","orientation.x","orientation.y","orientation.z","angular_velocity.x","angular_velocity.y","angular_velocity.z","linear_acceleration.x","linear_acceleration.y","linear_acceleration.z"]
	filewriter.writerow(timestr)
	for topic, msg, t in bag.read_messages(topics=['/imu3dmgx3/imu/data']):
		timestr = ["%.6f" % msg.header.stamp.to_sec()]
		timestr += [str(msg.orientation.x)]
		timestr += [str(msg.orientation.y)]
		timestr += [str(msg.orientation.z)]
		timestr += [str(msg.angular_velocity.x)]
		timestr += [str(msg.angular_velocity.y)]
		timestr += [str(msg.angular_velocity.z)]
		timestr += [str(msg.linear_acceleration.x)]
		timestr += [str(msg.linear_acceleration.y)]
		timestr += [str(msg.linear_acceleration.z)]
		
		filewriter.writerow(timestr)
		count = count + 1
		
print 'IMU Data count ' + str(count)
count = 0

print 'Extracting GPS data'
filename = folder + '/gps.dat'
start_rec = False
with open(filename, 'w') as csvfile:
	filewriter = csv.writer(csvfile, delimiter = ',')
	timestr = ["timestamp","latitude","longitude"]
	filewriter.writerow(timestr)
	for topic, msg, t in bag.read_messages(topics=['/imu3dmgx3/nav/fix']):
		timestr = ["%.6f" % msg.header.stamp.to_sec()]
		timestr += [str(msg.latitude)]
		timestr += [str(msg.longitude)]
		filewriter.writerow(timestr)
		count = count + 1
		
print 'GPS Data count ' + str(count)
#print 'Copying Bag File to Output directory'
#shutil.copyfile(bagName, folder + '/' + bagName)
count = 0

print 'Extracting LIDAR data'
filename = folder + '/laser.csv'
start_rec = False
with open(filename, 'w') as csvfile:
	filewriter = csv.writer(csvfile, delimiter = ',')
	for topic, msg, t in bag.read_messages(topics=['/scan']):
		timestr = ["%.6f" % msg.header.stamp.to_sec()]
		timestr += string.replace(string.replace(str(msg.ranges),')',''),'(','').split(',')
		filewriter.writerow(timestr)
		count = count + 1
		
print 'LIDAR Scan count ' + str(count)
count = 0

print 'Extracting Images data'
bridge = CvBridge()
for topic, msg, t in bag.read_messages(topics=['/PTZ/image_raw']):
	#newfile = open(folder + "/" + str(t)+".bmp","wb")
	try:
		cv_image = bridge.imgmsg_to_cv(msg, "bgr8")
	except CvBridgeError, e:
		print e
	timestr = "%.6f" % msg.header.stamp.to_sec()
	image_name = str(folder)+"/camera/"+timestr+".jpg"
	
	cv.SaveImage(image_name, cv_image)
	count  = count +1 
print 'Images count ' + str(count)
bag.close()
