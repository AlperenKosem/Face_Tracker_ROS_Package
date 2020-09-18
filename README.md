# Face Tracker ROS Package

This project aims to track face on 1 axis using rosserial_arduino package.

## Package

This package has following nodes.
- cam_ros
- face_detector
- serial_node

## Nodes

### cam_ros
#### Overview:<br>
`cam_ros` converts opencv images to sensor_msgs/Image format 

#### Published Topics

|topic| type |
|----------|-----|
|`/camera/image`|*sensor_msgs/Image*|

### face_detector
#### Overview:<br>
`face_detector` detects x location of face and calculates servo input to keep the face in the middle of image.

#### Subscribed Topics
|topic| type |
|----------|-----|
|`/camera/image`|*sensor_msgs/Image*|

#### Published Topics

|topic| type |
|----------|-----|
|`/servo_controller`|*std_msgs/Int16*|

### serial_node
#### Overview:<br>
`serial_node` provides communication between servo_controller topic and arduino.

#### Subscribed Topics

|topic| type |
|----------|-----|
|`/servo_controller`|*std_msgs/Int16*|








