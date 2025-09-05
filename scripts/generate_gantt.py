#!/usr/bin/env python3
import os
from datetime import datetime, date
from typing import List, Dict

import matplotlib
matplotlib.use('Agg')  # backend non interactif pour export PDF
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def ensure_docs_dir(project_root: str) -> str:
	output_dir = os.path.join(project_root, 'docs')
	os.makedirs(output_dir, exist_ok=True)
	return output_dir


def build_tasks() -> List[Dict]:
	# Fenêtre projet
	start_july = date(2025, 7, 1)
	end_aug = date(2025, 8, 31)

	# Fenêtre de déploiement sur les jours restants d'août (29–31 août 2025)
	deploy_start = date(2025, 8, 29)
	deploy_end = date(2025, 8, 31)

	# Plan macro en 9 lots (adapté au contenu du repo ParcInfo)
	return [
		{
			'name': 'Cadrage & Conception',
			'group': 'Phase 1',
			'color': '#2563eb',
			'begin': date(2025, 7, 1),
			'end': date(2025, 7, 5),
		},
		{
			'name': 'Fondations Backend (Django, RBAC, modèles)',
			'group': 'Phase 2',
			'color': '#1d4ed8',
			'begin': date(2025, 7, 4),
			'end': date(2025, 7, 12),
		},
		{
			'name': 'Gestion du parc (équipements, fournisseurs, commandes, livraisons)',
			'group': 'Phase 3',
			'color': '#0ea5e9',
			'begin': date(2025, 7, 10),
			'end': date(2025, 7, 22),
		},
		{
			'name': 'Demandes & décharges PDF (workflow, stocks)',
			'group': 'Phase 4',
			'color': '#22c55e',
			'begin': date(2025, 7, 18),
			'end': date(2025, 7, 26),
		},
		{
			'name': 'Notifications garanties & rôles',
			'group': 'Phase 5',
			'color': '#16a34a',
			'begin': date(2025, 7, 24),
			'end': date(2025, 8, 2),
		},
		{
			'name': 'Chatbot RAG + LLM (intégration apps/chatbot)',
			'group': 'Phase 6',
			'color': '#f59e0b',
			'begin': date(2025, 7, 28),
			'end': date(2025, 8, 10),
		},
		{
			'name': 'Dashboards Streamlit garanties (reporting)',
			'group': 'Phase 7',
			'color': '#eab308',
			'begin': date(2025, 8, 5),
			'end': date(2025, 8, 15),
		},
		{
			'name': 'Sécurité, perfs, supervision',
			'group': 'Phase 8',
			'color': '#ef4444',
			'begin': date(2025, 8, 12),
			'end': date(2025, 8, 22),
		},
		{
			'name': 'Recette, formation, documentation',
			'group': 'Phase 9',
			'color': '#a855f7',
			'begin': date(2025, 8, 20),
			'end': date(2025, 8, 28),
		},
		{
			'name': 'Déploiement (fenêtre restante août)',
			'group': 'Go-live',
			'color': '#10b981',
			'begin': deploy_start,
			'end': deploy_end,
		},
	]


def plot_gantt(tasks: List[Dict], project_root: str) -> str:
	output_dir = ensure_docs_dir(project_root)
	pdf_path = os.path.join(output_dir, 'gantt_parcinfo_juillet_aout_2025.pdf')

	# Préparation des bandes
	fig, ax = plt.subplots(figsize=(12, 6), constrained_layout=True)

	# Tri par date de début
	sorted_tasks = sorted(tasks, key=lambda x: x['begin'])
	labels = [t['name'] for t in sorted_tasks]
	y_positions = range(len(sorted_tasks))

	for i, task in enumerate(sorted_tasks):
		start = mdates.date2num(task['begin'])
		end = mdates.date2num(task['end'])
		duration = max(end - start, 1)
		ax.barh(i, duration, left=start, height=0.45, color=task['color'], edgecolor='black', alpha=0.9)
		ax.text(start + duration + 0.2, i, task['group'], va='center', fontsize=8, color='#334155')

	# Mise en forme axes
	ax.set_yticks(list(y_positions))
	ax.set_yticklabels(labels, fontsize=9)
	ax.invert_yaxis()

	# Fenêtre temporelle globale
	project_start = date(2025, 7, 1)
	project_end = date(2025, 8, 31)
	ax.set_xlim(mdates.date2num(project_start), mdates.date2num(project_end))

	# Format dates
	ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO, interval=1))
	ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
	ax.grid(True, axis='x', linestyle='--', alpha=0.3)
	ax.set_title('ParcInfo — Gantt (Juillet–Août 2025) • Déploiement: 29–31 août', fontsize=12, pad=14)
	ax.set_xlabel('Semaines')

	# Légendes simples
	custom_patches = [
		plt.Line2D([0], [0], color='#10b981', lw=8, label='Go-live'),
		plt.Line2D([0], [0], color='#2563eb', lw=8, label='Cadrage/Conception'),
		plt.Line2D([0], [0], color='#1d4ed8', lw=8, label='Backend'),
		plt.Line2D([0], [0], color='#0ea5e9', lw=8, label='Parc/Commandes/Livraisons'),
		plt.Line2D([0], [0], color='#22c55e', lw=8, label='Demandes & PDF'),
		plt.Line2D([0], [0], color='#f59e0b', lw=8, label='Chatbot RAG+LLM'),
		plt.Line2D([0], [0], color='#eab308', lw=8, label='Dashboards Streamlit'),
		plt.Line2D([0], [0], color='#ef4444', lw=8, label='Sécurité & Perfs'),
		plt.Line2D([0], [0], color='#a855f7', lw=8, label='Recette/Formation'),
	]
	ax.legend(handles=custom_patches, loc='lower right', fontsize=8, frameon=False)

	# Export PDF
	fig.savefig(pdf_path, format='pdf')
	plt.close(fig)
	return pdf_path


def main():
	project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
	tasks = build_tasks()
	pdf_path = plot_gantt(tasks, project_root)
	print(f"✅ Gantt généré: {pdf_path}")


if __name__ == '__main__':
	main()
