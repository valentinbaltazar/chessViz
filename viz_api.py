"""API to serve relevant plots"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import requests

import matplotlib.pyplot as plt
import io
import pandas as pd

from profile_plots import plot_elo

app = FastAPI()


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow your React app's origin
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


class PlotType(BaseModel):
    selectedOption: str



@app.get("/get-plot")
async def get_plot(option: str):
    df = pd.read_csv('./player_data/river650.csv')
    print(df.head())
   
    fig =  plot_elo(df, 'rapid', '1800')
    
    # Save plot to a bytes buffer
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)  # Close the figure to free up memory
  
    if option == 'Option 1':
        return StreamingResponse(buf, media_type="image/png")
    else:
        return "Not Option 1"
 
    
  

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)