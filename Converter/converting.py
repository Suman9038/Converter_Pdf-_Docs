import subprocess
import os
from pdf2docx import Converter

UNOCONV_PATH = r'python C:\unoconv-0.8.2\unoconv-0.8.2\unoconv.py'

def convert_docx_to_pdf(docx_path:str , pdf_path: str) :
    try :
        command= f'{UNOCONV_PATH} -f pdf -o "{pdf_path}" "{docx_path}"'
        subprocess.run(command,shell=True,check=True) # subprocess system command execute karne k liye use hota h, shell= true mtlb h ki shell k through command run hoga 
        return {"message": "Conversion successful", "output": pdf_path}
    except Exception as e:
        return {"error": f"Failed to convert DOCX to PDF: {str(e)}"}
    
def convert_pdf_to_docx(pdf_path: str, docx_path: str) :
    try :
        cv=Converter(pdf_path) # Converter object banaka k jo pdf file ko read kiya jo mtlb pdf tha usko converter k andar daal diya 
        cv.convert(docx_path, start= 0, end= None) # pura page convert kar raha h suru se leke last tak isliya start=0 and end none h  
        cv.close() #conversion ho jane k bad jo object bana tha usko close kar dera h 
        return {"message": "Conversion successful", "output": docx_path}
    except Exception as e:
        return {"error": f"Failed to convert PDF to DOCX: {str(e)}"}