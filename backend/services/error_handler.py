"""
Error handling & logging service
Centralizované error handling pre ILUMINATI SYSTEM
"""

import logging
import traceback
from typing import Optional, Dict, Any
from datetime import datetime
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import requests

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/iluminati.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("iluminati")


class IluminatiException(Exception):
    """Base exception pre ILUMINATI SYSTEM"""
    def __init__(self, message: str, code: str = "UNKNOWN_ERROR", status_code: int = 500):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(self.message)


class APIError(IluminatiException):
    """API related errors"""
    pass


class DatabaseError(IluminatiException):
    """Database related errors"""
    pass


class ExternalAPIError(IluminatiException):
    """External API errors (ARES, RPO, etc.)"""
    pass


def log_error(error: Exception, context: Optional[Dict[str, Any]] = None, request: Optional[Request] = None):
    """
    Loguje error s kontextom.
    
    Args:
        error: Exception objekt
        context: Dodatočný kontext (dict)
        request: FastAPI Request objekt
    """
    error_info = {
        "error_type": type(error).__name__,
        "error_message": str(error),
        "traceback": traceback.format_exc(),
        "timestamp": datetime.now().isoformat(),
        "context": context or {}
    }
    
    if request:
        error_info["request"] = {
            "url": str(request.url),
            "method": request.method,
            "client": request.client.host if request.client else None,
            "headers": dict(request.headers)
        }
    
    logger.error(f"Error occurred: {error_info}")
    
    # V produkcii by sme tu poslali do Sentry
    # sentry_sdk.capture_exception(error, contexts={"custom": error_info})


async def error_handler(request: Request, exc: Exception):
    """
    Global error handler pre FastAPI.
    
    Použitie:
        app.add_exception_handler(Exception, error_handler)
    """
    # Log error
    log_error(exc, request=request)
    
    # Vrátiť user-friendly error response
    if isinstance(exc, IluminatiException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": True,
                "code": exc.code,
                "message": exc.message,
                "timestamp": datetime.now().isoformat()
            }
        )
    elif isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": True,
                "code": "HTTP_ERROR",
                "message": exc.detail,
                "timestamp": datetime.now().isoformat()
            }
        )
    else:
        # Generic error
        return JSONResponse(
            status_code=500,
            content={
                "error": True,
                "code": "INTERNAL_ERROR",
                "message": "Vnútorná chyba servera. Skúste to znova neskôr.",
                "timestamp": datetime.now().isoformat()
            }
        )


def safe_api_call(func, *args, **kwargs):
    """
    Bezpečné volanie externého API s error handlingom.
    
    Returns:
        Tuple (result, error)
    """
    try:
        result = func(*args, **kwargs)
        return result, None
    except requests.exceptions.RequestException as e:
        error = ExternalAPIError(
            message=f"Chyba pri volaní externého API: {str(e)}",
            code="EXTERNAL_API_ERROR",
            status_code=502
        )
        log_error(error, context={"function": func.__name__, "args": args, "kwargs": kwargs})
        return None, error
    except Exception as e:
        error = APIError(
            message=f"Neočakávaná chyba: {str(e)}",
            code="UNEXPECTED_ERROR",
            status_code=500
        )
        log_error(error, context={"function": func.__name__, "args": args, "kwargs": kwargs})
        return None, error


def safe_database_call(func, *args, **kwargs):
    """
    Bezpečné volanie databázy s error handlingom.
    
    Returns:
        Tuple (result, error)
    """
    try:
        result = func(*args, **kwargs)
        return result, None
    except Exception as e:
        error = DatabaseError(
            message=f"Chyba pri prístupe k databáze: {str(e)}",
            code="DATABASE_ERROR",
            status_code=503
        )
        log_error(error, context={"function": func.__name__, "args": args, "kwargs": kwargs})
        return None, error

