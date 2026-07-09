"""StadiumAI entry point.

Starts the uvicorn ASGI server for the StadiumAI FastAPI application.
Reads APP_ENV to determine whether to enable hot-reload.
"""

import os
import uvicorn


def main() -> None:
    """Launch the StadiumAI server."""
    env = os.getenv("APP_ENV", "development")
    reload = env == "development"

    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=reload,
    )


if __name__ == "__main__":
    main()
