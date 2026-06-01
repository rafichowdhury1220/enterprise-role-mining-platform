"""Enterprise Role Mining Platform

This package exposes the core pipeline and analysis services for enterprise IAM role mining.
"""

from .pipeline import RoleMiningPipeline
from .cli import app

__all__ = ["RoleMiningPipeline", "app"]
