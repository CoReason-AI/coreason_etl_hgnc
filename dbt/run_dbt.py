import sys
import warnings
from typing import Any

# Silence the Pydantic V1 3.14 compatibility warning
warnings.filterwarnings("ignore", category=UserWarning)

# --- PYTHON 3.14 CYTHON & TYPE PARSING BYPASS ---
import pydantic.v1
import pydantic.v1.fields
import pydantic.v1.errors

# 1. Force Pydantic V1 to accept unrecognized Python 3.14 types globally
pydantic.v1.BaseConfig.arbitrary_types_allowed = True

# 2. Specifically target dbt-semantic-interfaces base model
try:
    from dbt_semantic_interfaces.implementations.base import HashableBaseModel
    if hasattr(HashableBaseModel, "Config"):
        HashableBaseModel.Config.arbitrary_types_allowed = True
except Exception:
    pass

# 3. Catch the ConfigError mid-air and manually construct the field state
_original_set_default_and_type = pydantic.v1.fields.ModelField._set_default_and_type

def _patched_set_default_and_type(self):
    try:
        # Let Pydantic attempt normal behavior
        _original_set_default_and_type(self)
    except pydantic.v1.errors.ConfigError as e:
        if "default_factory" in str(e):
            # The crash happened! Manually stitch the field together 
            # as if Pydantic successfully parsed it.
            self.type_ = Any
            self.outer_type_ = Any
            self.required = False
            self.allow_none = True
        else:
            raise

pydantic.v1.fields.ModelField._set_default_and_type = _patched_set_default_and_type
# ---------------------------------

from dbt.cli.main import cli

if __name__ == "__main__":
    # Launch the standard dbt CLI
    sys.exit(cli())
