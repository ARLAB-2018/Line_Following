import cv2
import numpy as np

cap = cv2.VideoCapture( 'Normal_Brightness.mp4' )   #Caputure video
sensors = 5  #Number of senors(Hypothetical)
threshold = 0.1 #Sensitivity of Color detection
Kernel_size=15

def thresholding( img ):                                       #Creates an HSV mask over the live feed
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(img, (Kernel_size, Kernel_size), 0)
	hsv = cv2.cvtColor( blurred, cv2.COLOR_BGR2GRAY )
	#hsv = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY )
	ret, thresh1 = cv2.threshold(hsv, 120, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)   
	return thresh1


def getContours( imgThres, img ):                             #Forms a contour around the largest visible(White) patch
	contours, heirarchy = cv2.findContours( imgThres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE )
	biggest = max( contours, key=cv2.contourArea )
	x, y, w, h = cv2.boundingRect( biggest )
	cx = x + w // 2
	cy = y + h // 2
	cv2.drawContours( img, biggest, -1, (255, 255, 0), 5 )
	cv2.circle( img, (cx, cy), 5, (0, 128, 255), cv2.FILLED )

	
def droneOutput(senOut):                                      #Gives Commands to drone
	if senOut==[0,1,1,1,0] :
		return 'Move Forward'
	if senOut==[0,1,1,1,1] :
		return  'Move Slight Right'
	if senOut==[1,1,1,1,0] :
		return  'Move Sligth Left'
	if senOut==[1,1,1,0,0] :
		return  'Move Left'
	if senOut==[0,0,1,1,1] :
		return  'Move Right'
	if senOut==[0,0,0,1,1] :
		return  'Rotate Right'
	if senOut==[1,1,0,0,0] :
		return  'Rotate Left'
	else :
		return 'Stop'
   

def getSensorOutput( imgThres, sensor ):                      #Senses the position of the drone along the path
	imgs = np.hsplit( imgThres, sensor )
	totalPixels = (img.shape[1] // sensor) * img.shape[0]
	senOut = []
	for x, im in enumerate( imgs ):
		pixelCount = cv2.countNonZero( im )
		if pixelCount > threshold * totalPixels:
			senOut.append( 1 )
		else:
			senOut.append( 0 )
		cv2.imshow( str( x ), im )
	print( senOut )
	return senOut


while True:
	_, img = cap.read()
	img = cv2.resize( img, (480, 360) )
	img = cv2.flip( img, 1 )

	imgThres = thresholding( img )
	cx = getContours( imgThres, img )  # Translation
	senOut = getSensorOutput( imgThres, sensors )
	cv2.imshow( "Output", img )
	cv2.imshow( "Path", imgThres )
	print(droneOutput(senOut))
	cv2.waitKey( 10 )