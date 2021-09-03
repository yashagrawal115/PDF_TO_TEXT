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

import ocrmypdf
import PIL





def extract_text(pdf_file,output_path):
    
    try:
        
        
    
    
    #print (f)
        pages = convert_from_path(pdf_file,dpi=120)
        
        images = pages
        file="temp.pdf"
        images[0].save(pwd+"/"+file, save_all=True, append_images=images[1:],quality=40, optimize=True)
        ocrmypdf.ocr(pwd+"/"+file,pwd+"/"+file,use_threads=False,progress_bar=True,language="eng+hin")
            
            
            
            
            
            
        with open(pwd+"/"+file, "rb") as f: 
            
            
            
            pdf = pdftotext.PDF(f)
            os.remove(pwd+"/"+file)
        text=""
        for p in range(0,len(pdf)):
            text=text+pdf[p]+"\n"
        pdf_file = os.path.split(pdf_file)[-1]
        filename, file_extension = os.path.splitext(pdf_file)
        output=output_path+"/"+filename+".txt"
        #print output
        with open(output, 'w') as f:
            for item in text.split('\n'):
                f.write("%s\n" % item)
    except Exception:
        
        print("ignoring file ",file)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno) 
        pass           
          
if __name__ == "__main__":
    input_path = sys.argv[1]
    output_path=sys.argv[2]
    #os.chdir(input_path)
#    input_path = "/run/user/1000/gvfs/smb-share:server=sbr-qnap-02,share=data_scientist/ALL_JUDGEMENTS/US_Courts_2/"
#    output_path = "/home/ganeshkharad/New_Data_Scientist/1_JET/2_US/1_Extract/usa_text_c2/"

#    pdf_list = os.listdir(input_path)  #[f for f in glob.glob("*.pdf")]
    
    pdf_list = list()
#processed_case_filenames = list()

    dirName = input_path #"/home/ganeshkharad/Downloads/All_Judgements/UK/"
    for (dirpath, dirnames, filenames) in os.walk(dirName):
    
        pdf_list += [os.path.join(dirpath, file) for file in filenames]    

    i=0
    for pdf in pdf_list:
        print (i,pdf)
        try:
            extract_text(pdf,output_path)
        except:
            pass
            
            #os.remove(pdf)
        i=i+1
    print ("completed the conversion of pdf files")


