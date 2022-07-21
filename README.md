# Line_Following
This Package can be used to make a PlutoX drone follow a path

## Connecting PlutoX
Run package
```
# To get data from drone
rosrun plutoserver data_via_rosservice.py

# plutonode for communication with drone
rosrun plutodrone plutonode

# To receive camera feed from drone
rosrun pluto_camera_sense plutocamera

#To display the live feed from drone
rosrun pluto_image_sun imagepronode

#For line detection from the receiving frames
Run Untitled-1.py in python IDE

```
** Note: For autonomous flight replace 'key_command.py' by 'drone_command.py' in the 'drone_comb.lauch' file
```
#For autonomous flight
roslauch plutoserver drone_comb.launch
```

