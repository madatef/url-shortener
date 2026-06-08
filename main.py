from fastapi import FastAPI


app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=5000,
        reload=True,
        access_log=True,
        reload_dirs=["app"],
        reload_includes=["*.py", "*.html", "*.css", "*.js"],
        reload_excludes=["*.pyc", "*.pyo", "*.pyd", "*.pyw", "*.pyz", "*.pywz", "*.pyzw"],
        reload_delay=0.5,
    )
