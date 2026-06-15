from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.api.v0.auth import router as auth_router
from app.core.errors import AppError


app = FastAPI()

@app.exception_handler(AppError)
async def error_handler(_: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'error': {
                'code': exc.code,
                'message': exc.message,
                'field': exc.field,
            }
        }

    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {"status": "ok"}

app.include_router(auth_router, prefix="/api/v0")

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
