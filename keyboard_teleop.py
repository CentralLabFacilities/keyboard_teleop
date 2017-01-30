#!/usr/bin/env python
import roslib; roslib.load_manifest('keyboard_teleop')
import rospy

from geometry_msgs.msg import Twist

import sys, select, termios, tty

msg = """
Reading from the keyboard  and Publishing to Twist!
---------------------------
Moving around:
   q    w    e
   a    s    d

+/- : increase/decrease max speeds by 10%

stop and reset velocities : space
anything else : stop

CTRL-C to quit
"""

SPEED_DEFAULT = 0.08
TURN_DEFAULT = 0.3

moveBindings = {
 		'w':(1,0,0,0),
                's':(-1,0,0,0),
		'q':(0,0,0,1),
		'e':(0,0,0,-1),
		'a':(0,1,0,0),
		'd':(0,-1,0,0),
	       }

speedBindings={
		'+':(1.1,1.1),
		'-':(.9,.9),
	      }

def getKey():
	tty.setraw(sys.stdin.fileno())
	select.select([sys.stdin], [], [], 0)
	key = sys.stdin.read(1)
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
	return key


def vels(speed,turn):
	return "currently:\tspeed %s\tturn %s " % (speed,turn)

if __name__=="__main__":
    	settings = termios.tcgetattr(sys.stdin)

	pub = rospy.Publisher('cmd_vel', Twist, queue_size = 1)
	rospy.init_node('keyboard_teleop')

	speed = rospy.get_param("~speed", SPEED_DEFAULT)
	turn = rospy.get_param("~turn", TURN_DEFAULT)
	x = 0
	y = 0
	z = 0
	th = 0
	status = 0

	try:
		print msg
		print vels(speed,turn)
		while(1):
			key = getKey()
			if key in moveBindings.keys():
				x = moveBindings[key][0]
				y = moveBindings[key][1]
				z = moveBindings[key][2]
				th = moveBindings[key][3]
			elif key in speedBindings.keys():
				speed = speed * speedBindings[key][0]
				turn = turn * speedBindings[key][1]

				print vels(speed,turn)
				if (status == 14):
					print msg
				status = (status + 1) % 15
	                elif key == ' ':
				print "resetting ..."

                		x = 0
                		y = 0
                		z = 0
                		th = 0

                		speed = SPEED_DEFAULT
                		turn = TURN_DEFAULT

                		print vels(speed,turn)
				if (status == 14):
					print msg
				status = (status + 1) % 15
			else:
				x = 0
				y = 0
				z = 0
				th = 0

				if (key == '\x03'):
					break

			twist = Twist()
			twist.linear.x = x*speed; twist.linear.y = y*speed; twist.linear.z = z*speed;
			twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = th*turn
			pub.publish(twist)

	except:
		print e

	finally:
		twist = Twist()
		twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
		twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
		pub.publish(twist)

    		termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
