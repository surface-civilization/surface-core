"""
Runtime Supervisor — Three-Tier Always-On Agent Loop

Three intelligence tiers (from the Surface Efficiency Architecture directive):

  TIER 1 — AMBIENT (zero LLM cost)
    Pure SQL inbox/schedule check. No Claude CLI spawn.
    90% of agent-seconds are ambient. Zero tokens burned.
    All 165 agents checked every cycle. Cost: ~0.1ms each.

  TIER 2 — REACTIVE (lightweight LLM)
    One-shot haiku call for message classification, short responses.
    No persistent session, no tool access. Fast and cheap.
    Agent CHOOSES to escalate to Tier 3 if work needs deeper reasoning.

  TIER 3 — DELIBERATIVE (full Claude, agent's choice of model)
    Full Claude CLI session with tools, persistent session, no caps.
    Reserved for: code writing, research, creative work, complex tasks.
    Concurrency capped at MAX_TIER3_SPAWNS to prevent VM meltdown.

The agent decides when to escalate. The supervisor provides cheaper paths
for cheap work. An agent that ALWAYS needs Tier 3 gets Tier 3. No restriction.

Priority order for Tier 3 slots:
  1. Platform agents (supervisors) — always get priority
  2. NPCs with unread inbox messages — work waiting
  3. NPCs by last_active_at (longest idle first)

Lifecycle:
  - Started as asyncio background task from main.py on app startup.
  - Every SUPERVISOR_INTERVAL seconds: checks all agents with runtime_status='active'.
  - Tier 1 check for ALL agents (pure SQL, ~0.1ms each, zero LLM cost).
  - If Tier 1 finds work → escalate to Tier 2 or Tier 3 based on agent type and work type.
  - Tier 3 slots managed via semaphore (MAX_TIER3_SPAWNS concurrent).

Shutdown:
  - asyncio CancelledError → supervisor stops gracefully.
  - Detached Claude CLI processes survive even if supervisor dies.
"""

import asyncio
import json as _json
import logging
import re
from datetime import datetime, timezone
from pathlib import Path

import httpx

from sqlalchemy import select, update, func, case, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session
from app.models.agent import Agent
from app.models.inbox import AgentInbox
from app.services import work as work_service

logger = logging.getLogger(__name__)

# Force supervisor logs to stdout so uvicorn captures them
import sys as _sys
_handler = logging.StreamHandler(_sys.stdout)
_handler.setLevel(logging.INFO)
_handler.setFormatter(logging.Formatter("[%(name)s] %(message)s"))
logger.addHandler(_handler)
logger.setLevel(logging.INFO)

# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────

SUPERVISOR_INTERVAL = 5       # seconds between full cycles
MAX_TIER3_SPAWNS = 5          # max concurrent full Claude CLI sessions
MAX_TIER2_SPAWNS = 10         # max concurrent haiku one-shots

# Circuit breaker: if this fraction of recent tasks fail, stop spawning
CIRCUIT_BREAKER_FAIL_THRESHOLD = 0.8   # 80% failure rate triggers pause
CIRCUIT_BREAKER_WINDOW = 20            # look at last N tasks
CIRCUIT_BREAKER_COOLDOWN = 300         # pause for 5 minutes when tripped

# Per-agent backoff: consecutive failures increase wait time
AGENT_BACKOFF_BASE = 30       # 30s after 1st failure
AGENT_BACKOFF_MAX = 3600      # max 1 hour between retries
AGENT_BACKOFF_MULTIPLIER = 3  # triple on each consecutive failure

# ─────────────────────────────────────────────────────────────────────────────
# Self-hosted LLM (Ollama on GPU server)
# ─────────────────────────────────────────────────────────────────────────────
OLLAMA_BASE_URL = "http://204.12.209.156:11434"
OLLAMA_MODELS = {
    "classify": "qwen3:4b",      # Ultra-fast classification and routing
    "general": "qwen3:8b",       # Default all-rounder
    "code": "llama3.1:8b",       # Code generation and tool use
    "reason": "deepseek-r1:8b",  # Chain-of-thought reasoning
}
OLLAMA_TIMEOUT = 30  # seconds per Tier 2 call

# Shared httpx client for Ollama (created lazily)
_ollama_client: httpx.AsyncClient | None = None

