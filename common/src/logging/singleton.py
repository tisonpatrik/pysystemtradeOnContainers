"""
Singleton Meta Module
---------------------
This module contains the SingletonMeta class, a thread-safe implementation of
the Singleton design pattern. The SingletonMeta class ensures that a class
has only one instance and provides a global point to access it.
"""

from threading import Lock
from typing import Any, Type


class SingletonMeta(type):
	"""
	This is a thread-safe implementation of Singleton.
	"""

	_instances: dict[Type[Any], Any] = {}

	_lock: Lock = Lock()

	def __call__(cls, *args, **kwargs):
		with cls._lock:
			if cls not in cls._instances:
				instance = super().__call__(*args, **kwargs)
				cls._instances[cls] = instance
		return cls._instances[cls]
