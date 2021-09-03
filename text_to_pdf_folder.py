#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 13:44:43 2020

@author: parag.patil
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 21:27:52 2020

@author: parag.patil
"""

# convert text to PDF for missing PDF files 319202
import os
import pdfkit

out_path="/home/parag.patil/Parag/Data/s3_cleaning/text_pdf_rename_files/"
flst=os.listdir(out_path)
flst=[x[:-4] for x in flst ]

filesconverted=[x+".txt" for x in flst ]

text_folder="/home/parag.patil/New_Data_Scientist/priynaka_backup/parag/pink_model_upload/"
txt_path=os.listdir(text_folder)



count=0
for fl in txt_path:
    tfl=fl
    fl=text_folder+fl
    if tfl not in filesconverted:

        with open(fl) as file:
                with open ("text.html", "w") as output:
                    file = file.read()
                    file = file.replace("\n", "<br>")
                    output.write(file)
        pdf_name=tfl[:-4]+".pdf"         
        pdfkit.from_file("text.html", out_path+pdf_name)
        os.remove("text.html")
        filesconverted.append(tfl)
        
        count+=1

        print("count----:",count)
        print("text file----:",fl)
        print("pdf file----:",out_path+pdf_name)
