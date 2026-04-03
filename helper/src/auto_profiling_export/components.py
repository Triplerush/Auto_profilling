import math


def dataframe(df, title: str = "", config: dict | None = None) -> dict:
    columns = df.columns.tolist()
    rows = []
    for _, row in df.iterrows():
        rows.append([
            None if (isinstance(v, float) and math.isnan(v)) else v
            for v in row.tolist()
        ])
    default_config = {"sortable": True, "searchable": True, "page_size": 10}
    if config:
        default_config.update(config)
    return {
        "type": "dataframe",
        "title": title,
        "data": {"columns": columns, "rows": rows},
        "config": default_config,
    }


class _ChartNamespace:
    @staticmethod
    def bar(labels: list, datasets: list[dict], title: str = "", config: dict | None = None) -> dict:
        return {
            "type": "chart",
            "chart_type": "bar",
            "title": title,
            "data": {"labels": labels, "datasets": datasets},
            "config": config or {},
        }

    @staticmethod
    def bar_horizontal(labels: list, data: list, title: str = "", config: dict | None = None) -> dict:
        return {
            "type": "chart",
            "chart_type": "bar",
            "title": title,
            "data": {
                "labels": labels,
                "datasets": [{"label": title, "data": data}],
            },
            "config": {"indexAxis": "y", **(config or {})},
        }

    @staticmethod
    def line(labels: list, datasets: list[dict], title: str = "", config: dict | None = None) -> dict:
        return {
            "type": "chart",
            "chart_type": "line",
            "title": title,
            "data": {"labels": labels, "datasets": datasets},
            "config": config or {},
        }

    @staticmethod
    def scatter(datasets: list[dict], title: str = "", config: dict | None = None) -> dict:
        return {
            "type": "chart",
            "chart_type": "scatter",
            "title": title,
            "data": {"labels": [], "datasets": datasets},
            "config": config or {},
        }

    @staticmethod
    def histogram(series, title: str = "", bins: int = 20, config: dict | None = None) -> dict:
        values = list(series)
        if not values:
            return {
                "type": "chart",
                "chart_type": "bar",
                "title": title,
                "data": {"labels": [], "datasets": []},
                "config": config or {},
            }
        min_val, max_val = min(values), max(values)
        if min_val == max_val:
            return {
                "type": "chart",
                "chart_type": "bar",
                "title": title,
                "data": {
                    "labels": [str(min_val)],
                    "datasets": [{"label": "Frecuencia", "data": [len(values)]}],
                },
                "config": config or {},
            }
        bin_width = (max_val - min_val) / bins
        counts = [0] * bins
        for v in values:
            idx = min(int((v - min_val) / bin_width), bins - 1)
            counts[idx] += 1
        labels = [f"{min_val + i * bin_width:.2f}" for i in range(bins)]
        return {
            "type": "chart",
            "chart_type": "bar",
            "title": title,
            "data": {
                "labels": labels,
                "datasets": [{"label": "Frecuencia", "data": counts}],
            },
            "config": {"x_label": "Valor", "y_label": "Frecuencia", **(config or {})},
        }

    @staticmethod
    def pie(labels: list, data: list, title: str = "", config: dict | None = None) -> dict:
        return {
            "type": "chart",
            "chart_type": "pie",
            "title": title,
            "data": {
                "labels": labels,
                "datasets": [{"label": title, "data": data}],
            },
            "config": config or {},
        }

    @staticmethod
    def correlation(df, title: str = "Correlaciones") -> dict:
        corr = df.corr()
        columns = corr.columns.tolist()
        matrix = []
        for _, row in corr.iterrows():
            matrix.append([
                round(v, 4) if not (isinstance(v, float) and math.isnan(v)) else 0.0
                for v in row.tolist()
            ])
        return {
            "type": "correlation_matrix",
            "title": title,
            "columns": columns,
            "matrix": matrix,
        }


chart = _ChartNamespace()


def quick_histogram(series, title: str = "") -> dict:
    return chart.histogram(series, title)


def quick_scatter(x, y, title: str = "") -> dict:
    data = [{"x": xi, "y": yi} for xi, yi in zip(x, y)]
    return chart.scatter([{"label": title, "data": data}], title)


def quick_correlation(df, title: str = "Correlaciones") -> dict:
    return chart.correlation(df, title)
