from point import Point,GeometryError



class Polygone(object):

	def __init__(self, points):
		super(Polygone, self).__init__()
		try:
			assert(type(points) == type([]))
			assert(len(points) > 2)
			for point in points:
				assert(type(point) == Point)
				self.points.append(point)
		except AssertionError:
			raise GeometryError('Polygone needs a list of points to be created (at least 3 points)')



	def rotate(self,center,angle):
		return Polygone([p.rotate(center,angle) for p in self.points])
		




class"""docstring for Rectangle""" Rectangle(Polygone):
	
	def __init__(self, points):
		super(Rectangle, self).__init__(points)


	def opposite(self):
		[p.opposite() for p in self.points]