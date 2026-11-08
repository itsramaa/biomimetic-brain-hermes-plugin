"""Agent directory resolution.

The kit never assumes a name. Resolution order:
  1. $MIND_AGENT_DIR
  2. --agent-dir on the command line
  3. ./agent  (relative to the kit root)
"""
from __future__ import annotations
import os, sys
from pathlib import Path


def agent_dir() -> Path:
    for i, arg in enumerate(sys.argv):
        if arg == "--agent-dir" and i + 1 < len(sys.argv):
            return Path(sys.argv[i + 1]).expanduser().resolve()
        if arg.startswith("--agent-dir="):
            return Path(arg.split("=", 1)[1]).expanduser().resolve()
    env = os.environ.get("MIND_AGENT_DIR")
    if env:
        return Path(env).expanduser().resolve()

    # 3. Profile-scoped brain path (Komponen 6 Multi-Profile)
    try:
        common_dir = Path(__file__).resolve().parent.parent.parent / "common"
        if str(common_dir.parent) not in sys.path:
            sys.path.insert(0, str(common_dir.parent))
        from common.profile_resolver import get_profile_dir
        profile_brain_dir = get_profile_dir() / "brain"
        if profile_brain_dir.is_dir():
            return profile_brain_dir.resolve()
    except Exception:
        pass

    return (Path(__file__).resolve().parent.parent / "agent")
