#!/usr/bin/env python3
"""
Trello Sync CLI for ParcInfo

Features:
- Authenticate using Trello API key and token from a JSON config
- Select a board and lists via IDs configured in the JSON config
- Create or update cards from simple task definitions (title, description, status)
- Map local statuses to Trello lists (e.g., todo -> To Do, doing -> In Progress, done -> Done)

Usage examples:
  python scripts/trello_sync.py init --config scripts/trello_config.json
  python scripts/trello_sync.py push-tasks tasks.json --config scripts/trello_config.json
  python scripts/trello_sync.py list-boards --config scripts/trello_config.json

Notes:
- Requires the 'requests' package: pip install requests
- Generate API credentials at https://trello.com/app-key and create a token for your account
"""

import argparse
import json
import os
import sys
from typing import Any, Dict, List, Optional

try:
    import requests
except Exception as exc:  # pragma: no cover - keep lightweight
    print("Missing dependency 'requests'. Install with: pip install requests", file=sys.stderr)
    raise


TRELLO_API_BASE = "https://api.trello.com/1"


class TrelloClient:
    def __init__(self, api_key: str, token: str):
        self.api_key = api_key
        self.token = token

    def _auth_params(self) -> Dict[str, str]:
        return {"key": self.api_key, "token": self.token}

    def get_member(self, username: str = "me") -> Dict[str, Any]:
        url = f"{TRELLO_API_BASE}/members/{username}"
        resp = requests.get(url, params=self._auth_params(), timeout=30)
        resp.raise_for_status()
        return resp.json()

    def list_boards(self) -> List[Dict[str, Any]]:
        url = f"{TRELLO_API_BASE}/members/me/boards"
        resp = requests.get(url, params=self._auth_params(), timeout=30)
        resp.raise_for_status()
        return resp.json()

    def list_lists(self, board_id: str) -> List[Dict[str, Any]]:
        url = f"{TRELLO_API_BASE}/boards/{board_id}/lists"
        resp = requests.get(url, params=self._auth_params(), timeout=30)
        resp.raise_for_status()
        return resp.json()

    def list_cards(self, board_id: str) -> List[Dict[str, Any]]:
        url = f"{TRELLO_API_BASE}/boards/{board_id}/cards"
        resp = requests.get(url, params=self._auth_params(), timeout=30)
        resp.raise_for_status()
        return resp.json()

    def create_card(self, list_id: str, name: str, desc: str = "", labels: Optional[List[str]] = None) -> Dict[str, Any]:
        url = f"{TRELLO_API_BASE}/cards"
        params: Dict[str, Any] = {"idList": list_id, "name": name, "desc": desc, **self._auth_params()}
        if labels:
            params["idLabels"] = ",".join(labels)
        resp = requests.post(url, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def update_card(self, card_id: str, list_id: Optional[str] = None, name: Optional[str] = None, desc: Optional[str] = None) -> Dict[str, Any]:
        url = f"{TRELLO_API_BASE}/cards/{card_id}"
        params: Dict[str, Any] = {**self._auth_params()}
        if list_id:
            params["idList"] = list_id
        if name:
            params["name"] = name
        if desc is not None:
            params["desc"] = desc
        resp = requests.put(url, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()


def load_config(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(path: str, data: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def cmd_init(args: argparse.Namespace) -> None:
    if os.path.exists(args.config) and not args.force:
        print(f"Config already exists at {args.config}. Use --force to overwrite.")
        return
    example = {
        "api_key": "YOUR_TRELLO_API_KEY",
        "token": "YOUR_TRELLO_TOKEN",
        "board_id": "",
        "status_to_list": {
            "todo": "",
            "doing": "",
            "done": ""
        }
    }
    save_config(args.config, example)
    print(f"Wrote example config to {args.config}")


def ensure_client(cfg: Dict[str, Any]) -> TrelloClient:
    api_key = cfg.get("api_key")
    token = cfg.get("token")
    if not api_key or not token:
        raise ValueError("api_key and token must be set in the config file")
    return TrelloClient(api_key=api_key, token=token)


def cmd_list_boards(args: argparse.Namespace) -> None:
    cfg = load_config(args.config)
    client = ensure_client(cfg)
    boards = client.list_boards()
    for b in boards:
        print(f"{b.get('name')}\t{b.get('id')}")


def cmd_list_lists(args: argparse.Namespace) -> None:
    cfg = load_config(args.config)
    client = ensure_client(cfg)
    board_id = cfg.get("board_id") or args.board
    if not board_id:
        raise ValueError("Provide --board or set board_id in config")
    lists = client.list_lists(board_id)
    for l in lists:
        print(f"{l.get('name')}\t{l.get('id')}")


def read_tasks(path: str) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("tasks file must be a JSON array of objects")
    return data


def cmd_push_tasks(args: argparse.Namespace) -> None:
    cfg = load_config(args.config)
    client = ensure_client(cfg)
    board_id = cfg.get("board_id")
    status_to_list: Dict[str, str] = cfg.get("status_to_list", {})
    if not board_id:
        raise ValueError("board_id must be set in config")
    tasks = read_tasks(args.tasks)

    # Cache existing cards to match by name
    existing_cards = client.list_cards(board_id)
    name_to_card: Dict[str, Dict[str, Any]] = {c.get("name", ""): c for c in existing_cards}

    for t in tasks:
        title = t.get("title") or t.get("name")
        desc = t.get("description", "")
        status = (t.get("status") or "todo").lower()
        if not title:
            print("Skipping task without title/name", file=sys.stderr)
            continue
        list_id = status_to_list.get(status)
        if not list_id:
            raise ValueError(f"No Trello list configured for status '{status}'")
        existing = name_to_card.get(title)
        if existing:
            client.update_card(existing.get("id"), list_id=list_id, name=title, desc=desc)
            print(f"Updated: {title} -> list {list_id}")
        else:
            created = client.create_card(list_id=list_id, name=title, desc=desc)
            print(f"Created: {title} (id {created.get('id')})")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="ParcInfo Trello Sync")
    p.add_argument("--config", default="scripts/trello_config.json", help="Path to Trello config JSON")

    sub = p.add_subparsers(dest="command", required=True)

    sp_init = sub.add_parser("init", help="Write example config JSON")
    sp_init.add_argument("--force", action="store_true")
    sp_init.set_defaults(func=cmd_init)

    sp_lb = sub.add_parser("list-boards", help="List Trello boards for the token")
    sp_lb.set_defaults(func=cmd_list_boards)

    sp_ll = sub.add_parser("list-lists", help="List lists for a board")
    sp_ll.add_argument("--board", help="Board ID (falls back to config.board_id)")
    sp_ll.set_defaults(func=cmd_list_lists)

    sp_push = sub.add_parser("push-tasks", help="Create/update cards from a JSON tasks file")
    sp_push.add_argument("tasks", help="Path to JSON array of tasks: [{title, description, status}]")
    sp_push.set_defaults(func=cmd_push_tasks)

    return p


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        args.func(args)
        return 0
    except Exception as exc:  # keep CLI friendly
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())


