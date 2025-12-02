import requests
from app.core.settings import settings
from app.schemas.jira_schema import JiraResponse

class JiraClient:
    def __init__(self):
        if not settings.jira_domain or not settings.jira_email or not settings.jira_api_token:
            raise ValueError("Jira settings not configured. Please add them in /settings.")

        self.base_url = f"https://{settings.jira_domain}/rest/api/3/issue"
        self.auth = (settings.jira_email, settings.jira_api_token)
        self.headers = {"Accept": "application/json"}

    def fetch_ticket(self, ticket_id: str) -> JiraResponse:
        url = f"{self.base_url}/{ticket_id}"

        response = requests.get(url, headers=self.headers, auth=self.auth)

        # Log response for debugging
        print("STATUS:", response.status_code)
        print("RAW RESPONSE:", response.text)

        # Handle known Jira errors
        if response.status_code == 401:
            raise ValueError("Unauthorized — invalid Jira email or API token.")

        if response.status_code == 404:
            raise ValueError(f"Ticket '{ticket_id}' not found on Jira.")

        if response.status_code != 200:
            raise ValueError(
                f"Jira API error ({response.status_code}): {response.text}"
            )

        # Safe JSON parsing (fixes NoneType errors)
        try:
            data = response.json()
        except Exception:
            raise ValueError(f"Jira returned non-JSON response: {response.text}")

        if not isinstance(data, dict):
            raise ValueError("Invalid Jira JSON format.")

        fields = data.get("fields")
        if fields is None:
            raise ValueError("Jira response missing 'fields' key.")

        return JiraResponse(
            ticket_id=ticket_id,
            project=(fields.get("project") or {}).get("key"),
            summary=fields.get("summary", ""),
            description=(fields.get("description") or {}).get("content", []),
            raw_description=fields.get("description"),
            acceptance_criteria=self.extract_acceptance_criteria(fields)
        )

    def extract_acceptance_criteria(self, fields):
        for key, value in fields.items():
            if "acceptance" in key.lower():
                return value
        return None
