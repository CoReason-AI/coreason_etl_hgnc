# Copyright (c) 2026 CoReason, Inc.
#
# This software is proprietary and dual-licensed.
# Licensed under the Prosperity Public License 3.0 (the "License").
# A copy of the license is available at https://prosperitylicense.com/versions/3.0.0
# For details, see the LICENSE file.
# Commercial use beyond a 30-day trial requires a separate license.
#
# Source Code: https://github.com/CoReason-AI/coreason_etl_hgnc

from pathlib import Path

import yaml


def test_dbt_project_structure() -> None:
    """Verifies that the dbt project structure is correctly initialized."""
    base_dir = Path("dbt")

    # Check if files exist
    assert (base_dir / "dbt_project.yml").is_file()
    assert (base_dir / "profiles.yml").is_file()
    assert (base_dir / "models").is_dir()
    assert (base_dir / "models" / "schema.yml").is_file()


def test_dbt_project_configuration() -> None:
    """Verifies that dbt_project.yml has the correct project name."""
    with open("dbt/dbt_project.yml") as f:
        config = yaml.safe_load(f)

    assert config["name"] == "coreason_etl_hgnc_dbt"
    assert config["profile"] == "coreason_etl_hgnc"
    assert "models" in config["model-paths"]


def test_dbt_schema_data_tests() -> None:
    """Verifies that the strict data tests are defined in schema.yml."""
    with open("dbt/models/schema.yml") as f:
        schema = yaml.safe_load(f)

    models = schema.get("models", [])
    assert len(models) == 6

    model = next(m for m in models if m["name"] == "coreason_etl_hgnc_silver_hgnc_genes")

    columns = {col["name"]: col for col in model.get("columns", [])}

    # hgnc_id tests
    assert "hgnc_id" in columns
    assert "tests" in columns["hgnc_id"]
    hgnc_id_tests = columns["hgnc_id"]["tests"]
    assert "unique" in hgnc_id_tests
    assert "not_null" in hgnc_id_tests

    # approved_symbol tests
    assert "approved_symbol" in columns
    assert "tests" in columns["approved_symbol"]
    assert "not_null" in columns["approved_symbol"]["tests"]

    # Gold model tests
    model_gold = next(m for m in models if m["name"] == "coreason_etl_hgnc_gold_hgnc_master_index")

    columns_gold = {col["name"]: col for col in model_gold.get("columns", [])}

    # hgnc_id tests
    assert "hgnc_id" in columns_gold
    assert "tests" in columns_gold["hgnc_id"]
    hgnc_id_tests_gold = columns_gold["hgnc_id"]["tests"]
    assert "unique" in hgnc_id_tests_gold
    assert "not_null" in hgnc_id_tests_gold

    # approved_symbol tests
    assert "approved_symbol" in columns_gold
    assert "tests" in columns_gold["approved_symbol"]
    assert "not_null" in columns_gold["approved_symbol"]["tests"]
