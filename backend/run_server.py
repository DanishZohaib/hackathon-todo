#!/usr/bin/env python3
"""
Script to run the Todo API server
"""

import uvicorn
import sys
import os

# Add the src directory to the path so imports work correctly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    print("Starting Todo API Server...")
    print("Visit http://localhost:8000 for API documentation")
    print("Press Ctrl+C to stop the server")

    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["src"],
        log_level="info"
    )