from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="ThreatForge Dashboard", version="1.0.0")

@app.get("/")
async def read_root():
    return HTMLResponse("""
    <html>
        <head>
            <title>ThreatForge Dashboard</title>
        </head>
        <body>
            <h1>ThreatForge Security Dashboard</h1>
            <p>Basic dashboard is working!</p>
            <p>Next: Add full functionality.</p>
        </body>
    </html>
    """)

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "dashboard"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
