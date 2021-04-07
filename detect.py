import cv2
import pytesseract
import numpy as np

# Mention the installed location of Tesseract-OCR in your system
pytesseract.pytesseract.tesseract_cmd = 'System_path_to_tesseract.exe'

# Read image from which text needs to be extracted
img = cv2.imread("sample.jpg")
# img = cv2.imread("burberry.jpg")
# img = cv2.imread("subway.jpg")

  
# Preprocessing the image starts
  
# Convert the image to gray scale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# cv2.imshow('gray',gray)
# cv2.waitKey()

# Performing OTSU threshold
ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
# cv2.imshow('thresh1',thresh1)
# cv2.waitKey()
  
# Specify structure shape and kernel size. 
# Kernel size increases or decreases the area 
# of the rectangle to be detected.
# A smaller value like (10, 10) will detect 
# each word instead of a sentence.
rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
  
# Appplying dilation on the threshold image
dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)
# cv2.imshow('dilation',dilation)
# cv2.waitKey()


############# Edge-Detection for Contours #############
# # converting BGR to HSV
# hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
# # define range of red color in HSV
# lower_red = np.array([30,150,50])
# upper_red = np.array([255,255,180])
    
# # create a red HSV colour boundary and 
# # threshold HSV image
# mask = cv2.inRange(hsv, lower_red, upper_red)

# # Bitwise-AND mask and original image
# res = cv2.bitwise_and(img,img, mask= mask)

# # Display an original image
# cv2.imshow('Original',img)

# # finds edges in the input image image and
# # marks them in the output map edges
# edges = cv2.Canny(img,200,300)

# # Display edges in a frame
# cv2.imshow('Edges',edges)

# # Wait for Esc key to stop
# cv2.waitKey()
# contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, 
#                                                  cv2.CHAIN_APPROX_NONE)
# contours = sorted(contours, key=cv2.contourArea, reverse=True)
#####################################################

  
# Finding contours
contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, 
                                                 cv2.CHAIN_APPROX_NONE)
  
# Creating a copy of image
im2 = img.copy()
  
# A text file is created and flushed
file = open("recognized.txt", "w+")
file.write("")
file.close()
  
# Looping through the identified contours
# Then rectangular part is cropped and passed on
# to pytesseract for extracting text from it
# Extracted text is then written into the text file
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
      
    # Drawing a rectangle on copied image
    rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
      
    # Cropping the text block for giving input to OCR
    cropped = im2[y:y + h, x:x + w]
    # cv2.imshow('cropped',cropped)
    # cv2.waitKey()
      
    # Open the file in append mode
    file = open("recognized.txt", "a")
      
    # Apply OCR on the cropped image
    text = pytesseract.image_to_string(cropped)
      
    # Appending the text into file
    file.write(text)
    file.write("\n")
      
    # Close the file
    file.close