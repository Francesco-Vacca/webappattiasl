from pathlib import Path


mapping_dict = {
    "Ares_archivio_delibere": "Ares",
    "Ares_archivio_determine": "Ares",
    "Asl_1_archivio_delibere": "Asl 1 Sassari",
    "Asl_1_archivio_determine": "Asl 1 Sassari",
    "Asl_2_archivio_delibere": "Asl 2 Gallura",
    "Asl_2_archivio_determine": "Asl 2 Gallura",
    "Asl_3_archivio_delibere": "Asl 3 Nuoro",
    "Asl_3_archivio_determine": "Asl 3 Nuoro",
    "Asl_4_archivio_delibere": "Asl 4 Ogliastra",
    "Asl_4_archivio_determine": "Asl 4 Ogliastra",
    "Asl_5_archivio_delibere": "Asl 5 Oristano",
    "Asl_5_archivio_determine": "Asl 5 Oristano",
    "Asl_6_archivio_delibere": "Asl 6 Medio Campidano",
    "Asl_6_archivio_determine": "Asl 6 Medio Campidano",
    "Asl_7_archivio_delibere": "Asl 7 Sulcis",
    "Asl_7_archivio_determine": "Asl 7 Sulcis",
    "Asl_8_archivio_delibere": "Asl 8 Cagliari",
    "Asl_8_archivio_determine": "Asl 8 Cagliari",
    "Ares_delibere": "Ares",
    "Ares_determine": "Ares",
    "Asl_1_delibere": "Asl 1 Sassari",
    "Asl_1_determine": "Asl 1 Sassari",
    "Asl_2_delibere": "Asl 2 Gallura",
    "Asl_2_determine": "Asl 2 Gallura",
    "Asl_3_delibere": "Asl 3 Nuoro",
    "Asl_3_determine": "Asl 3 Nuoro",
    "Asl_4_delibere": "Asl 4 Ogliastra",
    "Asl_4_determine": "Asl 4 Ogliastra",
    "Asl_5_delibere": "Asl 5 Oristano",
    "Asl_5_determine": "Asl 5 Oristano",
    "Asl_6_delibere": "Asl 6 Medio Campidano",
    "Asl_6_determine": "Asl 6 Medio Campidano",
    "Asl_7_delibere": "Asl 7 Sulcis",
    "Asl_7_determine": "Asl 7 Sulcis",
    "Asl_8_delibere": "Asl 8 Cagliari",
    "Asl_8_determine": "Asl 8 Cagliari",
    "Aob_delibere": "AOB",
    "Aob_determine": "AOB",
}

url_comm_dict = {
    "Ares_delibere": "https://www.aressardegna.it/albo-pretorio/delibere-del-direttore-generale/",
    "Asl_1_delibere": "https://www.asl1sassari.it/albo-pretorio/delibere-commissario/",
    "Asl_2_delibere": "https://www.aslgallura.it/albo-pretorio/delibere-commissario/",
    "Asl_3_delibere": "https://www.asl3nuoro.it/albo-pretorio/delibere-commissario/",
    "Asl_4_delibere": "https://www.aslogliastra.it/albo-pretorio/delibere-commissario/",
    "Asl_5_delibere": "https://www.asl5oristano.it/albo-pretorio/delibere-commissario/",
    "Asl_6_delibere": "https://www.aslmediocampidano.it/albo-pretorio/delibere-commissario/",
    "Asl_7_delibere": "https://www.aslsulcis.it/albo-pretorio/delibere-commissario/",
    "Asl_8_delibere": "https://www.asl8cagliari.it/albo-pretorio/delibere-commissario/",
    "Ares_determine": "https://www.aressardegna.it/albo-pretorio/determine-dirigenziali/",
    "Asl_1_determine": "https://www.asl1sassari.it/albo-pretorio/determine-dirigenziali/",
    "Asl_2_determine": "https://www.aslgallura.it/albo-pretorio/determine-dirigenziali/",
    "Asl_3_determine": "https://www.asl3nuoro.it/albo-pretorio/determine-dirigenziali/",
    "Asl_4_determine": "https://www.aslogliastra.it/albo-pretorio/determine-dirigenziali/",
    "Asl_5_determine": "https://www.asl5oristano.it/albo-pretorio/determine-dirigenziali/",
    "Asl_6_determine": "https://www.aslmediocampidano.it/albo-pretorio/determine-dirigenziali/",
    "Asl_7_determine": "https://www.aslsulcis.it/albo-pretorio/determine-dirigenziali/",
    "Asl_8_determine": "https://www.asl8cagliari.it/albo-pretorio/determine-dirigenziali/",
}

atti_excel_url = Path("MODULI") / "DB" / "ATTI_ASL_DAL_2022.xlsx"
atti_parquet_url = Path("MODULI") / "DB" / "ATTI_ASL_DAL_2022.parquet"
ultimo_agg_url = Path("MODULI") / "DB" / "ultimo aggiornamento.txt"
atti_pubb_url = Path("MODULI") / "DB" / "atti_in_public.xlsx"