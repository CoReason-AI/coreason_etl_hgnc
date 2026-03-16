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


def test_silver_hgnc_genes_sql_content() -> None:
    """Verifies that silver_hgnc_genes.sql exists and contains expected SQL constructs."""
    sql_path = Path("dbt/models/silver_hgnc_genes.sql")
    assert sql_path.exists()

    sql_content = sql_path.read_text()

    # Check for correct Postgres extension
    assert 'CREATE EXTENSION IF NOT EXISTS "uuid-ossp";' in sql_content

    # Check for core identifiers extraction
    assert (
        "uuid_generate_v5('106ebc37-142c-47db-a228-db629f1d07c0'::uuid, raw_data->>'hgnc_id') AS coreason_id"
        in sql_content
    )
    assert "md5(raw_data::text) AS content_hash" in sql_content

    # Check for expected JSON -> text operators (->>)
    assert "raw_data->>'hgnc_id' AS hgnc_id" in sql_content
    assert "raw_data->>'symbol' AS approved_symbol" in sql_content
    assert "raw_data->>'name' AS approved_name" in sql_content
    assert "raw_data->>'status' AS status" in sql_content
    assert "raw_data->>'locus_type' AS locus_type" in sql_content
    assert "raw_data->>'ensembl_gene_id' AS ensembl_id" in sql_content
    assert "raw_data->>'entrez_id' AS ncbi_entrez_id" in sql_content

    # Check for expected JSON -> JSONB operators (->)
    assert "raw_data->'uniprot_ids' AS uniprot_ids_raw" in sql_content
    assert "raw_data->'alias_symbol' AS alias_symbols_raw" in sql_content
    assert "raw_data->'prev_symbol' AS prev_symbols_raw" in sql_content

    # Check source table
    assert "source('bronze_hgnc', 'bronze_hgnc_genes_raw')" in sql_content


def test_gold_hgnc_master_index_sql_content() -> None:
    """Verifies that gold_hgnc_master_index.sql exists and contains expected SQL constructs."""
    sql_path = Path("dbt/models/gold_hgnc_master_index.sql")
    assert sql_path.exists()

    sql_content = sql_path.read_text()

    # Check source reference
    assert "ref('silver_hgnc_genes')" in sql_content

    # Check filtering logic
    assert "WHERE status = 'Approved'" in sql_content

    # Check selected fields
    assert "coreason_id" in sql_content
    assert "hgnc_id" in sql_content
    assert "approved_symbol" in sql_content
    assert "approved_name" in sql_content
    assert "locus_type" in sql_content
    assert "ensembl_id" in sql_content
    assert "ncbi_entrez_id" in sql_content
    assert "uniprot_ids_raw" in sql_content


def test_dbt_schema_updates_for_silver() -> None:
    """Verifies that schema.yml has the correctly updated structures for the silver model."""
    schema_path = Path("dbt/models/schema.yml")
    assert schema_path.exists()

    with open(schema_path) as f:
        schema = yaml.safe_load(f)

    # Validate source presence
    sources = schema.get("sources", [])
    assert len(sources) > 0
    bronze_source = next((s for s in sources if s["name"] == "bronze_hgnc"), None)
    assert bronze_source is not None
    assert any(t["name"] == "bronze_hgnc_genes_raw" for t in bronze_source.get("tables", []))

    # Validate model fields
    models = schema.get("models", [])
    model = next((m for m in models if m["name"] == "silver_hgnc_genes"), None)
    assert model is not None

    columns = {col["name"]: col for col in model.get("columns", [])}

    assert "coreason_id" in columns
    assert "unique" in columns["coreason_id"]["tests"]
    assert "not_null" in columns["coreason_id"]["tests"]

    assert "hgnc_id" in columns
    assert "unique" in columns["hgnc_id"]["tests"]
    assert "not_null" in columns["hgnc_id"]["tests"]

    assert "approved_symbol" in columns
    assert "not_null" in columns["approved_symbol"]["tests"]


def test_gold_hgnc_synonym_map_sql_content() -> None:
    """Verifies that gold_hgnc_synonym_map.sql exists and contains expected SQL constructs."""
    sql_path = Path("dbt/models/gold_hgnc_synonym_map.sql")
    assert sql_path.exists()

    sql_content = sql_path.read_text()

    # Check source reference
    assert "ref('silver_hgnc_genes')" in sql_content

    # Check JSON unnesting
    assert "jsonb_array_elements_text" in sql_content

    # Check unions
    assert "UNION ALL" in sql_content

    # Check term types
    assert "'Approved' AS term_type" in sql_content
    assert "'Alias' AS term_type" in sql_content
    assert "'Previous' AS term_type" in sql_content


def test_dbt_schema_updates_for_synonym_map() -> None:
    """Verifies that schema.yml has the correctly updated structures for the synonym map model."""
    schema_path = Path("dbt/models/schema.yml")
    assert schema_path.exists()

    with open(schema_path) as f:
        schema = yaml.safe_load(f)

    # Validate model fields
    models = schema.get("models", [])
    model = next((m for m in models if m["name"] == "gold_hgnc_synonym_map"), None)
    assert model is not None

    columns = {col["name"]: col for col in model.get("columns", [])}

    assert "hgnc_id" in columns
    assert "not_null" in columns["hgnc_id"]["tests"]

    assert "search_term" in columns
    assert "not_null" in columns["search_term"]["tests"]

    assert "term_type" in columns
    assert "not_null" in columns["term_type"]["tests"]


def test_dbt_schema_updates_for_gold() -> None:
    """Verifies that schema.yml has the correctly updated structures for the gold model."""
    schema_path = Path("dbt/models/schema.yml")
    assert schema_path.exists()

    with open(schema_path) as f:
        schema = yaml.safe_load(f)

    # Validate model fields
    models = schema.get("models", [])
    model = next((m for m in models if m["name"] == "gold_hgnc_master_index"), None)
    assert model is not None

    columns = {col["name"]: col for col in model.get("columns", [])}

    assert "coreason_id" in columns
    assert "unique" in columns["coreason_id"]["tests"]
    assert "not_null" in columns["coreason_id"]["tests"]

    assert "hgnc_id" in columns
    assert "unique" in columns["hgnc_id"]["tests"]
    assert "not_null" in columns["hgnc_id"]["tests"]

    assert "approved_symbol" in columns
    assert "not_null" in columns["approved_symbol"]["tests"]
