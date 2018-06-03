from point import Point,GeometryError

import math


class Rectangle(object):
	
	def __init__(self, Top_Left,Bottom_Right):
		super(Rectangle, self).__init__()
		try:
			assert(type(Top_Left) == Point)
			assert(type(Bottom_Right) == Point)
		except AssertionError:
			raise GeometryError('Need two arguments of type Point to create a Rectangle Object.')

		self.tl = Top_Left
		self.br = Bottom_Right


	def opposite(self):
		self.tl.opposite()
		self.br.opposite()


	def center(self):
		return Point((self.tl.x+self.br.x)/2,(self.tl.y+self.br.y)/2)


	def distance(self,R):
		try:
			assert(type(R) == Rectangle)
		except AssertionError:
			raise GeometryError('This method need a Rectangle as argument.')

		return self.center().distance(R.center())


	def zoom(self,factor):
		try:
			factor = float(factor)
		except AssertionError:
			raise GeometryError('This method need a float as argument.')
		
		self.tl.x,self.tl.y = [factor*self.tl.x,factor*self.tl.y]
		self.br.x,self.br.y = [factor*self.br.x,factor*self.br.y]


	def rotate(self,center,angle):
		return Rectangle(self.tl.rotate(center,angle),self.br.rotate(center,angle))


	def aligned(self,R1,R2):
		try:
			assert(type(R1) == Rectangle)
			assert(type(R2) == Rectangle)
		except AssertionError:
			raise GeometryError('Needs two Rectangle Objects as arguments.')

		return self.center().aligned(R1.center(),R2.center())


	def __repr__(self):
		return '['+self.tl.__repr__()+','+self.br.__repr__()+']'




##################################
#			TESTS                #
##################################
if __name__ == '__main__':

	P0 = Point(0,0)
	P1 = Point(1,1)
	P2 = Point(1,1)
	P3 = Point(0.5,0.5)
	P4 = Point(-0.5,-0.5)
	P5 = Point(-1,1)

	R1 = Rectangle(P0,P1)
	R2 = Rectangle(P0,P2)
	R3 = Rectangle(P3,P4)
	R4 = Rectangle(P0,P5)

	R2.opposite()
	print('opposite method test:')
	print(R2.br.x == -1,R2.br.y == -1,R2.tl.x == 0,R2.tl.y == 0)

	dist = R1.distance(R2)
	print('distance method test:')
	print(abs(dist-math.sqrt(2)) < 10e-10)

	print(R4)
	new_rect = R4.rotate(P0,math.pi)
	print(new_rect)
	print('rotation method test:')
	print(abs(new_rect.tl.x)<10e-10,abs(new_rect.tl.y)<10e-10)
	print(abs(new_rect.br.x-1)<10e-10,abs(new_rect.br.y+1)<10e-10)

	alg1 = R1.aligned(R2,R3)
	print('aligned method test 1:')
	print(alg1 == True)

	alg1 = R1.aligned(R2,R4)
	print('aligned method test 1:')
	print(alg1 == False)

