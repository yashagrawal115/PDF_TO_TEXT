#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 12:10:30 2020

@author: parag.patil
"""

import pdftotext
import sys
import os


pwd=os.getcwd()

from pdf2image import convert_from_path
from nostril import nonsense
#from wand.image import Image
from PIL import Image as PI
import pyocr
import pyocr.builders
tool = pyocr.get_available_tools()[0]
#lang = tool.get_available_languages()[1] # // 1 is eng
lang='eng'
import io
import re
import PIL
import logging

import tempfile

import cv2
import numpy as np
from PIL import Image

IMAGE_SIZE = 1800
BINARY_THREHOLD = 180

def process_image_for_ocr(file_path):
    # TODO : Implement using opencv
    temp_filename = set_image_dpi(file_path)
    im_new = remove_noise_and_smooth(temp_filename)
    return im_new

def set_image_dpi(file_path):
    im = Image.open(file_path)
    length_x, width_y = im.size
    factor = max(1, int(IMAGE_SIZE / length_x))
    size = factor * length_x, factor * width_y
    # size = (1800, 1800)
    im_resized = im.resize(size, Image.ANTIALIAS)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
    temp_filename = temp_file.name
    im_resized.save(temp_filename, dpi=(300, 300))
    return temp_filename

def image_smoothening(img):
    ret1, th1 = cv2.threshold(img, BINARY_THREHOLD, 255, cv2.THRESH_BINARY)
    ret2, th2 = cv2.threshold(th1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    blur = cv2.GaussianBlur(th2, (1, 1), 0)
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th3

def remove_noise_and_smooth(file_name):
    img = cv2.imread(file_name, 0)
    filtered = cv2.adaptiveThreshold(img.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 41,
                                     3)
    kernel = np.ones((1, 1), np.uint8)
    opening = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    img = image_smoothening(img)
    or_image = cv2.bitwise_or(img, closing)
    return or_image

def texts(pdf_file):
    try:
        with open(pdf_file, "rb") as f:
            
            pdf = pdftotext.PDF(f)
            
        text=""
        for p in range(0,len(pdf)):
            tmp_text=pdf[p]
            
            if tmp_text != "" :
                text=text+pdf[p]+"\n"
                

    
        return (text)
    except Exception as e :
        print(e)
        return ""
        pass

def text_check(text):
    try:
        if len(text)>100:
            if nonsense(text):
                return True
        else:
            return False
    except Exception as e :
        print(e)
        return False
        pass 

def file_size(pdf_file,text):
    try:
        statinfo = os.stat(pdf_file)
        size =  statinfo.st_size
        if size>500000 and len(text)<1000:
            return True
        else:
            return False        
    except Exception as e :
        print(e)
        return False
        pass         
    
def extract_text(pdf_file,output_path):
    final_text=[]
    text_extracted = texts(pdf_file)

    

    if text_extracted=="" or text_check(text_extracted) or file_size(pdf_file,text_extracted):
        print ("PDF is fulty/image PDF, running OCR")
        path=pdf_file
        pages = convert_from_path(path, 300)


        img='out.jpg'
        for page in pages:
            page.save(img, 'JPEG') 
            #img_tmp=process_image_for_ocr(img)
            #cv2.imwrite(img,img_tmp)
            txt = tool.image_to_string(
                PI.open(img),
                lang=lang,
                builder=pyocr.builders.TextBuilder()
            )
            #print (txt)
            final_text.append(txt)
        if os.path.exists(img):
            os.remove(img)
        pdf_file = os.path.split(pdf_file)[-1]
        filename, file_extension = os.path.splitext(pdf_file)
        output=output_path+"/"+filename+".txt"
        with open(output, 'w') as f:
            for item in final_text:
                #item=item.encode("utf-8")
                f.write("%s\n" %item)
        
        
    
    
    else:

        pdf_file = os.path.split(pdf_file)[-1]
        filename, file_extension = os.path.splitext(pdf_file)
        output=output_path+"/"+filename+".txt"
        with open(output, 'w') as f:
            for item in text_extracted.split('\n'):
                f.write("%s\n" % item)
            
import time
start_time = time.time()
          
if __name__ == "__main__":
    input_path = sys.argv[1]
    output_path=sys.argv[2]


    
    pdf_list = list()
    logging.basicConfig(level=logging.INFO,filename='ocr_logs.log',format='%(message)s')
    logging.info("OCR started")
	

    dirName = input_path #"/home/ganeshkharad/Downloads/All_Judgements/UK/"
    for (dirpath, dirnames, filenames) in os.walk(dirName):
    
        pdf_list += [os.path.join(dirpath, file) for file in filenames]    

    i=1
    for pdf in pdf_list:
        print ("no of files processed:",i,"file name:",pdf)
        logging.info('OCR details: %s', { 'no of files processed:': i, 'file name:' : pdf })
        try:
            extract_text(pdf,output_path)
        except:
            pass
            
            #os.remove(pdf)
            
        i=i+1
    print ("completed the conversion of pdf files")
    logging.info("completed the conversion of pdf files")
    print("--- %s seconds ---" % (time.time() - start_time))



