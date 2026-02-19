"""Drowsy Driver Detection Package"""

__all__ = ['run']


def run():
    """Run the drowsy driver detection application"""
    from .app import run as _run
    return _run()
