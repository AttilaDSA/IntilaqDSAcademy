import math
import numpy as np

class GeometryError(Exception):

	def __init__(self,*args,**kwargs):
		Exception.__init__(self)



class Point(object):
	
	def __init__(self,x,y):
		super(Point, self).__init__()
		try:
			self.x = float(x)
			self.y = float(y)
		except TypeError:
			raise GeometryError('Arguments type must be float,int or string')
		except ValueError:
			raise GeometryError('Need floats, ints or float-formatables strings to instanciate a point.')


	def opposite(self):
		self.x = -self.x
		self.y = -self.y


	def add(self,P):
		try:
			assert(type(P) == Point)
		except AssertionError:
			raise GeometryError("Argument must be an instance of class Point.")

		return Point(self.x+P.x,self.y+P.y)


	def __add__(self,P):
		return self.add(P)


	def distance(self,P):
		try:
			assert(type(P) == Point)
		except AssertionError:
			raise GeometryError("Argument must be an instance of class Point.")

		return math.sqrt((self.x-P.x)**2+(self.y-P.y)**2)


	def rotate(self,center,angle):
		try:
			assert(type(center) == Point)
			angle = float(angle)
		except AssertionError:
			raise GeometryError("Arguments must be an instance of class Point and a float.")

		x = self.x - center.x
		y = self.y - center.y
		return Point(
			center.x+x*np.cos(angle)-y*np.sin(angle),
			center.y+x*np.sin(angle)+y*np.cos(angle)
		)


	def aligned(self,P1,P2):
		try:
			assert(type(P1) == Point)
			assert(type(P1) == Point)
		except AssertionError:
			raise GeometryError('Needs two Point Objects as arguments.')

		try:
			assert((self.x != P1.x) or (self.y != P1.y))
			assert((self.x != P2.x) or (self.y != P2.y))
			assert((P2.x != P1.x) or (P2.y != P1.y))
		except AssertionError:
			return True

		x1 = P1.x-self.x
		x2 = P2.x-self.x
		y1 = P1.y-self.y
		y2 = P2.y-self.y

		# cos(OP1,x), cos(OP2,x), sin(OP1,x), sin(OP2,x)
		OP1 = math.sqrt(x1**2+y1**2)
		OP2 = math.sqrt(x2**2+y2**2)
		cos1 = x1/OP1
		cos2 = x2/OP2
		sin1 = y1/OP1
		sin2 = y2/OP2

		# Accuracy 10e-10
		return cos1*cos2+sin1*sin2+10e-10 > 1 or cos1*cos2+sin1*sin2-10e-10 < -1


	def __repr__(self):
		return '('+str(self.x)+','+str(self.y)+')'



##################################
#			TESTS                #
##################################
if __name__ == '__main__':

	P1 = Point(1,2)
	P2 = Point(1.0,3)
	P3 = Point('1.0',2)
	P4 = Point(0,'0')

	P5 = Point('P1',P2)

	P3.opposite()
	print('opposite method test:')
	print(P3.x == -1,P3.y == -2)

	new_pt = P4.add(P2)
	print('add method test:')
	print(new_pt.x == 1,new_pt.y == 3)

	new_pt = P4+P2
	print('__add__ method test:')
	print(new_pt.x == 1,new_pt.y == 3)

	dist = P1.distance(P4)
	print('distance method test:')
	print(abs(dist-math.sqrt(5)) < 10e-10)

	new_pt = Point(1,0).rotate(P4,math.pi/2)
	print('rotation method test:')
	print(abs(new_pt.x)<10e-10,abs(new_pt.y-1)<10e-10)

	alg1 = P4.aligned(P1,P3)
	print('aligned method test 1:')
	print(alg1)

	alg1 = P4.aligned(P1,P2)
	print('aligned method test 1:')
	print(alg1)

