import cv2
from imutils.contours import sort_contours
import numpy as np
import argparse
import imutils
from pyzbar.pyzbar import decode
# Make one method to decode the barcode  
def BarcodeReader(image): 
      
    # read the image in numpy array using cv2 
    img = cv2.imread(image) 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    #thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Morph open to remove noise and invert image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    opening = cv2.morphologyEx(blur, cv2.MORPH_OPEN, kernel, iterations=1)
    invert = 255 - opening
    # Decode the barcode image 
    return decode(opening)
                  
    #Display the image 
    #cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    #cv2.imshow("Image", img) 
    #cv2.waitKey(0) 
    #cv2.destroyAllWindows() 

import os
import pandas as pd
from tqdm import tqdm

def get_cods():
    files = os.listdir("imgs")

    headers = {
        'img_path' : [],
        'barcode_data' : [],
        'barcode_type' : [],
        'barcode_x' : [],
        'barcode_y' : [],
        'barcode_w': [],
        'barcode_h' : []
    }

    df = pd.DataFrame(data=headers)

    for file in files:
        if file.split('.')[1] != 'png':
            files.remove(file)

    for i in tqdm(range(len(files))):
        file = files[i]
        #if file.split('.')[1] == 'png':
        try:
            barcodes = BarcodeReader(f'Pt2_codbarras/{file}')
            if len(barcodes) != 0:
                for barcode in barcodes:
                    (x,y,w,h) = barcode.rect
                    data = {
                        'img_path' : file,
                        'barcode_data' : barcode.data,
                        'barcode_type' : barcode.type,
                        'barcode_x' : x,
                        'barcode_y' : y,
                        'barcode_w': w,
                        'barcode_h' : h
                    }
                    df = df._append(data, ignore_index=True)
            else:
                data = {
                        'img_path' : file,
                        'barcode_data' : "",
                        'barcode_type' : "",
                        'barcode_x' : "",
                        'barcode_y' : "",
                        'barcode_w': "",
                        'barcode_h' : ""
                    }
                df = df._append(data, ignore_index=True)


        except:
            print(file)
            data = {
                    'img_path' : file,
                    'barcode_data' : "",
                    'barcode_type' : "",
                    'barcode_x' : "",
                    'barcode_y' : "",
                    'barcode_w': "",
                    'barcode_h' : ""
                }
            df = df._append(data, ignore_index=True)
    return df

if __name__ == "__main__":
    df = get_cods()
    df.to_csv('cods_barras.csv')