import cv2
import sys
import os


# Based on https://stackoverflow.com/questions/10702105/detecting-led-object-status-from-image
# Based on https://answers.opencv.org/question/65545/led-blinking-frequency/

nameFileEntry = "VideoTest.mp4" # Name of video.
vidcap = cv2.VideoCapture(nameFileEntry)

nameFileExit = "ficheroSalida.txt"

success, image = vidcap.read()

if not success:
    print("No ha sido posible abrir el archivo")
    sys.exit()

count = 0  # Number of frames
while success:
    cv2.imwrite("frame%d.jpg" % count, image)  # save frame as jpg file
    success, image = vidcap.read()
    
    count += 1

# This code changes to grayscale the .jpg images obtained before.
count2 = 0
while count2 < count:
    img = cv2.imread('frame%d.jpg' % count2, cv2.IMREAD_GRAYSCALE)
    if img is None:
        sys.exit("Could not read image in count " + str(count2))
    cv2.imwrite("frameGris%d.jpg" % count2, img)
    count2 += 1

# Code that obtains in the first frames, the 0, and the number of contours that has the 0.
# Let's assume the video always starts at 0.

zero = cv2.imread('frameGris0.jpg')
imgray = cv2.cvtColor(zero, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray, 127, 255, 0)
   
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
numeroContornos = contours


# Loop that takes out by file each of the 1s or 0s

file = open('M-binario.txt', "w")  # Abrimos un fichero desde cero.
count3 = 0
while count3 < count:
    

    img1 = cv2.imread('frameGris%d.jpg' % count3)
    imgray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

    # https://docs.opencv.org/master/d7/d4d/tutorial_py_thresholding.html    
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
        
    contours, hierarchy = cv2.findContours(
    thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # Instead of looking at the number of contours, we now look at whether there is a difference in contours, i.e. whether there are more contours than in the frame0
    if (len(contours) <= len(numeroContornos)):
        file.write("0")
    if (len(contours) > len(numeroContornos)):
        file.write("1")
    count3 += 1

file.close()
    

file = open('M-binario.txt', "r")

cadena = file.read()

punteroCadena = 0
LongitudCadenas1 = 0
LongitudCadenas0 = 0

# First we put the pointer on the first 1.
while cadena[punteroCadena] == '0' and punteroCadena < len(cadena)-1:
    punteroCadena += 1
# We count how many 1s each digit is 1

while cadena[punteroCadena] == '1' and punteroCadena < len(cadena)-1:
    LongitudCadenas1 += 1
    punteroCadena += 1

# We count how many 0s each digit is 0
while cadena[punteroCadena] == '0' and punteroCadena < len(cadena)-1:
    LongitudCadenas0 += 1
    punteroCadena += 1

# We generate the limits of the 1s and 0s.

LimiteSuperior0 = LongitudCadenas0 + 2
LimiteSuperior1 = LongitudCadenas1 + 2

# The string is in the second 10 of the preamble, so in the file we write '10
finalFile = open(nameFileExit, "w")

finalFile.write('10')

# Another extra loop reading the 0s and 1, by strings and writing to a file apart from 0 and 1, depending on the size of the string.

while punteroCadena < count:

    numeroCeros = 0
    numeroUnos = 0
    if cadena[punteroCadena] == '0':
        while punteroCadena < count and cadena[punteroCadena] == '0':

            numeroCeros += 1
            punteroCadena += 1
    else:
        while punteroCadena < count and cadena[punteroCadena] == '1':
            numeroUnos += 1
            punteroCadena += 1

    if numeroCeros != 0:
        if numeroCeros <= LimiteSuperior0:
            finalFile.write('0')
        else:
            finalFile.write('00')
    if numeroUnos != 0:
        if numeroUnos <= LimiteSuperior1:
            finalFile.write('1')
        else:
            finalFile.write('11')

finalFile.close()





