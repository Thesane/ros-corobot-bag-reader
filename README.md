ros-corobot-bag-reader
======================

- simple python script to read bag file recorded from rosbag and extract information in portable format
- extract Webcam pictures from corobot_camera (frame rate is adjustable from corobot launch file) and create a folder with all extracted images
- extract gps data published by Microstrain 3DM-GX3-45 INS and generate csv file with extracted data
- extract imu data published by Microstrain 3DM-GX3-45 INS and generate csv file with extracted data
- extract lidar reading published by Hokuyo UTM-30LX lidar and generate csv file with extracted data
- print out number of reading for each topic
