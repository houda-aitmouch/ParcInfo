#!/usr/bin/env python3
import os
import sys
import json
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional, Tuple

import requests

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


API_BASE = "https://api.trello.com/1"


def env(key: str, default: Optional[str] = None) -> Optional[str]:
	val = os.environ.get(key, default)
	return val


def require_env(keys: List[str]) -> None:
	missing = [k for k in keys if not env(k)]
	if missing:
		raise SystemExit(
			"Variables d'environnement manquantes: " + ", ".join(missing) +
			"\nAttendu: TRELLO_KEY, TRELLO_TOKEN, TRELLO_BOARD_ID"
		)


def ensure_docs_dir(project_root: str) -> str:
	output_dir = os.path.join(project_root, 'docs')
	os.makedirs(output_dir, exist_ok=True)
	return output_dir


def trello_get(endpoint: str, params: Dict = None) -> any:
	params = params or {}
	params.update({
		'key': env('TRELLO_KEY'),
		'token': env('TRELLO_TOKEN')
	})
	url = f"{API_BASE}{endpoint}"
	r = requests.get(url, params=params, timeout=20)
	r.raise_for_status()
	return r.json()


def fetch_board_data(board_id: str) -> Tuple[List[Dict], Dict[str, str]]:
	# Cartes avec champs utiles (start, due, list, labels)
	cards = trello_get(
		f"/boards/{board_id}/cards",
		params={
			'fields': 'name,due,start,idList,labels,url,dateLastActivity',
			'memberships': 'none'
		}
	)
	# Noms des listes
	lists = trello_get(f"/boards/{board_id}/lists", params={'fields': 'name'})
	list_id_to_name = {l['id']: l['name'] for l in lists}
	return cards, list_id_to_name


def parse_date(d: Optional[str]) -> Optional[date]:
	if not d:
		return None
	try:
		# Trello returns ISO 8601
		dt = datetime.fromisoformat(d.replace('Z', '+00:00'))
		return dt.date()
	except Exception:
		return None


def derive_dates(card: Dict) -> Tuple[date, date]:
	"""Derive start/end dates. If start missing, fallback to (due - 7j) or lastActivity - 3j, else today."""
	start = parse_date(card.get('start'))
	due = parse_date(card.get('due'))
	if not start and due:
		start = due - timedelta(days=7)
	if not due and start:
		due = start + timedelta(days=3)
	if not start and not due:
		last = parse_date(card.get('dateLastActivity'))
		base = last or date.today()
		start = base
		due = base + timedelta(days=2)
	# Ensure start <= due
	if start > due:
		start, due = due, start
	return start, due


def build_tasks_from_trello(cards: List[Dict], list_id_to_name: Dict[str, str]) -> List[Dict]:
	COLOR_BY_LIST = {
		'Todo': '#94a3b8',
		'Doing': '#f59e0b',
		'In Progress': '#f59e0b',
		'Done': '#10b981',
	}
	default_color = '#2563eb'
	tasks = []
	for c in cards:
		start, end = derive_dates(c)
		list_name = list_id_to_name.get(c.get('idList', ''), 'Other')
		color = COLOR_BY_LIST.get(list_name, default_color)
		label_names = [lbl.get('name') for lbl in (c.get('labels') or []) if lbl.get('name')]
		name = c.get('name', 'Sans titre')
		group = list_name
		tasks.append({
			'name': name,
			'group': group,
			'color': color,
			'begin': start,
			'end': end,
			'url': c.get('url'),
			'labels': label_names,
		})
	return tasks


def plot_gantt(tasks: List[Dict], project_root: str, title_suffix: str = '') -> str:
	output_dir = ensure_docs_dir(project_root)
	pdf_path = os.path.join(output_dir, f'gantt_trello{title_suffix}.pdf')

	fig, ax = plt.subplots(figsize=(12, max(4, 0.4 * len(tasks) + 2)), constrained_layout=True)

	sorted_tasks = sorted(tasks, key=lambda x: (x['begin'], x['end']))
	labels = [t['name'] for t in sorted_tasks]

	for i, task in enumerate(sorted_tasks):
		start = mdates.date2num(task['begin'])
		end = mdates.date2num(task['end'])
		duration = max(end - start, 0.5)
		ax.barh(i, duration, left=start, height=0.45, color=task['color'], edgecolor='black', alpha=0.9)
		# Afficher la liste (groupe) à droite
		ax.text(start + duration + 0.2, i, task['group'], va='center', fontsize=8, color='#334155')

	ax.set_yticks(list(range(len(sorted_tasks))))
	ax.set_yticklabels(labels, fontsize=9)
	ax.invert_yaxis()

	if sorted_tasks:
		min_start = min(t['begin'] for t in sorted_tasks)
		max_end = max(t['end'] for t in sorted_tasks)
		ax.set_xlim(mdates.date2num(min_start - timedelta(days=1)), mdates.date2num(max_end + timedelta(days=1)))

	ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO, interval=1))
	ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
	ax.grid(True, axis='x', linestyle='--', alpha=0.3)
	ax.set_title(f"ParcInfo — Gantt Trello {title_suffix}", fontsize=12, pad=14)
	ax.set_xlabel('Semaines')

	legend_handles = [
		plt.Line2D([0], [0], color='#94a3b8', lw=8, label='Todo'),
		plt.Line2D([0], [0], color='#f59e0b', lw=8, label='Doing'),
		plt.Line2D([0], [0], color='#10b981', lw=8, label='Done'),
		plt.Line2D([0], [0], color='#2563eb', lw=8, label='Autres'),
	]
	ax.legend(handles=legend_handles, loc='lower right', fontsize=8, frameon=False)

	fig.savefig(pdf_path, format='pdf')
	plt.close(fig)
	return pdf_path


def main():
	require_env(['TRELLO_KEY', 'TRELLO_TOKEN', 'TRELLO_BOARD_ID'])
	board_id = env('TRELLO_BOARD_ID')
	project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

	cards, list_names = fetch_board_data(board_id)
	tasks = build_tasks_from_trello(cards, list_names)

	# Limiter aux mois de juillet-août si souhaité (optionnel)
	start_filter = date(2025, 7, 1)
	end_filter = date(2025, 8, 31)
	tasks = [t for t in tasks if not (t['end'] < start_filter or t['begin'] > end_filter)]

	pdf_path = plot_gantt(tasks, project_root, title_suffix=' (Juil–Août 2025)')
	print(f"✅ Gantt Trello généré: {pdf_path}")


if __name__ == '__main__':
	main()
