{{ config(
    materialized='table',
    pre_hook='CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'
) }}

WITH raw_source AS (
    SELECT
        raw_data
    FROM {{ source('bronze_hgnc', 'bronze_hgnc_genes_raw') }}
)

SELECT
    uuid_generate_v5('106ebc37-142c-47db-a228-db629f1d07c0'::uuid, raw_data->>'hgnc_id') AS coreason_id,
    raw_data->>'hgnc_id' AS hgnc_id,
    raw_data->>'symbol' AS approved_symbol,
    raw_data->>'name' AS approved_name,
    raw_data->>'status' AS status,
    raw_data->>'locus_type' AS locus_type,
    raw_data->>'ensembl_gene_id' AS ensembl_id,
    raw_data->>'entrez_id' AS ncbi_entrez_id,
    raw_data->'uniprot_ids' AS uniprot_ids_raw,
    raw_data->'alias_symbol' AS alias_symbols_raw,
    raw_data->'prev_symbol' AS prev_symbols_raw,
    md5(raw_data::text) AS content_hash
FROM raw_source
