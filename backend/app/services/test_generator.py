from app.utils.crypto import decrypt_text
from app.database import crud, database
from google import genai
from typing import Dict, Any
import os
import json
import re

def _get_gemini_key(db):
    s = crud.get_settings(db)
    if not s or not s.gemini_api_key_encrypted:
        raise RuntimeError("Gemini API key not configured")
    return s.gemini_api_key_encrypted


def enhance_description_and_generate_scenarios(jira_data: Dict[str, Any], db_session) -> Dict[str, Any]:
    gemini_key = _get_gemini_key(db_session)
    client = genai.Client(api_key=gemini_key)

    # Compose prompt — tailor as needed
    title = jira_data.get("fields", {}).get("summary")
    raw_description = jira_data.get("fields", {}).get("description") or jira_data.get("description") or ""
    prompt = f"""
You are a senior QA lead. Given the Jira ticket title and description below,
1) Rewrite the description to be concise and unambiguous.
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

Ticket Title:
{title}

Ticket Description:
{raw_description}

Return only valid JSON.
"""
    try:
        resp = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                max_output_tokens=800
            )
        )

        # The response text is accessed directly
        text = resp.text

    except Exception as e:
        raise RuntimeError(f"Failed to call Gemini API: {e}")

    m = re.search(r"(\{[\s\S]*\}|\[[\s\S]*\])", text)
    if not m:
        # Include the raw text in the error for debugging
        raise RuntimeError(f"Failed to parse JSON from Gemini response. Raw text: {text[:200]}...")

    json_text = m.group(0)
    parsed = json.loads(json_text)
    return parsed
