from typing import Union

from pydantic import BaseModel


class Pam50(BaseModel):
    gene_symbol: str
    ref_seq_protein_id: str
    species: str
    gene_name: str

    # is_offer: Union[bool, None] = None


class ClinicalDataBreastCancer(BaseModel):

    complete_tcga_id: str
    gender: str
    age_at_initial_pathologic_diagnosis: int
    er_status: str
    pr_status: str
    her2_final_status: str
    tumor: str
    tumor_t1_coded: str
    node: str
    node_coded: str
    metastasis: str
    metastasis_coded: str
    ajcc_stage: str
    converted_stage: str
    survival_data_form: str
    vital_status: str
    days_to_date_of_last_contact: str
    days_to_date_of_death: Union[str, None] = None
    os_event: str
    os_time: str
    pam50_mrna: str
    sigclust_unsupervised_mrna: str
    sigclust_intrinsic_mrna: str
    mirna_clusters: str
    methylation_clusters: str
    rppa_clusters: str
    cn_clusters: str
    integrated_clusters_with_pam50: str
    integrated_clusters_no_exp: str
    integrated_clusters_unsup_exp: str
    first_name: str
    last_name: str


if __name__ == '__main__':
    from fastapi.encoders import jsonable_encoder
    c = ClinicalDataBreastCancer(
        complete_tcga_id = "TCGA-A2-A0T2",
        gender= "FEMALE",
        age_at_initial_pathologic_diagnosis=66,
        er_status="Negative",
        pr_status = "Negative",
        her2_final_status="Negative",
        tumor="T3",
        tumor_t1_coded="T_Other",
        node="N3",
        node_coded="Positive",
        metastasis="M1",
        metastasis_coded="Positive",
        ajcc_stage="Stage IV",
        converted_stage="No_Conversion",
        survival_data_form="followup",
        vital_status="DECEASED",
        days_to_date_of_last_contact="240",
        days_to_date_of_death="240.0",
        os_event="1",
        os_time="240",
        pam50_mrna="Basal-like",
        sigclust_unsupervised_mrna="0",
        sigclust_intrinsic_mrna="-13",
        mirna_clusters="3",
        methylation_clusters="5",
        rppa_clusters="Basal",
        cn_clusters="3",
        integrated_clusters_with_pam50="2",
        integrated_clusters_no_exp="2",
        integrated_clusters_unsup_exp="2",
        first_name="Amanda",
        last_name="Ryan",
    )

    print(type(c.json()))