"""
Vercel Serverless Function entry point.
Exposes the FastAPI ASGI application for Vercel Python runtime.
"""
import sys
import os

# Add project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.main import app
