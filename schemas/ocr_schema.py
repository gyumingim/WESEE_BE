from pydantic import BaseModel

class OCRRequest(BaseModel):
    image: str