# keyboard_teleop
Generic Keyboard Teleop for ROS
#Launch
To run: `rosrun keyboard_teleop keyboard_teleop.py`

#With custom values
`rosrun keyboard_teleop keyboard_teleop.py _topic:=test_topic _speed:=0.9 _turn:=0.8`

#Usage
```
Reading from the keyboard  and Publishing to Twist!
---------------------------
Moving around:
   q    w    e
   a    s    d

+/- : increase/decrease max speeds by 10%

stop and reset velocities : space
anything else : stop

CTRL-C to quit
```
