from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO
import os

import sys    
reload(sys)  
sys.setdefaultencoding('utf-8')

path = os.getcwd()



def pdfparser(filename):

    fp = file(os.path.join(input_path,filename), 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Process each page contained in the document.
    text=""
    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
        data =  retstr.getvalue()
        text=text+data+"\n"
    #print data
    txt_filename = filename.replace(".pdf",".txt")

    with open(os.path.join(output_path,txt_filename), 'w') as f:
        for item in data.split('\n'):
            item=item.encode("utf-8")
            f.write("%s\n" % item)
#            
##########################            
# =============================================================================
# def extract_text(pdf_file,output_path):
#     with open(pdf_file, "rb") as f:
#         pdf = pdftotext.PDF(f)
#     text=""
#     for p in range(0,len(pdf)):
#         text=text+pdf[p]+"\n"
#         
#     filename, file_extension = os.path.splitext(pdf_file)
#     output=output_path+"/"+filename+".txt"
#     #print output
#     with open(output, 'w') as f:
#         for item in text.split('\n'):
#             item=item.encode("utf-8")
#             f.write("%s\n" % item)
# =============================================================================
 ##################################################                       

if __name__ == '__main__':
    input_path = sys.argv[1] #"/home/ganeshkharad/Downloads/test/"#
    output_path = sys.argv[2] #"/home/ganeshkharad/Downloads/test/"#
    files_list = os.listdir(input_path)
    for pdf_file in files_list:
        if pdf_file.endswith(".pdf"):
            
            pdfparser(pdf_file)  
