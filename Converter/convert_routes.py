import time
import threading
from fastapi import APIRouter,UploadFile,File,HTTPException,Depends,status,BackgroundTasks
import os
import shutil,uuid
from fastapi.responses import FileResponse
import converting
from oauth2 import Authentication

auth=Authentication()
router= APIRouter()

UPLOAD_DIR="uploads"
os.makedirs(UPLOAD_DIR,exist_ok=True)

def delayed_delete(file_path):
    # ye function banaye h ki user download kiya toh delte karo warna 10 sec k bad delete krdo
    time.sleep(180)  # Wait before deleting the file for atleast 10 secs
    if os.path.exists(file_path):  # Check kro ki file exixt karti h ya nahi agar krti h toh remove krdo
        os.remove(file_path)

@router.post("/docx-to-pdf")
def docx_to_pdf(file: UploadFile= File(...), user: dict =Depends(auth.get_current_user)) :
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized. Please log in first."
        )
    
    if not file.filename.endswith(".docx"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only Docx files are allowed")
    
    file_id = str(uuid.uuid4()) # Har file ko ek unique id dega 
    docx_path= os.path.join(UPLOAD_DIR,f"{file_id}.docx")
    pdf_path= os.path.join(UPLOAD_DIR,f"{file_id}.pdf")

    with open(docx_path, "wb") as buffer :
        shutil.copyfileobj(file.file,buffer)  # PDF file server ke uploads folder me save karega

    result= converting.convert_docx_to_pdf(docx_path, pdf_path)

    if "error" in result :
        return{"error" : result["error"]}
    
    return {
        #Ye return karega file_id jo ki frontend mai kaam ayega and redirect karega download p and file_id ko paste krdega 
        "file_id": file_id,
        "download_url": f"/download/{file_id}"
    }
   
@router.post("/pdf-to-docx")
def pdf_to_docx(file: UploadFile= File(...), user: dict =Depends(auth.get_current_user)) :

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized. Please log in first."
        )
    
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only PDF files are allowed")
    
    file_id = str(uuid.uuid4()) # Har file ko ek unique id dega 
    pdf_path = os.path.join(UPLOAD_DIR, f"{file_id}.pdf")
    docx_path = os.path.join(UPLOAD_DIR, f"{file_id}.docx")
    
    with open(pdf_path, "wb") as buffer :
        shutil.copyfileobj(file.file,buffer) # PDF file server ke uploads folder me save karega

    result= converting.convert_pdf_to_docx(pdf_path, docx_path)

    if "error" in result :
        return{"error" : result["error"]}
    

    return {
        "file_id": file_id,
        "download_url": f"/download/{file_id}"
    }
    
  

@router.get("/download/{file_id}")
def download_file(file_id: str, background_tasks: BackgroundTasks):
    pdf_path = os.path.join(UPLOAD_DIR, f"{file_id}.pdf")
    docx_path = os.path.join(UPLOAD_DIR, f"{file_id}.docx")

    if os.path.exists(pdf_path):
        print(f"Downloading: {pdf_path}")  # Debugging ke liye
        background_tasks.add_task(delayed_delete, pdf_path)  # File delete ka task background me
        return FileResponse(pdf_path, filename=f"{file_id}.pdf", media_type="application/pdf")
    
    elif os.path.exists(docx_path):
        print(f"Downloading: {docx_path}")  # Debugging ke liye
        background_tasks.add_task(delayed_delete, docx_path)  # File delete ka task background me
        return FileResponse(docx_path, filename=f"{file_id}.docx", media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    
    else:
        raise HTTPException(status_code=404, detail="File not found")
