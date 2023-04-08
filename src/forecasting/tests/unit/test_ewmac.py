import pytest
import asyncio
from pandas import DataFrame
from unittest.mock import MagicMock

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from forecasting.src.ewmac.ewmac import compute_ewmac, process_record

