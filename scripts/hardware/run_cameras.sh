#!/bin/bash -e 
echo "The following are the Serial numbers for each camera (Serial Number is the one you want not Asic Serial Number)"
echo $(rs-enumerate-devices | grep Serial)

#Camera 1----------------------------------
echo "Starting camera 1 (should be d435 check launch serial above to confirm if needed)"
roslaunch realsense2_camera rs_camera.launch camera:=cam_1 serial_no:=944122074304 &
echo "pid of camera 1" + "$!"
camera_1_pid=$!

echo "Waiting 30 seconds for camera 1 to start up..."
sleep 30
echo "Camera 1 should be up"
#Camera 1----------------------------------

#Camera 2----------------------------------
echo "Starting camera 2 (should be d435i check launch serial above to confirm if needed)"
roslaunch realsense2_camera rs_camera.launch camera:=cam_2 serial_no:=939622070897 &
echo "pid of camera 2" + "$!"
camera_2_pid=$!

echo "Waiting 30 seconds for camera 2 to start up..."
sleep 30
echo "Camera 2 should be up"
#Camera 2----------------------------------

#Camera 3----------------------------------
#TODO
#Camera 3----------------------------------

function cleanup {
    echo "Ending Camera processes"
    kill $camera_1_pid
    kill $camera_2_pid
}

echo "Sleeping to allow cameras to run"
sleep infinity

trap cleanup EXIT

