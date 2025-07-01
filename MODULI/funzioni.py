from bs4 import BeautifulSoup
import requests
import re
import time
import polars as pl
import datetime
import streamlit as st
from MODULI.UTILITY.keys import mapping_dict, url_comm_dict
from MODULI.UTILITY.keys import atti_excel_url, atti_parquet_url,ultimo_agg_url,atti_pubb_url

#funzione per misurare il tempo d'esecuzione di una funzione (si applica come decoratore della funzione da misurare)

def orologio(func): 
    def wrapper(*args, **kwargs): 
        start_time = time.time() 
        result = func(*args, **kwargs) 
        end_time = time.time() 
        elapsed_time = end_time - start_time
        print(f"Tempo impiegato da {func.__name__}: {elapsed_time:.2f} secondi") 
        return result 

    return wrapper


#prende il dataframe base e lo rende omogeneo con le precedenti estrazioni
def modeling_asl(df):
    mapping_df = pl.DataFrame({
        "Albo": list(mapping_dict.keys()),
        "Azienda": list(mapping_dict.values())
    })

    df = df.join(mapping_df, how="left", left_on="Albo", right_on="Albo") 

    df = df.with_columns(
        pl.when(pl.col("Albo").str.ends_with("determine"))
        .then(pl.lit("Determine"))
        .otherwise(pl.lit("Delibere"))
        .alias("Tipo")
    )

    df = df.with_columns(
        pl.col("Titolo")
        .str.extract_all(r"\d+")  # Estrai tutte le sequenze di numeri
        .alias("SoloNumeri")
    )
    # Aggiunta di una colonna con l'ultimo elemento di ogni lista
    df = df.with_columns(
        pl.col("SoloNumeri").map_elements(lambda x: x[-4], return_dtype=pl.String).alias("Numero")
    )

    df = df.with_columns(
        pl.col("Data").str.strptime(pl.Date, format="%d.%m.%Y").alias("Data")
    )
        
    df= df.select('Azienda','Tipo','Numero','Data', 'Titolo', 'Descrizione','Link')
    print(df)
    return(df)


# unisce il nuovo df con il vecchio df
def unisci_file(new_df):
    print(new_df.schema)
    old_df= pl.read_excel(atti_excel_url)

    new_df= new_df.with_columns(pl.col('Numero').cast(pl.Int64))
    old_df= old_df.with_columns(pl.col('Numero').cast(pl.Int64))
    print(new_df.schema)
    print(old_df.schema)
    df = pl.concat([new_df,old_df])
    df = df.unique(subset=["Azienda", "Tipo", "Numero", "Data"])
    df = df.sort(["Tipo","Azienda", "Data","Numero"], descending=[False, False, True, True])
    data = marca_temporale()
    df.write_excel(atti_excel_url,worksheet=f"{data}")
    df.write_parquet(atti_parquet_url)
    return print("file aggiornato")

# restituisce una variabile contenente il giorno di utilizzo di questa funzione
def marca_temporale():
    # Memorizza la data e l'ora correnti
    data_ora_corrente = datetime.datetime.now()

    # Estrai solo anno, mese, giorno, ore e minuti
    anno_mese_giorno = data_ora_corrente.strftime("%d-%m-%Y")

    print(anno_mese_giorno)

    with open(ultimo_agg_url, "w") as file:
        file.write(anno_mese_giorno)
    return(anno_mese_giorno)

@orologio
def scrap_asl(dict = url_comm_dict ):
    links = []
    titles = []
    descriptions = []
    date_p = []
    albo = []

    for azienda, url in dict.items():  # Itera su chiavi e valori del dizionario
        while url:  # Continua a iterare finché esiste una pagina successiva
            print(f"Processing: {url}")
            response = requests.get(url, verify=False)
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Trova tutti i card-body
            card_body = soup.find_all('div', class_="card-body")
            for card in card_body:
                card_title = card.find('h5', class_="card-title")
                card_description = card.find('li', class_="col-lg-12 mt-1")
                date_publ = card.find('li', class_="col-md-12 col-12 mt-1")
                pattern = r'In Pubblicazione dal:\s*(\d{2}\.\d{2}\.\d{4})'
                if date_publ:
                    text = date_publ.get_text()  # Estrai il testo
                    date = re.search(pattern, text)  # Cerca il pattern
                    if date:
                        date_p.append(date.group(1))
                                            
                # Aggiungi descrizioni
                if card_description:
                    description = card_description.text.strip()
                    descriptions.append(description)

                
                # Aggiungi titoli e link
                if card_title:
                    link_tag = card_title.find('a')
                    if link_tag and 'href' in link_tag.attrs:
                        link = link_tag['href']
                        title = link_tag.get('title', link_tag.text.strip())
                        links.append(link)
                        titles.append(title)
                        albo.append(azienda)  # Aggiungi il nome dell'azienda
                        
            # Trova il link alla pagina successiva
            next_page = soup.find('a', class_="next page-link")
            if next_page and 'href' in next_page.attrs:
                url = next_page['href']  # Aggiorna l'URL con la pagina successiva
            else:
                url = None  # Non ci sono più pagine, interrompi il loop
    

    df_base = pl.DataFrame({
    "Albo": albo,
    "Data": date_p,
    "Titolo": titles,
    "Descrizione": descriptions,
    "Link": links
    })
    
    print(df_base)
    df_modellato=modeling_asl(df_base)
    df_modellato.write_excel(atti_pubb_url)
    unisci_file(df_modellato)
   
COLONNE = ["Azienda","Tipo","Numero","Data","Titolo","Descrizione", "Link"]

def motore_ricerca(df, azienda, tipo, numero, data_inizio, data_fine, descrizione):
    condizioni = []

    if azienda:
        condizioni.append(pl.col("Azienda").is_in(azienda))

    if tipo:
        condizioni.append(pl.col("Tipo").is_in(tipo))

    if numero:
        try:
            numero_int = int(numero)
            condizioni.append(pl.col("Numero") == numero_int)
        except ValueError:
            st.warning("⚠ Inserire un numero valido nel campo 'Numero'.")

    if data_inizio and data_fine:
        condizioni.append(pl.col("Data").is_between(data_inizio, data_fine, closed="both"))
    elif data_inizio:
        condizioni.append(pl.col("Data") >= data_inizio)
    elif data_fine:
        condizioni.append(pl.col("Data") <= data_fine)

    if descrizione:
        parole = descrizione.lower().split()
        cond_descrizione = None
        for parola in parole:
            cond = pl.col("Descrizione").str.to_lowercase().str.contains(parola)
            if cond_descrizione is None:
                cond_descrizione = cond
            else:
                cond_descrizione &= cond  # Cambiato da OR (|=) a AND (&=)
        if cond_descrizione is not None:
            condizioni.append(cond_descrizione)

    if condizioni:
        filtro_totale = condizioni[0]
        for cond in condizioni[1:]:
            filtro_totale &= cond
        df = df.filter(filtro_totale)
    
    return df