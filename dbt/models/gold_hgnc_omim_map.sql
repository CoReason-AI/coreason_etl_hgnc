WITH base AS (
    SELECT
        hgnc_id,
        omim_ids_raw
    FROM {{ ref('silver_hgnc_genes') }}
)
SELECT
    b.hgnc_id,
    o.omim_id
FROM base b,
LATERAL jsonb_array_elements_text(
    CASE
        WHEN jsonb_typeof(b.omim_ids_raw) = 'array' THEN b.omim_ids_raw
        ELSE '[]'::jsonb
    END
) AS o(omim_id)
WHERE b.omim_ids_raw IS NOT NULL
