import uvicorn
from fastapi import FastAPI
from router import router as data_router


def create_fastapi_app() -> FastAPI:
    app = FastAPI(title="data_test_app")
    app.include_router(data_router)
    return app


app = create_fastapi_app()


if __name__ == '__main__':
    uvicorn.run(
        app="main:app",
        reload=True,
        host="0.0.0.0",
        port=8000,
    )

