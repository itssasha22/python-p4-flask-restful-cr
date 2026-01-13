# Re-export models from root models.py
from models import db, Newsletter

__all__ = ['db', 'Newsletter']
