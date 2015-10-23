"""
# Coordinates 
	* Add comments!
"""
from math import *

"""
	 * Given a phr along with density, approximate radius size, and size of ESBR side
	 * returns a tuple containing two values: actual radius size and number of fillers
"""
def invPHR(phr, densityFiller, radiusFiller, densityMatrix, sideMatrix, twoD=True):
	import numpy
	
	radiusStep = 0.03*radiusFiller # Alter radius to accommodate varying phr 
	
	if twoD:
		numberFillers = numpy.arange(1.,36.) # 1 to 30 particles
		rsSquared = (numpy.arange(radiusFiller-10*radiusStep,  
			radiusFiller+10*radiusStep , radiusStep)) ** 2
		## Grid of number circles with variable radius
		nRGrid = numpy.outer(numberFillers,rsSquared) * pi 
		## Grid of differences
		diffGrid = sideMatrix ** 2 - nRGrid
	else:
		defaultN = 75
		endRange = calculatePHR3D(defaultN, densityFiller, radiusFiller+
			10*radiusStep, densityMatrix, sideMatrix)
		while phr > endRange:
			defaultN = defaultN * 0.1 + defaultN
			endRange = calculatePHR3D(defaultN, densityFiller, radiusFiller+
				10*radiusStep, densityMatrix, sideMatrix)
		
		numberFillers = numpy.arange(1.,defaultN+1) # 1 to defaultN+1 particles
		rsCubed = (numpy.arange(radiusFiller-10*radiusStep,  
			radiusFiller+10*radiusStep , radiusStep)) ** 3
		## Grid of number circles with variable radius
		nRGrid = numpy.outer(numberFillers,rsCubed) * pi * 4.0/3.0
		## Grid of differences
		diffGrid = sideMatrix ** 3 - nRGrid 
	
	ratioGrid = nRGrid/diffGrid
	phrGrid = numpy.multiply((100 * densityFiller / densityMatrix), ratioGrid)
	# Matrix of distances from phr
	distn = numpy.power(numpy.power((phr-phrGrid), 2), 0.5)
	# Returns the combination yielding closest approximation to phr
	vals = numpy.nonzero(distn == distn.min()) 
	if twoD:
		r = numpy.sqrt(rsSquared[vals[1][0]]) 
	else:
		r = numpy.power((rsCubed[vals[1][0]]), 1/3.0)
	
	n = numberFillers[vals[0][0]] # number of inclusions
	return r, int(n)

# Need an input PHR and then an actual PHR same with volume.
# Add a uniform version! one that isn't so random for when i fix all 
# the inputs and just search over interface values
def getPoints2D(seed, side, radius, number):
	import random
	import numpy
	random.seed(seed)
	
	rng = side-2.2*radius
	randXs = (1.1* radius) + rng * numpy.random.rand(100000,1)
	randYs = (1.1* radius) + rng * numpy.random.rand(100000,1)
	
	delta = 2.1 * radius;
	xCoords = [randXs[0][0]]
	yCoords = [randYs[0][0]]
	numberCoords = 1
	
	for i in range(1, 100000):
		x = randXs[i]
		y = randYs[i]
		distances = numpy.sqrt(numpy.power((x-xCoords), 2) + numpy.power((y-yCoords), 2))
		mindist = numpy.min(distances)
		if numberCoords == number:
			break
		if (mindist > delta):
			xCoords.append(x[0])
			yCoords.append(y[0])
			numberCoords += 1
		
	
	warningMsg = ''
	if numberCoords != number:
		warningMsg = '*'
		number = numberCoords # Needed for updated return value.
	
	return xCoords, yCoords, warningMsg, number

# Be more descriptive. This is confusing
def getPoints3D(seed, side, radius, number, interfacePortion=0.0, deltaCoefficient=0.15):
	import random
	import numpy
	random.seed(seed)
	
	# Delta is distances between particles
	#delta = 2 * radius + (radius * deltaCoefficient) + (interfacePortion * radius) # Default delta will be 2 radius + one tenth of radius. s
	# Think this works.
	#delta = 2 * ((radius + (radius * interfacePortion)) + (deltaCoefficient*(radius + radius*interfacePortion)))
	
	# x, y inside matrix without touching sides
	# This may be an issue.
	#rngr = side - (delta + radius * deltaCoefficient + radius * interfacePortion)
	#rngr = side - delta
	#rngr = (delta / 2.0) + (delta/2.0) * 0.1
	#randXs = (radius + (radius * deltaCoefficient) + (interfacePortion * radius)) + rngr * numpy.random.rand(100000,1)
	#randYs = (radius + (radius * deltaCoefficient) + (interfacePortion * radius)) + rngr * numpy.random.rand(100000,1)
	#randZs = (radius + (radius * deltaCoefficient) + (interfacePortion * radius)) + rngr * numpy.random.rand(100000,1)
	
	#randXs = rngr + (side-(rngr)) * numpy.random.rand(100000,1)
	#randYs = rngr + (side-(rngr)) * numpy.random.rand(100000,1)
	#randZs = rngr + (side-(rngr)) * numpy.random.rand(100000,1)
	
	######
	r = radius
	i = radius * interfacePortion + radius
	dC = i * deltaCoefficient + i
	d = r + (i - r) + (dC - i)
	#d = radius + (interfacePortion * radius + radius)
	randXs = d + (side-(2 * d)) * numpy.random.rand(100000,1)
	randYs = d + (side-(2 * d)) * numpy.random.rand(100000,1)
	randZs = d + (side-(2 * d)) * numpy.random.rand(100000,1)
	
	xCoords = [randXs[0][0]]
	yCoords = [randYs[0][0]]
	zCoords = [randZs[0][0]]
	numberCoords = 1
	
	for i in range(1, 100000):
		x = randXs[i]
		y = randYs[i]
		z = randZs[i]
		distances = numpy.sqrt(numpy.power((x-xCoords), 2) + numpy.power((y-yCoords), 2) + numpy.power((z-zCoords), 2))
		mindist = numpy.min(distances)
		if numberCoords == number:
			break
		if (mindist > 2 * d):
			xCoords.append(x[0])
			yCoords.append(y[0])
			zCoords.append(z[0])
			numberCoords += 1
		
	
	warningMsg = ''
	if numberCoords != number:
		warningMsg = '?'
		number = numberCoords # Needed for updated return value.
	
	return xCoords, yCoords, zCoords, warningMsg, number

# Add a method to search hash for phr or volPortion then point to proper inv function

##########################################
# Hard coded simulations, make more general soon...
def detCoordinatesAlumina():
	import numpy
	
	# Get all data out of excel into the general method..
	side = 520
	number = 8
	radius = 46
	deltaPortion = 0.2
	lowInterPortion = 0.1
	highInterPortion = 1.15
	phr = 10
	interRad = 98.9
	deltaRad = 118.68
	d = deltaRad
	
	#d = radius + (interfacePortion * radius + radius)
	xs = []
	ys = []
	zs = []
	
	numberCoords = 0
	nz = [1, 3]
	
	sizeInc = side / 4.0
	
	# This also limits delta to < 1/4 side or whatever...
	# So maybe define interface range to be < 1/4 side or 1/n depending on number
	for i in nz:
		for j in nz:
			for k in nz:
				xs.append(sizeInc*i)
				ys.append(sizeInc*j)
				zs.append(sizeInc*k)
	
	# Use recursion for variable nested loops
	#for i in nz:
	#	for j in nz:
	#		for k in nz:
	#			xs.append(d*i)
	#			ys.append(d*j)
	#			zs.append(d*k)
	
	return xs, ys, zs

## ADD code to have all the functionality the excel file has for determining
# all the ranges, numbers, radius, etc. Bisection method or similar should be fine

def holder():
	numberPossibilities = [1, 8, 27, 64, 125]

# Alternate version of other invPHR function
# NOTE: consider having one that returns closes approximation for each number size
# so we can make sure that number of particles doesn't disproportionately influence 
# TC. 
def invPHRAlternate3D(phr, densityFiller, radiusFiller, densityMatrix, sideMatrix):
	import numpy
	radiusStep = 0.02*radiusFiller # Alter radius to accommodate varying phr 
	stepSize = 15
	nS = [1, 8, 27, 64, 125]
	endRange = calculatePHR3D(nS[4], densityFiller, 
		radiusFiller+stepSize*radiusStep, densityMatrix, sideMatrix)
	lowRange = calculatePHR3D(nS[0], densityFiller, 
		radiusFiller-stepSize*radiusStep, densityMatrix, sideMatrix)
	
	while phr > endRange and phr < lowRange:
		if phr > endRange:
			stepSize = stepSize + 1
			endRange = calculatePHR3D(nS[4], densityFiller, radiusFiller+
				stepSize*radiusStep, densityMatrix, sideMatrix)
		else:
			stepSize = stepSize + 1
			lowRange = calculatePHR3D(nS[4], densityFiller, radiusFiller+
				stepSize*radiusStep, densityMatrix, sideMatrix)
			
	
	rsCubed = (numpy.arange(radiusFiller-stepSize*radiusStep,  
		radiusFiller+10*radiusStep , radiusStep)) ** 3
	## Grid of number circles with variable radius
	nRGrid = numpy.outer(nS,rsCubed) * pi * 4.0/3.0
	## Grid of differences
	diffGrid = sideMatrix ** 3 - nRGrid 
	
	ratioGrid = nRGrid/diffGrid
	phrGrid = numpy.multiply((100 * densityFiller / densityMatrix), ratioGrid)
	# Matrix of distances from phr
	distn = numpy.power(numpy.power((phr-phrGrid), 2), 0.5)
	# Returns the combination yielding closest approximation to phr
	vals = numpy.nonzero(distn == distn.min()) 
	r = numpy.power((rsCubed[vals[1][0]]), 1/3.0)
	n = nS[vals[0][0]] # number of inclusions
	return r, int(n)

# phr = 10
# densityFiller = 3.950e-015
# radiusFiller = 37.5
# densityMatrix = 9.3e-016
# sideMatrix = 520
# r, n = invPHRAlternate3D(phr, densityFiller, radiusFiller, densityMatrix, sideMatrix)

## NEED TO LIMIT DELTA < side/2*(n^1/3)

# Now next... we want the placement of the sphere centers that lets us vary our 
# interface size within the limits specified. 1. limit function, 2. change "getPoints"

# Works!!
def getInterfacePortionLimit(side, radius, number, delta=0.15):
	import numpy
	
	#hardLimit = side / (2.0 * number ** (1/3.0)) # Ensure d < this
	
	numerator = side - (2.0 * (number ** (1/3.0))) * (radius * delta + radius)
	denominator = 2.0 * (number ** (1/3.0)) * (radius * delta + radius)
	intPortionLimit = numerator / float(denominator)

	return intPortionLimit

def getPoints3dDeterministic(side, radius, number, interfacePortion=0.0, delta=0.15):
	import numpy
	
	xs = []
	ys = []
	zs = []
	
	impNum = (2 *(number ** (1/3.0)))
	impNum = int(round(impNum))
	nz = [y+1 for y in range(impNum) if (y+1) % 2 == 1]
	sizeInc = side / float(impNum)
	
	# This also limits delta to < 1/4 side or whatever...
	# So maybe define interface range to be < 1/4 side or 1/n depending on number
	for i in nz:
		for j in nz:
			for k in nz:
				xs.append(sizeInc*i)
				ys.append(sizeInc*j)
				zs.append(sizeInc*k)
	
	return xs, ys, zs


""" Need to fix!
"""
# Need a better way for dealing with fractional inclusions similar to invPHR function
def invAreaCircle(radiusFiller, sideMatrix, areaRatio):
	import numpy
	numberFillers = round((areaRatio * sideMatrix ** 2) / (pi * radiusFiller ** 2))
	return numberFillers

"""
	Returns number of fillers
	* ToDo : Add smaller particles instead of rounding
	* Specific to Spheres, need functionality for squares, ellipses, and TMOICF
"""
def invVolumeSphere(radiusFiller, sideMatrix, volumePortion):
	import numpy
	numFillers = round((3.0 / 4.0 * volumePortion * sideMatrix ** 3) / (pi * radiusFiller ** 3))
	return numFillers

def calculatePHR3D(n, densityFiller, radiusFiller, densityMatrix, sideMatrix):
	numerator = n * pi * radiusFiller * radiusFiller * radiusFiller * (4/3.0)
	denominator = sideMatrix * sideMatrix * sideMatrix - numerator
	phr = (numerator / denominator) * (densityFiller / densityMatrix) * 100
	return phr

def calculateVolume(n, radiusFiller, sideMatrix):
	return ((n * pi * (4.0/3.0) * radiusFiller ** 3) / (sideMatrix ** 3))


"""
	(seed, side, radius, number, interfacePortion=0.0, deltaCoefficient=0.15
def drawDeterminedPoints2D(side, radius, number, interfacePortion=0.0, deltaCoefficient=0.15):
	# Delta is distances between particles
	delta = 2 * radius + (radius * deltaCoefficient) + (interfacePortion * radius) # Default delta will be 2 radius + one tenth of radius.
	
	# x, y inside matrix without touching sides
	rngr = side - (delta + radius * deltaCoefficient + radius * interfacePortion)
	randXs = (radius + (radius * deltaCoefficient) + (interfacePortion * radius)) + rngr * numpy.random.rand(100000,1)
	randYs = (radius + (radius * deltaCoefficient) + (interfacePortion * radius)) + rngr * numpy.random.rand(100000,1)
	randZs = (radius + (radius * deltaCoefficient) + (interfacePortion * radius)) + rngr * numpy.random.rand(100000,1)
	
	if num == 1:
		r1 = (side/2, side/2)
	elif num == 2 through 4:
		r1 = (side/4, side/4)
		r2 = (side/4, 3*side/4)
		r3 = (3*side/4, 3*side/4)
		r4 = (3*side/4, side/4)
	elif num == 5 through 16:
		r1 = etc
		
	until parittion side length is less than radius + delta + interface
	
	
	xCoords = [randXs[0][0]]
	yCoords = [randYs[0][0]]
	zCoords = [randZs[0][0]]
	numberCoords = 1
	
	for i in range(1, 100000):
		x = randXs[i]
		y = randYs[i]
		z = randZs[i]
		distances = numpy.sqrt(numpy.power((x-xCoords), 2) + numpy.power((y-yCoords), 2) + numpy.power((z-zCoords), 2))
		mindist = numpy.min(distances)
		if numberCoords == number:
			break
		if (mindist > delta):
			xCoords.append(x[0])
			yCoords.append(y[0])
			zCoords.append(z[0])
			numberCoords += 1
		
	
	warningMsg = ''
	if numberCoords != number:
		warningMsg = '*'
		number = numberCoords # Needed for updated return value.
	
	return xCoords, yCoords, zCoords, warningMsg, number
	
"""


"""
# Add methods for Carbon Nanotubes 2D & 3D
def invAreaRectangle(lengthFiller, heightFiller, sideMatrix, areaRatio) # 2D Carbon nanotube as a rectangle
	import numpy
	numberFillers = round((areaRatio * sideMatrix ** 2) / (lengthFiller * heightFiller))
	return numberFillers

def getPointsRectangle(seed, side, length, width, number, orientation=45, randomO=False):
	import random
	import numpy
	random.seed(seed)
	
	
	
	rng = int(side-2.2*radius)
	randXs = (1.1* radius) + rng * numpy.random.rand(100000,1)
	randYs = (1.1* radius) + rng * numpy.random.rand(100000,1)
	
	delta = 2.1 * radius;
	xCoords = [randXs[0]]
	yCoords = [randYs[0]]
	numberCoords = 1
	
	for i in range(1, 100000):
		x = randXs[i]
		y = randYs[i]
		distances = numpy.sqrt(numpy.power((x-xCoords), 2) + numpy.power((y-yCoords), 2))
		mindist = numpy.min(distances)
		if numberCoords == number:
			break
		if (mindist > delta):
			xCoords.append(x)
			yCoords.append(y)
			numberCoords += 1
		
	
	warningMsg = ''
	if numberCoords != number:
		warningMsg = '*'
	
	return xCoords, yCoords, warningMsg


# Add a method that gives warning for possible combinations that aren't feasible.

# All unused! 

def invAreaSquare(fillerSide, siliconSide, volumePortion):

	Returns number of fillers

	import numpy
	volumePortion = volumePortion / 100.0
	numFillers = round((volumePortion * siliconSide * siliconSide) / (volumePortion * fillerSide * fillerSide + fillerSide * fillerSide))
	return numFillers
 


def invAreaEllipse(fillerLength, fillerHeight, siliconSide, volumePortion)
	import numpy
	volumePortion = volumePortion / 100.0
	numFillers = ((volumePortion * siliconSide * siliconSide) / (volumePortion * .5 * fillerLength * .5 * fillerHeight * pi + .5 * fillerLength * .5 * fillerHeight * pi))
	return numFillers

def invVolumeCube(fillerSide, siliconSide, volumePortion):
	
	import numpy
	volumePortion = volumePortion / 100.0
	numFillers = round((volumePortion * (siliconSide ** 3)) / (volumePortion * (fillerSide ** 3) + (fillerSide ** 3)))
	return numFillers
	
def invVolumeBlock(fillerLength, fillerHeight, fillerWidth, siliconSide, volumePortion):
	
	import numpy
	volumePortion = volumePortion / 100.0
	numFillers = round((volumePortion * (siliconSide ** 3)) / (volumePortion * fillerLength * fillerHeight * fillerWidth + fillerLength * fillerHeight * fillerWidth))
	return numFillers

def invVolumeElipsoid(fillerRLength, fillerRHeight, fillerRWidth, siliconSide, volumePortion):
	
	import numpy
	volumePortion = volumePortion / 100.0
	numFillers = round((volumePortion * (siliconSide ** 3)) / (volumePortion * (4/3.0) * pi * fillerRHeight * fillerRLength * fillerRWidth + fillerRLength * fillerRHeight * fillerRWidth * (4/3.0) * pi))
	return numFillers
"""