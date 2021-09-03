#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 20:52:46 2019

@author: ganeshkharad
"""

import pdftotext
import sys
import os


def extract_text(pdf_file,output_path):
    with open(pdf_file, "rb") as f:
        pdf = pdftotext.PDF(f)
    text=""
    for p in range(0,len(pdf)):
        text=text+pdf[p]+"\n"
    pdf_file = os.path.split(pdf_file)[-1]
    filename, file_extension = os.path.splitext(pdf_file)
    output=output_path+"/"+filename+".txt"
    #print output
    with open(output, 'w') as f:
        for item in text.split('\n'):
            #item=item.encode("utf-8")
            f.write("%s\n" % item)
            
          
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


