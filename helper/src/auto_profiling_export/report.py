import json
import re
from datetime import datetime, timezone
from pathlib import Path

from .validators import validate_report


def _slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[-\s]+", "-", text)


class Section:
    def __init__(self, title: str, description: str = ""):
        self.title = title
        self.description = description
        self.components: list[dict] = []

    def add(self, component: dict):
        self.components.append(component)

    def add_confusion_matrix(self, y_true, y_pred, labels=None, title="Matriz de Confusion"):
        unique = sorted(set(y_true) | set(y_pred))
        if labels is None:
            labels = [str(v) for v in unique]
        label_to_idx = {v: i for i, v in enumerate(unique)}
        n = len(unique)
        matrix = [[0] * n for _ in range(n)]
        for t, p in zip(y_true, y_pred):
            matrix[label_to_idx[t]][label_to_idx[p]] += 1
        self.components.append({
            "type": "confusion_matrix",
            "title": title,
            "labels": labels,
            "matrix": matrix,
        })

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "description": self.description,
            "components": self.components,
        }


class Report:
    def __init__(
        self,
        title: str,
        description: str = "",
        author: str = "",
        tags: list[str] | None = None,
        colab_url: str | None = None,
        github_url: str | None = None,
    ):
        self.metadata = {
            "id": _slugify(title),
            "title": title,
            "description": description,
            "author": author,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "tags": tags or [],
            "colab_url": colab_url,
            "github_url": github_url,
        }
        self.kpis: list[dict] = []
        self.sections: list[Section] = []

    def add_kpi(self, label: str, value: str, description: str = "", severity: str = "ok"):
        self.kpis.append({
            "label": label,
            "value": value,
            "description": description,
            "severity": severity,
        })

    def add_section(self, section: Section):
        self.sections.append(section)

    def to_dict(self) -> dict:
        return {
            "metadata": self.metadata,
            "kpis": self.kpis,
            "sections": [s.to_dict() for s in self.sections],
        }

    def save(self, output_path: str | Path):
        data = self.to_dict()
        validate_report(data)
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
