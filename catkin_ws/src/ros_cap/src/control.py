#!/usr/bin/env python

import rospy #importar ros para python
from std_msgs.msg import String, Int32 # importar mensajes de ROS tipo String y tipo Int32
from geometry_msgs.msg import Twist # importar mensajes de ROS tipo geometry / Twist
from sensor_msgs.msg import Joy
from duckietown_msgs.msg import Twist2DStamped



class Control(object):
	def __init__(self, args):
		super(Control, self).__init__()
		self.args = args
		self.subscriber=rospy.Subscriber("/duckiebot/joy", Joy,self.callback)
		self.publisher=rospy.Publisher("/duckiebot/wheels_driver_node/car_cmd", Twist2DStamped, queue_size=10)



	def callback(self,msg):
		rospy.loginfo(msg.axes)
		#cmd2=Twist2DStamped()
		cmd=Twist2DStamped()
		cmd.v=-2* msg.axes[1]
		cmd.omega=8*msg.axes[0]
		panico=msg.buttons[0]
		#if  cmd.v>= 0.4 or cmd.v<=-0.4:
		#self.publisher.publish(cmd)
		#else:
			#cmd.v=0
			#cmd.omega=0
			#self.publisher.publish(cmd)
		#if  cmd.omega>= 0.16 or cmd.omega<=-0.16:
			#self.publisher.publish(cmd) 
		if panico==1:
			cmd.v=0.0 
			cmd.omega=0.0
		self.publisher.publish(cmd)
		


def main():
	rospy.init_node('test') #creacion y registro del nodo!

	obj = Control('args') # Crea un objeto del tipo Template, cuya definicion se encuentra arriba

	#objeto.publicar() #llama al metodo publicar del objeto obj de tipo Template

	rospy.spin() #funcion de ROS que evita que el programa termine -  se debe usar en  Subscribers


if __name__ =='__main__':
	main()
