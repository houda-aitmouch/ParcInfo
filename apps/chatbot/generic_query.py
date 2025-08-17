import re
import unicodedata
from typing import Any, Dict, List, Optional, Tuple

from django.apps import apps as django_apps
from django.db.models import Model, QuerySet, Q, Count, Sum, Avg, Min, Max

try:
    from rapidfuzz import fuzz  # optional for fuzzy alias matching
except Exception:
    fuzz = None

class GenericQueryEngine:
    """
    Very lightweight NL → ORM query engine for read-only exploration across the project's models.

    Supported patterns (French):
    - "liste <modele>" / "affiche <modele>"
    - filtres: "où|dont|avec <champ> (contient|=|>|<|>=|<=|commence|finit) <valeur>"
    - opérateurs: contient → __icontains, commence → __istartswith, finit → __iendswith
    - comptes: "compte <modele>" / "nombre de <modele>"
    - agrégations: "somme de <champ>", "moyenne de <champ>", "min de <champ>", "max de <champ>"
    - tri: "trié par <champ> (asc|desc)" (desc par défaut si "décroissant" trouvé)
    - limite: "top N", "premiers N", "afficher N"

    Limitations:
    - Traverse au plus 1 niveau de ForeignKey via "<fk> <champ>" → fk__champ
    - Sélectionne des champs par défaut; pas de jointures multiples complexes
    - Lecture seule, limite de sécurité MAX_LIMIT
    """

    MAX_LIMIT = 50

    def __init__(self) -> None:
        self.model_registry: Dict[str, Model] = {}
        self.model_aliases: Dict[str, str] = {}
        self.field_aliases: Dict[str, Dict[str, str]] = {}
        self._build_registry()

    def _build_registry(self) -> None:
        models = django_apps.get_models()
        for m in models:
            # Only include project models (located under apps.*)
            module = getattr(m, "__module__", "")
            if not module.startswith("apps."):
                continue
            meta = m._meta
            key = f"{meta.app_label}.{meta.model_name}".lower()
            self.model_registry[key] = m

            # Aliases: model_name, verbose_name, verbose_name_plural, plain words
            names = set()
            # Use CamelCase class name to build human-readable tokens
            class_name = getattr(m, "__name__", meta.model_name)
            tokens = self._split_words(class_name)
            if not tokens:
                tokens = meta.model_name.replace("_", " ").lower().split()
            base_alias = " ".join(tokens)
            names.add(base_alias)
            # Verbose names
            if meta.verbose_name:
                names.add(self._normalize_text(str(meta.verbose_name)))
            if meta.verbose_name_plural:
                names.add(self._normalize_text(str(meta.verbose_name_plural)))
            # App + model combinations
            names.add(self._normalize_text(f"{meta.app_label} {base_alias}"))
            names.add(self._normalize_text(f"{base_alias} {meta.app_label}"))
            # Add common French 'de' variants and basic plurals
            names.update(self._alias_variants(tokens))

            # Add special synonyms for common domain models
            label_lower = meta.label_lower
            if label_lower == 'commande_informatique.lignecommande':
                names.update([
                    'ligne commande informatique',
                    'lignes commande informatique',
                    'ligne de commande informatique',
                    'lignes de commande informatiques',
                ])
            if label_lower == 'commande_bureau.lignecommandebureau':
                names.update([
                    'ligne commande bureau',
                    'lignes commande bureau',
                    'ligne de commande bureau',
                    'lignes de commande bureau',
                ])
            if label_lower == 'commande_informatique.designation':
                names.update([
                    'designation informatique',
                    'designations informatiques',
                    'désignation informatique',
                    'désignations informatiques',
                ])
            if label_lower == 'commande_informatique.description':
                names.update([
                    'description informatique',
                    'descriptions informatiques',
                ])
            if label_lower == 'commande_bureau.designationbureau':
                names.update([
                    'designation bureau',
                    'designations bureau',
                    'désignation bureau',
                    'désignations bureau',
                ])
            if label_lower == 'commande_bureau.descriptionbureau':
                names.update([
                    'description bureau',
                    'descriptions bureau',
                ])
            if label_lower == 'demande_equipement.demandeequipement':
                names.update([
                    'demande equipement',
                    'demandes equipement',
                    'demande d equipement',
                    'demandes d equipement',
                    'demande d\'equipement',
                    'demandes d\'equipement',
                ])

            for n in names:
                nn = self._normalize_text(n)
                if nn not in self.model_aliases:
                    self.model_aliases[nn] = key

            # Build field alias map for this model
            field_map: Dict[str, str] = {}
            for f in meta.get_fields():
                # Skip reverse relations without concrete column
                if not hasattr(f, 'name'):
                    continue
                field_map[self._normalize_text(f.name)] = f.name
                verbose = getattr(f, 'verbose_name', None)
                if verbose:
                    vn = self._normalize_text(str(verbose))
                    if vn and vn not in field_map:
                        field_map[vn] = f.name
            self.field_aliases[key] = field_map

    def _normalize_text(self, text: str) -> str:
        t = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
        t = t.lower().strip()
        t = re.sub(r"\s+", " ", t)
        return t

    def _split_words(self, name: str) -> List[str]:
        # Split CamelCase and underscores into lower tokens
        if not name:
            return []
        s = re.sub(r"([a-z])([A-Z])", r"\1 \2", name)
        s = s.replace('_', ' ')
        s = self._normalize_text(s)
        return [p for p in s.split() if p]

    def _alias_variants(self, tokens: List[str]) -> List[str]:
        if not tokens:
            return []
        res: List[str] = []
        base = " ".join(tokens)
        # With 'de' between tokens: e.g., 'ligne de commande'
        if len(tokens) >= 2:
            res.append(" de ".join(tokens))
            # Plurals: naive 's' suffix
            res.append(" de ".join([tokens[0] + 's'] + tokens[1:]))  # 'lignes de commande'
            res.append(" de ".join(tokens[:-1] + [tokens[-1] + 's']))  # 'ligne de commandes'
            res.append(" de ".join([tokens[0] + 's'] + tokens[1:-1] + [tokens[-1] + 's']))  # both plural
            # With "d " elision variant
            res.append(" d ".join(tokens))  # 'demande d equipement'
            res.append(" d ".join([tokens[0] + 's'] + tokens[1:]))
        # Simple plurals without preposition
        res.append(" ".join([tokens[0] + 's'] + tokens[1:]))
        res.append(" ".join(tokens[:-1] + [tokens[-1] + 's']))
        res.append(" ".join([tokens[0] + 's'] + tokens[1:-1] + [tokens[-1] + 's']))
        res.append(base)
        return [self._normalize_text(x) for x in res]

    # ----------------------------- Public API ---------------------------------
    def try_execute(self, text: str) -> Optional[str]:
        plan = self._parse(text)
        if not plan or not plan.get("model_key"):
            return None
        try:
            data = self._execute_plan(plan)
            return self._format_result(plan, data)
        except Exception:
            # Fail silently so the caller can fall back to other handlers
            return None

    # ------------------------------ Parsing -----------------------------------
    def _parse(self, text: str) -> Optional[Dict[str, Any]]:
        q = self._normalize_text(text or "")
        if not q:
            return None

        # Detect action
        action = "list"
        if re.search(r"\b(compte|nombre de)\b", q):
            action = "count"
        elif re.search(r"\b(somme de|somme\s+du|total de)\b", q):
            action = "sum"
        elif re.search(r"\b(moyenne de)\b", q):
            action = "avg"
        elif re.search(r"\b(min(?:imum)? de)\b", q):
            action = "min"
        elif re.search(r"\b(max(?:imum)? de)\b", q):
            action = "max"
        elif re.search(r"\b(champs|sch[ée]ma)\b", q):
            action = "schema"

        # Detect models by alias occurrence (longest aliases first, allow multiple)
        model_keys: List[str] = []
        chosen_aliases: List[str] = []
        for alias in sorted(self.model_aliases.keys(), key=len, reverse=True):
            if alias in q:
                k = self.model_aliases[alias]
                if k not in model_keys:
                    model_keys.append(k)
                    chosen_aliases.append(alias)
        if not model_keys:
            # Fuzzy alias matching as a fallback for small typos
            if fuzz is not None:
                scored: List[Tuple[int, str]] = []
                for alias in self.model_aliases.keys():
                    try:
                        score = max(
                            fuzz.partial_ratio(alias, q),
                            fuzz.partial_ratio(q, alias)
                        )
                        if score >= 88:
                            scored.append((score, alias))
                    except Exception:
                        continue
                if scored:
                    scored.sort(reverse=True)
                    for _, alias in scored[:3]:
                        k = self.model_aliases[alias]
                        if k not in model_keys:
                            model_keys.append(k)
                            chosen_aliases.append(alias)
            if not model_keys:
                return None

        # Extract filters after keywords: où|dont|avec
        filters: List[Tuple[str, str, str]] = []  # (field_path, op, value)
        filter_parts = re.split(r"\b(?:où|ou|dont|avec)\b", q, maxsplit=1)
        if len(filter_parts) > 1:
            conds = filter_parts[1]
            # split by ' et '
            for cond in re.split(r"\s+et\s+", conds):
                cond = cond.strip()
                if not cond:
                    continue
                m = re.search(
                    r"([\w\s]+?)\s*(contient|commence|finit|>=|<=|=|>|<)\s*[\"'“”]?([\w\-À-ÿ\s./:_]+)",
                    cond
                )
                if m:
                    raw_field = m.group(1).strip()
                    op = m.group(2)
                    value = m.group(3).strip().strip('"\'“”')
                    field_path = self._normalize_field_path(model_key, raw_field)
                    if field_path:
                        filters.append((field_path, op, value))

        # Sorting
        order_by: Optional[str] = None
        order_desc = False
        m_sort = re.search(r"tri[ée]s?\s+par\s+([\w\s\.]+)", q)
        if m_sort:
            order_by = self._normalize_field_path(model_keys[0], m_sort.group(1).strip())
            order_desc = bool(re.search(r"(d[ée]croissant|desc)\b", q))

        # Limit
        limit = None
        m_lim = re.search(r"\b(?:top|premiers|afficher)\s+(\d+)\b", q)
        if m_lim:
            limit = int(m_lim.group(1))

        # Aggregation field (for sum/avg/min/max)
        agg_field = None
        if action in {"sum", "avg", "min", "max"}:
            m_agg = re.search(r"\b(?:de|du|des)\s+([\w\s\.]+)$", q)
            if m_agg:
                agg_field = self._normalize_field_path(model_keys[0], m_agg.group(1).strip())

        return {
            "action": action,
            "model_keys": model_keys,
            "aliases": chosen_aliases,
            "filters": filters,
            "order_by": order_by,
            "order_desc": order_desc,
            "limit": limit,
            "agg_field": agg_field,
        }

    def _normalize_field_path(self, model_key: str, raw: str) -> Optional[str]:
        raw = raw.strip()
        if not raw:
            return None
        # Support FK chaining with a space: "fournisseur nom" → fournisseur__nom
        raw = raw.replace("__", ".")  # normalize
        parts = [p for p in re.split(r"[\s\./]+", raw) if p]
        if not parts:
            return None
        # Map the first segment via aliases (name or verbose_name)
        field_map = self.field_aliases.get(model_key, {})
        first = parts[0].lower().replace(" ", "_")
        mapped_first = field_map.get(first, parts[0])
        parts[0] = mapped_first
        return "__".join(parts)

    # ------------------------------ Execution ---------------------------------
    def _execute_plan(self, plan: Dict[str, Any]) -> Any:
        keys = plan["model_keys"]
        action = plan["action"]

        # For single-model plan, keep fast path
        if len(keys) == 1:
            model = self.model_registry[keys[0]]
            return self._execute_single(model, plan)

        # Multi-model: list and count supported; schema returns combined
        results: Dict[str, Any] = {}
        if action == "count":
            total = 0
            counts: Dict[str, int] = {}
            for k in keys:
                model = self.model_registry[k]
                c = self._execute_single(model, {**plan, "model_keys": [k]})
                counts[k] = int(c or 0)
                total += counts[k]
            results["counts"] = counts
            results["total"] = total
            return results

        if action == "schema":
            schemas: Dict[str, Any] = {}
            for k in keys:
                model = self.model_registry[k]
                schemas[k] = self._describe_model(model)
            return {"schemas": schemas}

        # Default to list
        lists: Dict[str, List[Model]] = {}
        for k in keys:
            model = self.model_registry[k]
            lists[k] = self._execute_single(model, {**plan, "model_keys": [k]})
        return {"lists": lists}

    def _execute_single(self, model: Model, plan: Dict[str, Any]) -> Any:
        qs: QuerySet = model.objects.all()
        for field_path, op, value in plan["filters"]:
            lookup = self._op_to_lookup(op)
            if lookup is not None:
                qs = qs.filter(**{f"{field_path}{lookup}": self._coerce_value(value)})

        if plan["action"] == "count":
            return qs.count()
        if plan["action"] == "schema":
            return self._describe_model(model)
        if plan["action"] in {"sum", "avg", "min", "max"}:
            field = plan["agg_field"] or plan["filters"][0][0] if plan["filters"] else None
            if not field:
                return None
            agg_map = {"sum": Sum(field), "avg": Avg(field), "min": Min(field), "max": Max(field)}
            res = qs.aggregate(value=agg_map[plan["action"]])
            return res.get("value")
        if plan["order_by"]:
            order = f"-" + plan["order_by"] if plan["order_desc"] else plan["order_by"]
            qs = qs.order_by(order)
        limit = plan["limit"] or self.MAX_LIMIT
        limit = min(limit, self.MAX_LIMIT)
        return list(qs[:limit])

    def _op_to_lookup(self, op: str) -> str:
        op = op.strip()
        if op == "contient":
            return "__icontains"
        if op == "commence":
            return "__istartswith"
        if op == "finit":
            return "__iendswith"
        if op == "=":
            return ""
        if op in {">", "<", ">=", "<="}:
            return {">": "__gt", "<": "__lt", ">=": "__gte", "<=": "__lte"}[op]
        return ""

    def _coerce_value(self, value: str) -> Any:
        v = value.strip()
        # Try int
        try:
            return int(v)
        except Exception:
            pass
        # Try float (comma decimal)
        try:
            return float(v.replace(",", "."))
        except Exception:
            pass
        return v

    # ------------------------------ Formatting --------------------------------
    def _format_result(self, plan: Dict[str, Any], data: Any) -> Optional[str]:
        action = plan["action"]
        aliases = plan.get("aliases") or []
        model_keys = plan.get("model_keys") or []

        if data is None:
            return None

        if isinstance(data, int) and action == "count":
            alias = aliases[0] if aliases else self._friendly_model_label(model_keys[0])
            return f"**Nombre de {alias}**: {data}"

        if isinstance(data, (int, float)) and action in {"sum", "avg", "min", "max"}:
            label = {"sum": "Somme", "avg": "Moyenne", "min": "Min", "max": "Max"}[action]
            alias = aliases[0] if aliases else self._friendly_model_label(model_keys[0])
            return f"**{label} ({alias})**: {data}"

        if isinstance(data, list):
            if not data:
                alias = aliases[0] if aliases else self._friendly_model_label(model_keys[0])
                return f"Aucun résultat pour {alias}."
            lines: List[str] = []
            alias = aliases[0] if aliases else self._friendly_model_label(model_keys[0])
            lines.append(f"**{len(data)} résultat(s) - {alias}:**")
            for obj in data:
                summary = self._summarize_instance(obj)
                lines.append(f"• {summary}")
            return "\n".join(lines)

        if isinstance(data, dict) and plan["action"] == "schema":
            if "schemas" in data:  # multi-model schema
                lines: List[str] = []
                for k, schema in data["schemas"].items():
                    alias = self._friendly_model_label(k)
                    lines.append(f"**Champs disponibles - {alias}:**")
                    for name, ftype in schema.get("fields", []):
                        lines.append(f"• {name} ({ftype})")
                    if schema.get("relations"):
                        lines.append("\n**Relations (FK):**")
                        for name, target in schema["relations"]:
                            lines.append(f"• {name} → {target}")
                    lines.append("")
                return "\n".join([ln for ln in lines if ln is not None])
            lines: List[str] = []
            alias = aliases[0] if aliases else self._friendly_model_label(model_keys[0])
            lines.append(f"**Champs disponibles - {alias}:**")
            for name, ftype in data.get("fields", []):
                lines.append(f"• {name} ({ftype})")
            if data.get("relations"):
                lines.append("\n**Relations (FK):**")
                for name, target in data["relations"]:
                    lines.append(f"• {name} → {target}")
            return "\n".join(lines)

        if isinstance(data, dict) and "counts" in data and action == "count":
            lines: List[str] = []
            total = data.get("total", 0)
            for k, c in data["counts"].items():
                alias = self._friendly_model_label(k)
                lines.append(f"**Nombre de {alias}**: {c}")
            lines.append(f"\n**Total**: {total}")
            return "\n".join(lines)

        if isinstance(data, dict) and "lists" in data:
            lines: List[str] = []
            for k, objs in data["lists"].items():
                alias = self._friendly_model_label(k)
                if not objs:
                    lines.append(f"Aucun résultat pour {alias}.")
                    continue
                lines.append(f"**{len(objs)} résultat(s) - {alias}:**")
                for obj in objs:
                    summary = self._summarize_instance(obj)
                    lines.append(f"• {summary}")
                lines.append("")
            return "\n".join([ln for ln in lines if ln is not None])

        return None

    def _summarize_instance(self, obj: Model) -> str:
        # Prefer __str__ if informative
        try:
            text = str(obj)
            if text and text != obj.__class__.__name__:
                return text
        except Exception:
            pass
        # Fallback: show model name and primary key plus a couple of char fields
        meta = obj._meta
        pk_name = meta.pk.name
        parts = [f"{meta.model_name}(id={getattr(obj, pk_name, 'N/A')})"]
        shown = 0
        for f in meta.fields:
            if f.name == pk_name:
                continue
            try:
                value = getattr(obj, f.name)
            except Exception:
                continue
            if value is None:
                continue
            # Prefer short string-ish fields
            if hasattr(value, "__str__"):
                sval = str(value)
                if 0 < len(sval) <= 60:
                    parts.append(f"{f.name}={sval}")
                    shown += 1
            if shown >= 2:
                break
        return ", ".join(parts)

    def _friendly_model_label(self, model_key: str) -> str:
        try:
            model = self.model_registry[model_key]
            meta = model._meta
            if meta.verbose_name_plural:
                return self._normalize_text(meta.verbose_name_plural)
            if meta.verbose_name:
                return self._normalize_text(meta.verbose_name)
            return self._normalize_text(meta.model_name)
        except Exception:
            try:
                return model_key.split(".")[-1]
            except Exception:
                return "modele"

    def _describe_model(self, model: Model) -> Dict[str, Any]:
        meta = model._meta
        fields: List[Tuple[str, str]] = []
        relations: List[Tuple[str, str]] = []
        for f in meta.get_fields():
            if not hasattr(f, 'name'):
                continue
            ftype = f.get_internal_type() if hasattr(f, 'get_internal_type') else type(f).__name__
            if hasattr(f, 'remote_field') and getattr(f.remote_field, 'model', None) is not None and f.many_to_one:
                target = f.remote_field.model._meta.label_lower
                relations.append((f.name, target))
            else:
                fields.append((f.name, ftype))
        return {"fields": fields, "relations": relations}


