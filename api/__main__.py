import sys


if sys.argv[1] == "run" and sys.argv[2] == "server":
    try:
        from api.src.main.server import uvicorn, app
    except ImportError:
        from src.main.server import uvicorn, app
    host = sys.argv[3] if len(sys.argv) > 3 else "0.0.0.0"
    port = int(sys.argv[4]) if len(sys.argv) > 4 else 23100
    uvicorn.run(
        app, host=host, port=port,
        ws_ping_interval=60, ws_ping_timeout=30, ws_per_message_deflate=False, timeout_keep_alive=300
    )
