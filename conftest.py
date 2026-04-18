"""
conftest.py
Configuración global: marcadores personalizados y hook que guarda
cada resultado de prueba en reports/results.csv automáticamente.
"""

import pytest
import csv
import os
from datetime import datetime


def pytest_configure(config):
    """Registra los marcadores personalizados."""
    config.addinivalue_line(
        "markers", "smoke: pruebas críticas de humo — corren primero")
    config.addinivalue_line(
        "markers", "regression: suite completa de regresión")
    config.addinivalue_line(
        "markers", "performance: validación de tiempos de respuesta")


def pytest_runtest_logreport(report):
    """Hook: guarda el resultado de cada prueba en CSV al finalizar."""
    if report.when == "call":
        os.makedirs("reports", exist_ok=True)
        filepath = "reports/results.csv"
        write_header = not os.path.exists(filepath)
        with open(filepath, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if write_header:
                writer.writerow(
                    ["timestamp", "test_id", "outcome", "duration_s"])
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                report.nodeid,
                report.outcome,      # "passed" | "failed" | "error"
                round(report.duration, 4),
            ])


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Muestra resumen final en consola."""
    passed = len(terminalreporter.stats.get("passed", []))
    failed = len(terminalreporter.stats.get("failed", []))
    errors = len(terminalreporter.stats.get("error",  []))
    total = passed + failed + errors
    rate = round(passed / total * 100, 1) if total else 0

    print(f"\n{'='*55}")
    print(f"  QA Pipeline — Resumen Final")
    print(f"  API: https://jsonplaceholder.typicode.com")
    print(f"{'='*55}")
    print(f"  ✅ Pasaron  : {passed}")
    print(f"  ❌ Fallaron : {failed}")
    print(f"  💥 Errores  : {errors}")
    print(f"  📈 Éxito    : {rate}%")
    print(f"{'='*55}\n")
