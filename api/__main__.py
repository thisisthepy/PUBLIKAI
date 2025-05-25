import sys


if sys.argv[1] == "run" and sys.argv[2] == "server":
    from api.server import uvicorn, app
    host = sys.argv[3] if len(sys.argv) > 3 else "0.0.0.0"
    port = int(sys.argv[4]) if len(sys.argv) > 4 else 8000
    uvicorn.run(app, host=host, port=port)
