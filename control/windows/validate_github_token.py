"""Validate a PAT received only over stdin; never print its value."""
from __future__ import annotations

import sys
from urllib import error, request


def main() -> int:
    token = sys.stdin.buffer.read().decode("utf-8").strip()
    if not token:
        print("GITHUB_API_401")
        return 1
    req = request.Request(
        "https://api.github.com/user",
        headers={
            "Authorization": "Bearer " + token,
            "Accept": "application/vnd.github+json",
            "User-Agent": "MATA-Local-Watcher-Setup",
        },
    )
    try:
        with request.urlopen(req, timeout=30) as response:
            if response.status == 200:
                print("GITHUB_API_OK")
                return 0
            print("GITHUB_API_" + str(response.status))
            return 1
    except error.HTTPError as exc:
        print("GITHUB_API_" + str(exc.code))
    except (error.URLError, TimeoutError):
        print("GITHUB_API_NETWORK_ERROR")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
