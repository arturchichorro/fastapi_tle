from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from satellite import get_satellite_position, InvalidTLEError
from typing import Optional

class TLERequest(BaseModel):
    line1: str
    line2: str
    timestamp: Optional[datetime] = None

class PositionResponse(BaseModel):
    x: float
    y: float
    z: float

app = FastAPI()

@app.post("/position", response_model=PositionResponse)
def get_position(data: TLERequest):
    try:
        position = get_satellite_position(data.line1, data.line2, data.timestamp)
        return PositionResponse(x=position[0], y=position[1], z=position[2])
    except InvalidTLEError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {e}")
    except Exception:
        raise HTTPException(status_code=500, detail="An unexpected error occurred while computing the satellite position.")
