WITH base AS (
    SELECT
        hgnc_id,
        approved_symbol,
        alias_symbols_raw,
        prev_symbols_raw
    FROM {{ ref('silver_hgnc_genes') }}
)
SELECT
    hgnc_id,
    approved_symbol AS search_term,
    'Approved' AS term_type
FROM base

UNION ALL

SELECT
    b.hgnc_id,
    a.alias_symbol AS search_term,
    'Alias' AS term_type
FROM base b,
LATERAL jsonb_array_elements_text(
    CASE
        WHEN jsonb_typeof(b.alias_symbols_raw) = 'array' THEN b.alias_symbols_raw
        ELSE '[]'::jsonb
    END
) AS a(alias_symbol)
WHERE b.alias_symbols_raw IS NOT NULL

UNION ALL

SELECT
    b.hgnc_id,
    p.prev_symbol AS search_term,
    'Previous' AS term_type
FROM base b,
LATERAL jsonb_array_elements_text(
    CASE
        WHEN jsonb_typeof(b.prev_symbols_raw) = 'array' THEN b.prev_symbols_raw
        ELSE '[]'::jsonb
    END
) AS p(prev_symbol)
WHERE b.prev_symbols_raw IS NOT NULL
