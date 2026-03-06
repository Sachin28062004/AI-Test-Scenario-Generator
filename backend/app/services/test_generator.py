from app.utils.crypto import decrypt_text
from app.database import crud
from openai import OpenAI
from typing import Dict, Any
import json
import re

GROK_BASE_URL = "https://api.x.ai/v1"
GROK_MODEL = "grok-2"


def _get_grok_key(db):
    s = crud.get_settings(db)
    if not s or not s.grok_api_key_enc:
        raise RuntimeError("Grok API key not configured")
    return decrypt_text(s.grok_api_key_enc)


def generate_scenarios_from_description(description: str, title: str, db_session) -> Dict[str, Any]:
    """Generate test scenarios from user-provided description (no Jira)."""
    grok_key = _get_grok_key(db_session)

    client = OpenAI(
        api_key=grok_key,
        base_url=GROK_BASE_URL,
    )

    display_title = title.strip() or "Feature / Requirement"
    prompt = f"""
You are a senior QA lead. Given the feature/requirement description below,
1) Rewrite the description to be concise and unambiguous (enhanced_description).
2) Produce a JSON array of test scenarios covering: Frontend flows, API/backend test cases, DB validations, negative cases, and edge cases.
Return: {{
  "enhanced_description": "...",
  "scenarios": [
    {{
      "id": "T1",
      "type": "frontend|backend|db|security",
      "title": "...",
      "steps": ["..."],
      "expected_result": "..."
    }}
  ]
}}

Title/Feature:
{display_title}

Description:
{description}

Return only valid JSON.
"""
    try:
        resp = client.chat.completions.create(
            model=GROK_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        text = resp.choices[0].message.content

    except Exception as e:
        raise RuntimeError(f"Failed to call Grok API: {e}")

    m = re.search(r"(\{[\s\S]*\}|\[[\s\S]*\])", text)
    if not m:
        raise RuntimeError(f"Failed to parse JSON from Grok response. Raw text: {text[:200]}...")

    json_text = m.group(0)
    parsed = json.loads(json_text)
    return parsed
