WITH base AS (
    SELECT * FROM {{ ref('coreason_etl_hgnc_silver_hgnc_genes') }}
)
SELECT
    -- Core Identifiers (concept_id and source_id purposely excluded)
    coreason_id,
    hgnc_id,
    
    -- Attributes
    approved_symbol,
    approved_name,
    status,
    locus_type,
    location,
    ensembl_id,
    ncbi_entrez_id,
    
    -- Cleaned Arrays (Replacing the dropped _raw columns and 1-to-many map tables)
    ARRAY(SELECT jsonb_array_elements_text(CASE WHEN jsonb_typeof(uniprot_ids_raw) = 'array' THEN uniprot_ids_raw ELSE '[]'::jsonb END)) AS uniprot_ids,
    ARRAY(SELECT jsonb_array_elements_text(CASE WHEN jsonb_typeof(omim_ids_raw) = 'array' THEN omim_ids_raw ELSE '[]'::jsonb END)) AS omim_ids,
    ARRAY(SELECT jsonb_array_elements_text(CASE WHEN jsonb_typeof(alias_symbols_raw) = 'array' THEN alias_symbols_raw ELSE '[]'::jsonb END)) AS alias_symbols,
    ARRAY(SELECT jsonb_array_elements_text(CASE WHEN jsonb_typeof(prev_symbols_raw) = 'array' THEN prev_symbols_raw ELSE '[]'::jsonb END)) AS prev_symbols,
    ARRAY(SELECT jsonb_array_elements_text(CASE WHEN jsonb_typeof(prev_names_raw) = 'array' THEN prev_names_raw ELSE '[]'::jsonb END)) AS prev_names,
    ARRAY(SELECT jsonb_array_elements_text(CASE WHEN jsonb_typeof(gene_groups_raw) = 'array' THEN gene_groups_raw ELSE '[]'::jsonb END)) AS gene_groups,
    ARRAY(SELECT jsonb_array_elements_text(CASE WHEN jsonb_typeof(refseq_accessions_raw) = 'array' THEN refseq_accessions_raw ELSE '[]'::jsonb END)) AS refseq_accessions,
    ARRAY(SELECT jsonb_array_elements_text(CASE WHEN jsonb_typeof(ena_raw) = 'array' THEN ena_raw ELSE '[]'::jsonb END)) AS ena_ids,
    ARRAY(SELECT jsonb_array_elements_text(CASE WHEN jsonb_typeof(imgt_raw) = 'array' THEN imgt_raw ELSE '[]'::jsonb END)) AS imgt_ids,
    ARRAY(SELECT jsonb_array_elements_text(CASE WHEN jsonb_typeof(agr_raw) = 'array' THEN agr_raw ELSE '[]'::jsonb END)) AS agr_ids,
    ARRAY(SELECT jsonb_array_elements_text(CASE WHEN jsonb_typeof(pseudogene_org_raw) = 'array' THEN pseudogene_org_raw ELSE '[]'::jsonb END)) AS pseudogene_org_ids

FROM base
