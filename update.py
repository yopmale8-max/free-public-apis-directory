import json
import socket
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parent
API_FILE = ROOT / "data" / "apis.json"
README_FILE = ROOT / "README.md"

README_HEADER = """# 🚀 Awesome Free Public APIs & Webhooks

> A 100% free, automated directory of reliable public APIs, webhooks, and mock endpoints for developers. Updated weekly via GitHub Actions.

[![Sponsored: Your Tool Here](https://img.shields.io/badge/🌟_Sponsored-Get_Your_API_Featured!-blue?style=for-the-badge)](https://your-gumroad-or-stripe-link.com)

## Directory

| API Name | Category | Auth Required? | Status | Endpoint |
| :--- | :--- | :--- | :--- | :--- |
"""


def check_status(url):
    try:
        with urlopen(url, timeout=5) as response:
            return "Active 🟢" if response.status < 400 else "Degraded 🟡"
    except HTTPError:
        return "Degraded 🟡"
    except (URLError, TimeoutError, socket.timeout):
        return "Down 🔴"


def main():
    with API_FILE.open(encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data.get("apis"), list):
        raise ValueError(f"{API_FILE} must contain an 'apis' list.")

    for api in data["apis"]:
        if not isinstance(api, dict) or not isinstance(api.get("url"), str):
            raise ValueError("Each API entry must be an object with a string 'url'.")
        api["status"] = check_status(api["url"])

    with API_FILE.open("w", encoding="utf-8", newline="\n") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
        file.write("\n")

    rows = [
        f"| **{api['name']}** | {api['category']} | {api['auth']} | "
        f"{api['status']} | `{api['url']}` |"
        for api in data["apis"]
    ]
    readme_content = (
        README_HEADER
        + "\n".join(rows)
        + "\n\n*Want your API featured at the top? [Submit a sponsorship inquiry]"
        "(https://your-gumroad-or-stripe-link.com).*\n"
    )
    README_FILE.write_text(readme_content, encoding="utf-8", newline="\n")

    print("Directory updated and README regenerated successfully!")


if __name__ == "__main__":
    main()
