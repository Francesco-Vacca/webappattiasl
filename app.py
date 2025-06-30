import streamlit as st
from MODULI.funzioni import scrap_asl, motore_ricerca
import polars as pl
from MODULI.UTILITY.keys import atti_excel_url, atti_parquet_url,ultimo_agg_url,atti_pubb_url

COLONNE = ["Azienda", "Tipo", "Numero", "Data", "Titolo", "Descrizione", "Link"]

st.set_page_config(
    page_title="Atti ASL Regione Sardegna",
    page_icon=r"MODULI\UTILITY\Icona_regione_sardegna.ico",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🗂️ Consultazione e Aggiornamento Atti ASL")
st.link_button("🔗 CONSULTA TUTTO",
    "https://1drv.ms/x/c/b1564e55915469ec/EUfD0CuXBbJJuQX3RmwjdwQB1E7cLTr0h4ymc1YAER6JZw?e=w7lKKO"
)

# --- Stato per mostrare/nascondere i filtri ---
if "show_filters" not in st.session_state:
    st.session_state.show_filters = False

def toggle_filters():
    st.session_state.show_filters = not st.session_state.show_filters

st.button("🔍 MOTORE RICERCA BETA", on_click=toggle_filters)

if st.session_state.show_filters:
    with st.expander("🎯 Filtri di ricerca", expanded=True):
        # Lazy loading: carica il DataFrame solo qui!
        @st.cache_data
        def load_data():
            return pl.read_parquet(atti_parquet_url)
        df = load_data()
        aziende = df["Azienda"].unique().sort().to_list()
        tipi = df["Tipo"].unique().sort().to_list()
        min_data = df["Data"].min()
        max_data = df["Data"].max()

        col1, col2, col3 = st.columns(3)
        with col1:
            azienda = st.multiselect("Azienda", options=aziende)
            tipo = st.multiselect("Tipo", options=tipi)
        with col2:
            numero = st.text_input("Numero")
            descrizione = st.text_input("Testo nella descrizione")
        with col3:
            data_inizio = st.date_input("Data inizio", value=min_data)
            data_fine = st.date_input("Data fine", value=max_data)

        if st.button("🔎 Cerca"):
            risultati = motore_ricerca(
                df,
                azienda=azienda,
                tipo=tipo,
                numero=numero,
                data_inizio=data_inizio,
                data_fine=data_fine,
                descrizione=descrizione
            )
            st.success(f"✅ {risultati.shape[0]} risultati trovati")
            st.dataframe(risultati, use_container_width=True)

# --- Aggiornamento dati ---
if st.button("🔄 AGGIORNA"):
    with st.spinner("⏳ Aggiornamento in corso..."):
        scrap_asl()
    st.success("✅ Aggiornamento completato!")

# --- Visualizza ultimo aggiornamento ---
try:
    data = pl.read_csv(ultimo_agg_url)
    data = data.columns
    st.subheader(f"🕒 Atti aggiornati al {data[0]}")
except Exception:
    st.warning("Data ultimo aggiornamento non disponibile.")
