# coding:utf-8
"""Viking Memory SDK Type Definitions"""

import json
from enum import Enum
from typing import Any


class EnumEncoder(json.JSONEncoder):
    """Enum type JSON encoder"""

    def default(self, obj: Any) -> Any:
        if isinstance(obj, Enum):
            return obj.value
        return super().default(obj)
