# Backend: FastAPI implementation with improved error handling
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import os
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Request model
class DataRequest(BaseModel):
    data: List[str]

# User details
USER_DETAILS = {
    "user_id": "honey_paptan",
    "email": "22bai71414@cuchd.in",
    "roll_number": "22BAI71414"
}
#get
@app.get("/bfhl")
def get_operation_code():
    return {"operation_code": 1}
#post
@app.post("/bfhl")
def process_data(request: DataRequest):
    try:
        if not isinstance(request.data, list) or not all(isinstance(item, str) for item in request.data):
            raise HTTPException(status_code=400, detail="Invalid format: 'data' must be an array of strings.")

        numbers = [item for item in request.data if item.isdigit()]
        alphabets = [item for item in request.data if item.isalpha()]
        highest_alphabet = [max(alphabets, key=str.upper)] if alphabets else []

        response = {
            "is_success": True,
            **USER_DETAILS,
            "numbers": numbers,
            "alphabets": alphabets,
            "highest_alphabet": highest_alphabet
        }
        return response

    except ValidationError as e:
        raise HTTPException(status_code=422, detail="Invalid request format.") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# Running the server locally
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000)) 
    uvicorn.run(app, host="0.0.0.0", port=port)
