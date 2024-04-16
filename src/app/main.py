import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.core.application:get_application",
        port=8080,
        reload=True,
    )
