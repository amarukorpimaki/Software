#!/usr/bin/env python

import rospy #importar ros para python
from std_msgs.msg import String, Int32 # importar mensajes de ROS tipo String y tipo Int32
from geometry_msgs.msg import Twist # importar mensajes de ROS tipo geometry / Twist
from sensor_msgs.msg import Image # importar mensajes de ROS tipo Image
import cv2 # importar libreria opencv
from cv_bridge import CvBridge # importar convertidor de formato de imagenes
import numpy as np # importar libreria numpy
from geometry_msgs import Point


class Template(object):
	def __init__(self, args):
		super(Template, self).__init__()
		self.args = args
		self.subscriber=rospy.Subscriber("/duckiebot/camera_node/image/rect", Image,self.callback)
		self.publisher=rospy.Publisher("instagram", Image, queue_size=10)
		self.pub_equalizada=rospy.Publisher("equalizada", Image, queue_size=10)
		self.pub_imagen=rospy.Publisher("imagen", Image, queue_size=10)
		self.pub_point=rospy.publisher("Point", Point, queue_size=10)


	def callback(self,msg):
		bridge= CvBridge()
		image=bridge.imgmsg_to_cv2(msg,"bgr8")
		imageP= self.preprocesar_img(image)
		image0=self.procesar_img(imageP)
		
		msgI= bridge.cv2_to_imgmsg(image,"bgr8")
		self.pub_imagen.publish(msgI)

		msgP= bridge.cv2_to_imgmsg(imageP,"bgr8")
		self.pub_equalizada.publish(msgP)
		msg= bridge.cv2_to_imgmsg(image0,"bgr8")
		self.publisher.publish(msg)
		#cota1=np.array([10,140,140])
		#cota2=np.array([60,255,255])
		#batman=cv2.bitwaise_and(image_out,image_out,image=image)

	def preprocesar_img(self,img):
		b, g, r = cv2.split(img)
		red= cv2.equalizeHist(r)
		green= cv2.equalizeHist(g)
		blue= cv2.equalizeHist(b)
		return cv2.merge((blue, green, red))

		#image_out=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		#equ = cv2.equalizeHist(image_out)
		#image_out=cv2.cvtColor(equ, cv2.COLOR_GRAY2BGR)
		#return image_out
	def procesar_img(self, img):
		
		self.fx=165.1926389508671
		self.fy=167.42725035374085
		
		# Cambiar espacio de color
		image_out=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		# Filtrar rango util
		#cotas  y mscara
		mask= cv2.inRange(image_out,np.array([10,140,140]),np.array([60,255,255]))

		# Aplicar mascara
		#batman=cv2.bitwise_and(image_out,image_out,mask=mask)
		# Aplicar transformaciones morfologicas
		kernel = np.ones((5,5),np.uint8)
		img_out = cv2.erode(mask, kernel, iterations = 1)
		img_out = cv2.dilate(img_out, kernel, iterations = 1)	
		batman=cv2.bitwise_and(img_out,img_out,mask=mask)		
		# Definir blobs
		_,contours, hierarchy = cv2.findContours(img_out, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
		# Dibujar rectangulos de cada blob
		for cnt in contours:
			x,y,w,h = cv2.boundingRect(cnt) #obtener rectangulo
			if (w/h)< (3.7/3):
				cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2) #Dibujar rectangulo
		
			#calcular distancia al pato
			dz=(self.fx*3.9)/w
			dy=(self.fy*3.0)/h
			U= x+w/2
			V= y+h/2
			point=Point()
			point.x= ((U-165.66522940282505)/165.1926389508671)*dy
			point.y= ((V-120.29518828841765)/167.42725035374085)*dy
			point.z= dy
			self.pub_point.pubish(point)

		# Publicar imagen final

		return img


def main():
	rospy.init_node('test') #creacion y registro del nodo!

	obj = Template('args') # Crea un objeto del tipo Template, cuya definicion se encuentra arriba

	#objeto.publicar() #llama al metodo publicar del objeto obj de tipo Template

	rospy.spin() #funcion de ROS que evita que el programa termine -  se debe usar en  Subscribers


if __name__ =='__main__':
	main()
