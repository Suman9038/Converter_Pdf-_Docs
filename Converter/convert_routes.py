from fastapi import APIRouter,UploadFile,File,HTTPException,Depends,status
import os
import shutil
from fastapi.responses import FileResponse
import converting,oauth2


auth=oauth2.Authentication
router= APIRouter()

UPLOAD_DIR="uploads"
os.makedirs(UPLOAD_DIR,exist_ok=True)

@router.post("/docx-to-pdf")
def docx_to_pdf(file: UploadFile= File(...), user: dict = Depends(auth.get_current_user)) :

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized. Please log in first."
        )
    
    if not file.filename.endswith(".docx"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only Docx files are allowed")
    
    file_path=f"{UPLOAD_DIR}/{file.filename}"  # Upload ki gayi file ka server me path set karega {file.filename ka mtlb h file ka naam upload foldder mai dalna }

    with open(file_path, "wb") as buffer :
        shutil.copyfileobj(file.file,buffer)  # PDF file server ke uploads folder me save karega

    output_pdf= file_path.replace(".docx" , ".pdf")
    result= converting.convert_docx_to_pdf(file_path, output_pdf)

    if "error" in result :
        return{"error" : result["error"]}
    return FileResponse(output_pdf, filename=os.path.basename(output_pdf), media_type="application/pdf")

@router.post("/pdf-to-docx")
def pdf_to_docx(file: UploadFile= File(...),user: dict = Depends(auth.get_current_user)) :

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized. Please log in first."
        )
    
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only PDF files are allowed")
    
    file_path=f"{UPLOAD_DIR}/{file.filename}" # Upload ki gayi file ka server me path set karega

    with open(file_path, "wb") as buffer :
        shutil.copyfileobj(file.file,buffer) # PDF file server ke uploads folder me save karega

    output_docx= file_path.replace(".pdf" , ".docx")
    result= converting.convert_pdf_to_docx(file_path, output_docx)

    if "error" in result :
        return{"error" : result["error"]}
    
    return FileResponse(output_docx, filename=os.path.basename(output_docx), media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")