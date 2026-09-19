"""
AETHER Authentication Layer
HMAC-signed session tokens, HttpOnly cookie sessions, env-provisioned operator accounts.
Accounts are configured via environment (AETHER_ADMIN_EMAIL / AETHER_ADMIN_PASSWORD)
with safe demo fallbacks for the hackathon environment.
"""

import os
import time
import hmac
import hashlib
from typing import Optional, Dict, Any

SESSION_COOKIE = "aether_session"
SESSION_TTL_SECONDS = 12 * 3600


def _secret() -> str:
    return os.getenv("SECRET_KEY", "aether-context-layer-hmac-secret-v1")


def _sign(payload: str) -> str:
    return hmac.new(_secret().encode(), payload.encode(), hashlib.sha256).hexdigest()


def issue_token(email: str) -> str:
    expires = int(time.time()) + SESSION_TTL_SECONDS
    payload = f"{email}|{expires}"
    return f"{payload}|{_sign(payload)}"


def verify_token(token: Optional[str]) -> Optional[str]:
    """Returns the authenticated email, or None."""
    if not token:
        return None
    try:
        email, expires, sig = token.rsplit("|", 2)
        payload = f"{email}|{expires}"
        if not hmac.compare_digest(_sign(payload), sig):
            return None
        if int(expires) < time.time():
            return None
        return email
    except Exception:
        return None


def get_accounts() -> Dict[str, Dict[str, Any]]:
    accounts: Dict[str, Dict[str, Any]] = {}
    admin_email = os.getenv("AETHER_ADMIN_EMAIL", "admin@nexus.dev").lower()
    admin_password = os.getenv("AETHER_ADMIN_PASSWORD", "admin123")
    admin_name = os.getenv("AETHER_ADMIN_NAME", "Alex Vance (Hackathon Organizer)")
    accounts[admin_email] = {"password": admin_password, "name": admin_name, "role": "organizer"}
    accounts.setdefault("shiv@nexus.dev", {
        "password": "builder123", "name": "Shiv Sharma", "role": "builder"
    })
    return accounts


def authenticate(email: str, password: str) -> Optional[Dict[str, Any]]:
    acc = get_accounts().get(email.lower().strip())
    if not acc or not hmac.compare_digest(acc["password"], password):
        return None
    return {"email": email.lower().strip(), "name": acc["name"], "role": acc["role"]}
