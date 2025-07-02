from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import ops, client
import os

app = FastAPI()

# Include routers
app.include_router(ops.router, prefix="/ops", tags=["Ops User"])
app.include_router(client.router, prefix="/client", tags=["Client User"])

# Ensure files directory exists
if not os.path.exists("files"):
    os.makedirs("files")

# Serve uploaded files (for internal use, not direct public access)
app.mount("/files", StaticFiles(directory="files"), name="files") 