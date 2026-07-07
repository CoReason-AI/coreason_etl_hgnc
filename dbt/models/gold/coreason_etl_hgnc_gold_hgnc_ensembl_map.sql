WITH base AS (
    SELECT
        hgnc_id,
        ensembl_id
    FROM {{ ref('coreason_etl_hgnc_silver_hgnc_genes') }}
    WHERE ensembl_id IS NOT NULL
)
SELECT
    hgnc_id,
    ensembl_id
FROM base
