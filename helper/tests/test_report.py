import json
import tempfile
from pathlib import Path

import pytest

from auto_profiling_export import Report, Section, chart, dataframe


def test_report_to_dict():
    r = Report("Test Report", description="A test", author="Tester", tags=["test"])
    r.add_kpi("Accuracy", "95%", severity="ok")
    s = Section("EDA", "Exploracion")
    s.add(chart.bar(["a", "b"], [{"label": "v", "data": [1, 2]}], title="Bar"))
    r.add_section(s)
    data = r.to_dict()

    assert data["metadata"]["id"] == "test-report"
    assert data["metadata"]["title"] == "Test Report"
    assert data["metadata"]["author"] == "Tester"
    assert data["metadata"]["tags"] == ["test"]
    assert len(data["kpis"]) == 1
    assert data["kpis"][0]["label"] == "Accuracy"
    assert len(data["sections"]) == 1
    assert data["sections"][0]["title"] == "EDA"
    assert data["sections"][0]["components"][0]["type"] == "chart"


def test_report_save():
    r = Report("Save Test", author="Bot")
    r.add_kpi("F1", "0.8")
    s = Section("Results")
    s.add(chart.pie(["A", "B"], [30, 70], title="Dist"))
    r.add_section(s)

    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "out.json"
        r.save(path)
        assert path.exists()
        data = json.loads(path.read_text())
        assert data["metadata"]["id"] == "save-test"
        assert len(data["sections"]) == 1


def test_invalid_severity():
    r = Report("Bad Severity")
    r.add_kpi("Acc", "90%", severity="invalid")
    s = Section("S")
    s.add(chart.bar([], [], title="empty"))
    r.add_section(s)

    with tempfile.TemporaryDirectory() as tmpdir:
        with pytest.raises(ValueError, match="severity"):
            r.save(Path(tmpdir) / "bad.json")


def test_no_sections_raises():
    r = Report("Empty")
    r.add_kpi("K", "V")
    with tempfile.TemporaryDirectory() as tmpdir:
        with pytest.raises(ValueError, match="section"):
            r.save(Path(tmpdir) / "empty.json")


def test_chart_histogram():
    values = [1, 2, 2, 3, 3, 3, 4, 4, 5]
    result = chart.histogram(values, title="Hist", bins=5)
    assert result["type"] == "chart"
    assert result["chart_type"] == "bar"
    assert len(result["data"]["labels"]) == 5
    assert sum(result["data"]["datasets"][0]["data"]) == len(values)


def test_confusion_matrix():
    s = Section("Eval")
    y_true = [0, 0, 1, 1, 1]
    y_pred = [0, 1, 1, 1, 0]
    s.add_confusion_matrix(y_true, y_pred, labels=["Neg", "Pos"])
    comp = s.components[0]
    assert comp["type"] == "confusion_matrix"
    assert comp["labels"] == ["Neg", "Pos"]
    assert comp["matrix"] == [[1, 1], [1, 2]]


def test_chart_bar_horizontal():
    result = chart.bar_horizontal(["f1", "f2"], [0.8, 0.6], title="Importance")
    assert result["config"]["indexAxis"] == "y"


def test_dataframe_with_pandas():
    try:
        import pandas as pd
    except ImportError:
        pytest.skip("pandas not installed")
    df = pd.DataFrame({"a": [1, 2, None], "b": [4, 5, 6]})
    result = dataframe(df, title="Test DF")
    assert result["type"] == "dataframe"
    assert result["data"]["columns"] == ["a", "b"]
    assert result["data"]["rows"][2][0] is None  # NaN -> None
