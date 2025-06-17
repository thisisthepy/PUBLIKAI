import sys


if sys.argv[1] == "run" and sys.argv[2] == "server":
    try:
        from api.src.main.server import uvicorn
        server_object = "api.src.main.server:app"
    except ImportError:
        from src.main.server import uvicorn
        server_object = "src.main.server:app"
    host = sys.argv[3] if len(sys.argv) > 3 else "0.0.0.0"
    port = int(sys.argv[4]) if len(sys.argv) > 4 else 23100
    uvicorn.run(
        server_object, host=host, port=port, reload=True,
        ws_ping_interval=300, ws_ping_timeout=300, ws_per_message_deflate=False
    )
