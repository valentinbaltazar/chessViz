"""API to serve relevant plots"""
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


import matplotlib.pyplot as plt
import io

from profile_plots import plot_elo, plot_wins
from opening_tree import get_tree

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
    """Get requested plot from Option value"""
    if option == 'Option 1':
        fig = plot_elo('river650', 'rapid', '1800', testing=False)

        # Save plot to a bytes buffer
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        plt.close(fig)  # Close the figure to free up memory
        return StreamingResponse(buf, media_type="image/png")
    elif option == 'Option 2':
        fig = plot_wins('river650')
        
        # Save plot to a bytes buffer
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        plt.close(fig)  # Close the figure to free up memory
        return StreamingResponse(buf, media_type="image/png")
    elif option == 'Option 3':
        return {"tree": get_tree()}
    else:
        return "Not Option 1"
 
    
  

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)