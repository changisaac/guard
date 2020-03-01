- launch D435 first by serial number
- then launch D435i second by serial number
- use 5_11_11_100 firmware for each camera
- realsense-ros v2.2.8
- librealsense v2.28.1
- launch with 320x240 at 6Hz for less frame drops
- use `rs-enumerate-devices` to find valid fps and resolutions configs
- also use `rs-enumerate-devices` to find camera serial numbers

- For launching cameras:
    - `roslaunch realsense2_camera rs_camera.launch camera:=cam_1 serial_no:=<serial number of the first camera>`
    - `roslaunch realsense2_camera rs_camera.launch camera:=cam_2 serial_no:=<serial number of the second camera>`

Sources:
- https://github.com/IntelRealSense/realsense-ros
- https://dev.intelrealsense.com/docs/firmware-update-tool
- https://github.com/IntelRealSense/realsense-ros/issues/1051
    - shreyas2311 comment on Jan 13 for downgrade of realsense-ros and librealsense info
    - child issue: https://github.com/IntelRealSense/realsense-ros/issues/1002
- https://github.com/JetsonHacksNano/installLibrealsense
    - jetsonhacks tutorial and script for installing librealsense
    - modify `buildLibrealsense.sh` line 9 for version change
- realsense-ros version change
    - git clone <repo>
    - `git checkout 2.2.8`
    - catkin_make
- https://www.digitalocean.com/community/tutorials/how-to-add-swap-space-on-ubuntu-16-04
    - how to add swapspace if building runs out of memory
    - also close chrome for builds to save memory
