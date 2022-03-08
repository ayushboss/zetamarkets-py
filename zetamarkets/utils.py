from anchorpy import Idl, Program
from typing import Dict


def default_commitment() -> Dict:
    return {
        "skipPreflight": False,
        "preflightCommitment": "confirmed",
        "commitment": "confirmed",
    }
