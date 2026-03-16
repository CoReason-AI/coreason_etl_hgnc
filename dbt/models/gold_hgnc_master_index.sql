SELECT
    coreason_id,
    hgnc_id,
    approved_symbol,
    approved_name,
    locus_type,
    ensembl_id,
    ncbi_entrez_id,
    uniprot_ids_raw,
    omim_ids_raw
FROM {{ ref('silver_hgnc_genes') }}
WHERE status = 'Approved'
