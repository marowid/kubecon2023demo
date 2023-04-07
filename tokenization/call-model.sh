#!/bin/bash

curl --location --silent --request POST 'http://127.0.0.1:8000/files/breast_cancer' \
--header 'Content-Type: application/json' \
--data-raw '{
    "complete_tcga_id": "TCGA-A2-A0T2",
    "gender": "FEMALE",
    "age_at_initial_pathologic_diagnosis": 66,
    "er_status": "Negative",
    "pr_status": "Negative",
    "her2_final_status": "Negative",
    "tumor": "T3",
    "tumor_t1_coded": "T_Other",
    "node": "N3",
    "node_coded": "Positive",
    "metastasis": "M1",
    "metastasis_coded": "Positive",
    "ajcc_stage": "Stage IV",
    "converted_stage": "No_Conversion",
    "survival_data_form": "followup",
    "vital_status": "DECEASED",
    "days_to_date_of_last_contact": "240",
    "days_to_date_of_death": "240.0",
    "os_event": "1",
    "os_time": "240",
    "pam50_mrna": "Basal-like",
    "sigclust_unsupervised_mrna": "0",
    "sigclust_intrinsic_mrna": "-13",
    "mirna_clusters": "3",
    "methylation_clusters": "5",
    "rppa_clusters": "Basal",
    "cn_clusters": "3",
    "integrated_clusters_with_pam50": "2",
    "integrated_clusters_no_exp": "2",
    "integrated_clusters_unsup_exp": "2",
    "first_name": "Amanda",
    "last_name": "Ryan"
}'