WITH base AS (
    SELECT
        hgnc_id,
        uniprot_ids_raw
    FROM {{ ref('silver_hgnc_genes') }}
)
SELECT
    b.hgnc_id,
    u.uniprot_id
FROM base b,
LATERAL jsonb_array_elements_text(
    CASE
        WHEN jsonb_typeof(b.uniprot_ids_raw) = 'array' THEN b.uniprot_ids_raw
        ELSE '[]'::jsonb
    END
) AS u(uniprot_id)
WHERE b.uniprot_ids_raw IS NOT NULL
