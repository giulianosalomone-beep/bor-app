import streamlit as st
import pandas as pd
from fpdf import FPDF
import tempfile
import datetime
import os

# ==========================================
# GESTIONE CARICAMENTO CATALOGO (FLESSIBILE)
# ==========================================
def trova_file_excel_locale():
    candidati = [f for f in os.listdir('.') if f.endswith('.xlsx') and not f.startswith('~$')]
    # Privilegia file con BOR o Sviluppo nel nome
    candidati_bor = [f for f in candidati if any(k in f for k in ['BOR', 'Sviluppo', 'Prodotti'])]
    if candidati_bor:
        return candidati_bor[0]
    if candidati:
        return candidati[0]
    return None

def pulisci_dataframe(df_p, df_s):
    df_p['Tipo Nodo'] = df_p['Tipo Nodo'].fillna('Passivo')
    df_p['Descrizione Articolo'] = df_p['Descrizione Articolo'].fillna(df_p['Nome Articolo'])
    df_p['Prezzo Unitario Listino'] = pd.to_numeric(df_p['Prezzo Unitario Listino'], errors='coerce').fillna(0.0)
    df_s['Prezzo Unitario Listino'] = pd.to_numeric(df_s['Prezzo Unitario Listino'], errors='coerce').fillna(0.0)
    return df_p, df_s

# ==========================================
# GESTIONE TESTI SICURI PER IL PDF
# ==========================================
def safe_str(testo):
    if not testo or pd.isna(testo):
        return ""
    conversione = {
        'à': "a'", 'á': "a'", 'è': "e'", 'é': "e'", 'ì': "i'", 'í': "i'",
        'ò': "o'", 'ó': "o'", 'ù': "u'", 'ú': "u'", '€': "Euro", '’': "'",
        '“': '"', '”': '"', '–': '-', '\t': ' '
    }
    testo = str(testo)
    for k, v in conversione.items():
        testo = testo.replace(k, v)
    return testo.encode('latin-1', 'replace').decode('latin-1')

def calcola_assistenza_bor(nodi_totali):
    tiers = [(4, 100.0), (8, 150.0), (16, 250.0), (32, 400.0), (48, 600.0)]
    for limite, tariffa in tiers:
        if nodi_totali <= limite:
            return tariffa
    return 800.0 + (nodi_totali - 48) * 15.0

# ==========================================
# CLASSE PDF MEMORANDUM BOR (2 PAGINE)
# ==========================================
class MemorandumBOR_PDF(FPDF):
    def __init__(self, cliente, agente, note_progetto):
        super().__init__()
        self.cliente = safe_str(cliente)
        self.agente = safe_str(agente)
        self.note_progetto = safe_str(note_progetto)

    def header(self):
        if os.path.exists("logo_bor.png"):
            self.image("logo_bor.png", 10, 8, 38)
            self.set_xy(50, 10)
        else:
            self.set_xy(10, 10)
            self.set_font('Arial', 'B', 18)
            self.set_text_color(30, 58, 138)
            self.cell(40, 10, 'BOR', 0, 0, 'L')
            self.set_xy(50, 10)

        self.set_font('Arial', 'B', 12)
        self.set_text_color(30, 58, 138)
        self.cell(0, 6, 'MEMORANDUM OPERATIVO E DI INVESTIMENTO', 0, 1, 'R')
        self.set_font('Arial', '', 8)
        self.set_text_color(100, 116, 139)
        self.cell(0, 4, 'Sistemi di Sicurezza in Telepresenza e Gestione Eventi Critici', 0, 1, 'R')
        self.set_draw_color(30, 58, 138)
        self.set_line_width(0.6)
        self.line(10, 24, 200, 24)
        self.ln(6)

    def footer(self):
        self.set_y(-12)
        self.set_draw_color(226, 232, 240)
        self.set_line_width(0.3)
        self.line(10, 285, 200, 285)
        self.set_font('Arial', 'I', 7)
        self.set_text_color(148, 163, 184)
        self.cell(95, 8, 'BOR S.r.l. - Documento ad uso interno e riservato', 0, 0, 'L')
        self.cell(95, 8, f'Pagina {self.page_no()} di 2', 0, 0, 'R')

    def box_sezione(self, titolo):
        self.set_font('Arial', 'B', 8.5)
        self.set_fill_color(30, 58, 138)
        self.set_text_color(255, 255, 255)
        self.cell(0, 5.5, f'  {titolo}', 0, 1, 'L', True)
        self.ln(1.5)

def genera_pdf_memorandum(cliente, agente, note, acconto, tipo_contratto, carrello_hw, servizi_sel, canoni_calcolati):
    pdf = MemorandumBOR_PDF(cliente, agente, note)
    pdf.set_auto_page_break(auto=False, margin=10)
    
    # ------------------ PAGINA 1 ------------------
    pdf.add_page()
    
    pdf.set_fill_color(248, 250, 252)
    pdf.set_draw_color(226, 232, 240)
    pdf.rect(10, 26, 190, 18, 'FD')
    
    pdf.set_xy(12, 28)
    pdf.set_font('Arial', 'B', 8)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(24, 3.5, 'Cliente / Ditta:', 0, 0)
    pdf.set_font('Arial', 'B', 8)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(82, 3.5, safe_str(cliente) if cliente else 'Destinatario Proposta', 0, 0)
    
    pdf.set_font('Arial', 'B', 8)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(26, 3.5, 'Security Manager:', 0, 0)
    pdf.set_font('Arial', '', 8)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 3.5, safe_str(agente) if agente else 'Team Tecnico BOR', 0, 1)

    pdf.set_xy(12, 32.5)
    pdf.set_font('Arial', 'B', 8)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(24, 3.5, "Data e Validita':", 0, 0)
    pdf.set_font('Arial', '', 8)
    pdf.set_text_color(30, 41, 59)
    data_str = datetime.datetime.now().strftime("%d/%m/%Y")
    pdf.cell(82, 3.5, f'{data_str} | Proposta Riservata (30 gg)', 0, 0)

    pdf.set_font('Arial', 'B', 8)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(26, 3.5, 'Regime Impianto:', 0, 0)
    pdf.set_font('Arial', '', 8)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 3.5, safe_str(tipo_contratto), 0, 1)

    pdf.set_xy(12, 37)
    pdf.set_font('Arial', 'B', 8)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(24, 3.5, 'Note Esecutive:', 0, 0)
    pdf.set_font('Arial', 'I', 7)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(0, 3.5, safe_str(note) if note else "Configurazione su misura calcolata in base all'analisi dei varchi e criticita'.", 0, 1)

    pdf.set_y(47)

    # 1. Investimento a Corpo
    pdf.box_sezione("1. DIMENSIONAMENTO INFRASTRUTTURA HARDWARE (A CORPO)")
    tot_hw = sum(item['totale'] for item in carrello_hw)
    nodi_cam = sum(item['qt'] for item in carrello_hw if item['tipo_nodo'] == 'Camera')
    nodi_totali = sum(item['qt'] for item in carrello_hw if item['tipo_nodo'] in ['Camera', 'Audio', 'MSB_Fog', 'MSB_Sos', 'MSB_Gate'])
    assistenza = calcola_assistenza_bor(nodi_totali)
    totale_finale = tot_hw + assistenza

    pdf.set_fill_color(241, 245, 249)
    pdf.set_draw_color(203, 213, 225)
    pdf.rect(10, pdf.get_y(), 190, 24, 'FD')
    
    start_y = pdf.get_y()
    pdf.set_xy(12, start_y + 2)
    pdf.set_font('Arial', 'B', 9)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(186, 4.5, "CONFIGURAZIONE IMPIANTO BOR - FORMULA GLOBALE CHIAVI IN MANO", 0, 1, 'C')
    
    pdf.set_xy(12, start_y + 7.5)
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(186, 6.5, f"Euro {totale_finale:,.2f} + IVA", 0, 1, 'C')
    
    pdf.set_xy(12, start_y + 15)
    pdf.set_font('Arial', '', 7.5)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(186, 3.5, f"Dotazione attiva: {nodi_cam} Nodi Telecamera | {nodi_totali} Nodi Totali di Rete Presidiati", 0, 1, 'C')
    pdf.set_xy(12, start_y + 18.5)
    pdf.cell(186, 3.5, f"Quota Servizi Ingegnerizzazione e Laboratorio inclusa a corpo (Euro {assistenza:,.2f})", 0, 1, 'C')

    pdf.set_y(start_y + 28)

    # 2. Dettaglio Hardware per Macrocategorie
    pdf.box_sezione("2. COMPONENTI HARDWARE SUDDIVISI PER MACROCATEGORIE")
    categorie_map = {}
    for item in carrello_hw:
        cat = item['categoria']
        categorie_map.setdefault(cat, []).append(item)

    for cat_nome, prods in categorie_map.items():
        pdf.set_font('Arial', 'B', 7.5)
        pdf.set_text_color(30, 58, 138)
        pdf.cell(48, 3.8, f"- {cat_nome}:", 0, 0)
        
        dettagli_str = ", ".join([f"{p['qt']}x {p['nome']}" for p in prods])
        pdf.set_font('Arial', '', 7)
        pdf.set_text_color(51, 65, 85)
        pdf.multi_cell(0, 3.8, safe_str(dettagli_str))

    pdf.ln(2)

    # 3. Servizi di Ingegnerizzazione Inclusi
    pdf.box_sezione("3. SERVIZI BOR PER L'ATTIVAZIONE DEL SISTEMA (INCLUSI)")
    servizi_elenco = [
        ("Progettazione Tecnica Esecutiva", "Analisi vulnerabilita', coni visivi e piano planimetrico di copertura."),
        ("Pre-Configurazione in Laboratorio", "Assemblaggio a banco, cablaggio rack e stress-test apparati pre-posa."),
        ("Configurazione AI & Analisi Neurale", "Tracciamento perimetri virtuali avanzati a bordo camera per abbattimento falsi allarmi."),
        ("Direzione Lavori e Coordinamento", "Fornitura schemi esecutivi e supervisione costante maestranze sul cantiere."),
        ("Collaudo On-Site & Allaccio Remoto", "Orientamento ottiche congiunto con tecnici remoti e allaccio crittografato alla Centrale.")
    ]
    for tit, desc in servizi_elenco:
        pdf.set_font('Arial', 'B', 7.5)
        pdf.set_text_color(30, 58, 138)
        pdf.cell(50, 3.6, f"[INCLUSO] {tit}:", 0, 0)
        pdf.set_font('Arial', '', 7)
        pdf.set_text_color(51, 65, 85)
        pdf.cell(0, 3.6, desc, 0, 1)

    pdf.ln(2)

    # Politica Posa in Opera
    pdf.set_fill_color(254, 242, 242)
    pdf.set_draw_color(254, 202, 202)
    pdf.rect(10, pdf.get_y(), 190, 12, 'FD')
    pdf.set_xy(12, pdf.get_y() + 1.5)
    pdf.set_font('Arial', 'B', 7)
    pdf.set_text_color(185, 28, 28)
    pdf.cell(0, 3.2, "POLITICA DI POSA IN OPERA FISICA:", 0, 1)
    pdf.set_font('Arial', '', 6.5)
    pdf.set_text_color(69, 10, 10)
    pdf.multi_cell(186, 3, "La stesura cavi e posa fisica puo' essere affidata all'elettricista di fiducia del cliente (guidato dalla nostra Direzione Lavori) oppure preventivata a parte richiedendo un Installatore Partner Certificato BOR.")

    # ------------------ PAGINA 2 ------------------
    pdf.add_page()

    # 4. Canoni Telepresenza
    pdf.box_sezione("4. PROSPETTO CANONI MENSILI TELEPRESENZA E GUARDIANIA VIRTUALE")
    pdf.set_font('Arial', '', 7.5)
    pdf.set_text_color(51, 65, 85)
    pdf.multi_cell(0, 3.5, "Il canone include: Telepresenza su piattaforma BOR, Help Desk tecnologico costante da remoto e Chat Bidirezionale prioritaria con i Guardiani Virtuali.")
    pdf.ln(2)

    pdf.set_font('Arial', 'B', 8)
    pdf.set_fill_color(241, 245, 249)
    pdf.set_draw_color(203, 213, 225)
    pdf.cell(15, 6, 'Scelta', 1, 0, 'C', True)
    pdf.cell(90, 6, 'Profilo Operativo Centrale BOR', 1, 0, 'L', True)
    pdf.cell(40, 6, 'Modalita di Presidio', 1, 0, 'C', True)
    pdf.cell(45, 6, 'Canone Mensile (+IVA)', 1, 1, 'C', True)

    desc_profili = {
        "Su Inserimento (Zero Presenza)": "Sito disabitato/chiuso",
        "Fascia Oraria Notturna (22-06)": "Orari concordati fisso",
        "Su Inserimento (Con Presenza)": "Perimetro attivo c/persone",
        "H24 Senza Presenza": "Presidio continuo sito vuoto",
        "H24 Con Presenza": "Presidio continuo operativo"
    }

    pdf.set_font('Arial', '', 7.5)
    for nome_prof, canone in canoni_calcolati.items():
        pdf.cell(15, 5.5, '[   ]', 1, 0, 'C')
        pdf.set_font('Arial', 'B', 7.5)
        pdf.set_text_color(30, 41, 59)
        pdf.cell(90, 5.5, f' {nome_prof}', 1, 0, 'L')
        pdf.set_font('Arial', '', 7)
        pdf.set_text_color(71, 85, 105)
        pdf.cell(40, 5.5, desc_profili.get(nome_prof, ''), 1, 0, 'C')
        pdf.set_font('Arial', 'B', 8)
        pdf.set_text_color(30, 58, 138)
        pdf.cell(45, 5.5, f'Euro {canone:,.2f} / mese', 1, 1, 'C')

    pdf.ln(3)

    # 5. Moduli MSB Opzionali
    if servizi_sel:
        pdf.box_sezione("5. UPGRADE SERVIZI MENSILI PERSONALIZZATI (MSB)")
        pdf.set_font('Arial', '', 7.5)
        pdf.set_text_color(51, 65, 85)
        for s in servizi_sel:
            pdf.cell(15, 5, '[ X ]', 0, 0, 'C')
            pdf.set_font('Arial', 'B', 8)
            pdf.set_text_color(30, 41, 59)
            pdf.cell(115, 5, safe_str(s['nome']), 0, 0, 'L')
            pdf.set_font('Arial', 'B', 8)
            pdf.set_text_color(30, 58, 138)
            pdf.cell(0, 5, f'+ Euro {s["prezzo"]:,.2f} / mese', 0, 1, 'R')
        pdf.ln(2)

    # 6. Clausole e Firme
    pdf.box_sezione("6. CLAUSOLE DI SALVAGUARDIA, GARANZIE E ACCONTO")
    pdf.set_fill_color(248, 250, 252)
    pdf.set_draw_color(226, 232, 240)
    pdf.rect(10, pdf.get_y(), 190, 30, 'FD')
    
    curr_y = pdf.get_y() + 2
    pdf.set_xy(12, curr_y)
    pdf.set_font('Arial', 'B', 7.5)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(0, 3.5, "CLAUSOLA DI BLOCCO BUDGET E RECESSO GARANTITO (20%):", 0, 1)
    pdf.set_font('Arial', '', 7)
    pdf.set_text_color(51, 65, 85)
    acconto_val = safe_str(acconto) if acconto else "_______________"
    testo_clausola = (
        f"A conferma delle condizioni esposte, viene versato un acconto di Euro {acconto_val} a titolo di prenotazione "
        "slot e predisposizione centrale. Qualora il progetto esecutivo finale dovesse comportare una variazione del budget "
        "hardware superiore al 20%, il Cliente avra' diritto al recesso immediato con rimborso integrale dell'acconto."
    )
    pdf.multi_cell(186, 3.2, testo_clausola)
    
    pdf.set_xy(12, curr_y + 13.5)
    pdf.set_font('Arial', 'B', 7.5)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(0, 3.5, "REGIME DI GARANZIA TECNOLOGICA:", 0, 1)
    pdf.set_font('Arial', '', 7)
    pdf.set_text_color(51, 65, 85)
    garanzia_txt = (
        f"Copertura applicata: {safe_str(tipo_contratto)}. Include la sostituzione o riparazione degli apparati "
        "rilevati dalla telemetria del nostro Help Desk durante l'intero periodo di sottoscrizione attiva del servizio."
    )
    pdf.multi_cell(186, 3.2, garanzia_txt)

    pdf.set_y(curr_y + 32)
    pdf.set_font('Arial', 'B', 8)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(95, 5, 'Per il Cliente (Firma per Accettazione):', 0, 0, 'L')
    pdf.cell(95, 5, 'Per BOR S.r.l. (Il Security Manager):', 0, 1, 'L')
    pdf.ln(8)
    pdf.set_font('Arial', '', 8)
    pdf.cell(95, 4, 'Firma: ____________________________________', 0, 0, 'L')
    pdf.cell(95, 4, 'Firma: ____________________________________', 0, 1, 'L')

    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    pdf.output(temp_pdf.name)
    with open(temp_pdf.name, "rb") as f:
        bytes_out = f.read()
    try:
        os.remove(temp_pdf.name)
    except:
        pass
    return bytes_out

# ==========================================
# INTERFACCIA UTENTE (STREAMLIT CPQ)
# ==========================================
st.set_page_config(page_title="BOR CPQ - Preventivatore Ufficiale", page_icon="🛡️", layout="wide")

if os.path.exists("logo_bor.png"):
    st.image("logo_bor.png", width=220)
st.title("Configuratore Preventivi & Memorandum BOR")

# 1. Tenta caricamento automatico
file_locale = trova_file_excel_locale()
df_prodotti = None
df_servizi = None

if file_locale:
    try:
        p = pd.read_excel(file_locale, sheet_name='Videosorveglianza BOR')
        s = pd.read_excel(file_locale, sheet_name='Servizi BOR')
        df_prodotti, df_servizi = pulisci_dataframe(p, s)
    except Exception:
        pass

# 2. Fallback con uploader se il file non è presente nella cartella
if df_prodotti is None:
    st.info("💡 **Modalità Cloud / Primo Avvio:** Il catalogo non è presente sul server. Trascina qui sotto il file Excel del listino per iniziare la sessione.")
    up = st.file_uploader("Carica file Excel 'Sviluppo Elenco Prodotti BOR con Codici - 2026.xlsx'", type=["xlsx"])
    if up is not None:
        try:
            p = pd.read_excel(up, sheet_name='Videosorveglianza BOR')
            s = pd.read_excel(up, sheet_name='Servizi BOR')
            df_prodotti, df_servizi = pulisci_dataframe(p, s)
        except Exception as e:
            st.error("Errore nella lettura del file Excel caricato. Verifica che contenga i fogli 'Videosorveglianza BOR' e 'Servizi BOR'.")
            st.stop()
    else:
        st.stop()

# Session state per carrello e PDF
if "carrello_hw" not in st.session_state:
    st.session_state.carrello_hw = []
if "pdf_pronto" not in st.session_state:
    st.session_state.pdf_pronto = None
if "pdf_nomefile" not in st.session_state:
    st.session_state.pdf_nomefile = "Memorandum_BOR.pdf"

col_dati, col_cfg = st.columns([1, 2])

with col_dati:
    st.subheader("1. Dati Gestionali Offerta")
    cliente = st.text_input("Ragione Sociale / Cliente", placeholder="Es. Ditta Rossi S.r.l.")
    agente = st.text_input("Security Manager (Progettista)", placeholder="Es. Giuliano Salomone")
    acconto = st.text_input("Acconto Proposto (Euro)", placeholder="Es. 1.500,00")
    note = st.text_area("Note Progettuali / Specifiche Varchi", placeholder="Es. Copertura perimetrale esterna e varco merci...")

    st.subheader("2. Parametri di Rischio")
    tipo_contratto = st.radio("Tipologia Contratto", ["Business (Garanzia 12 mesi)", "Residenziale (Garanzia 24 mesi)"])
    
    st.markdown("**Fattori di Complessita' Ambientale:**")
    f_traffico = st.checkbox("Traffico continuo / Movimenti frequenti (+5%)")
    f_fornitori = st.checkbox("Transito frequente fornitori / Accessi merci (+10%)")
    f_multinucleo = st.checkbox("Piu' nuclei familiari / Sede condivisa (+15%)")
    k_ambiente = 1.0 + (0.05 if f_traffico else 0) + (0.10 if f_fornitori else 0) + (0.15 if f_multinucleo else 0)

with col_cfg:
    st.subheader("3. Selezione Componenti Hardware")
    
    macro_disponibili = sorted(df_prodotti['Macrocategoria'].unique())
    c1, c2, c3, c4 = st.columns([1.5, 2.5, 0.8, 1])
    
    with c1:
        cat_sel = st.selectbox("Macrocategoria", macro_disponibili)
    with c2:
        prodotti_filtrati = df_prodotti[df_prodotti['Macrocategoria'] == cat_sel]
        prod_sel = st.selectbox("Articolo", prodotti_filtrati['Nome Articolo'].tolist())
    with c3:
        qt_sel = st.number_input("Qt.", min_value=1, value=1, step=1)
    with c4:
        st.write("")
        st.write("")
        if st.button("➕ Aggiungi", use_container_width=True):
            riga_prod = prodotti_filtrati[prodotti_filtrati['Nome Articolo'] == prod_sel].iloc[0]
            st.session_state.carrello_hw.append({
                "codice": riga_prod['Codice Prodotto'],
                "nome": riga_prod['Nome Articolo'],
                "categoria": riga_prod['Macrocategoria'],
                "prezzo_unit": float(riga_prod['Prezzo Unitario Listino']),
                "qt": int(qt_sel),
                "totale": float(riga_prod['Prezzo Unitario Listino']) * int(qt_sel),
                "tipo_nodo": str(riga_prod['Tipo Nodo'])
            })
            st.session_state.pdf_pronto = None
            st.rerun()

    # Distinta carrello
    if st.session_state.carrello_hw:
        df_carrello = pd.DataFrame(st.session_state.carrello_hw)
        st.dataframe(
            df_carrello[['categoria', 'nome', 'qt', 'prezzo_unit', 'totale']],
            column_config={
                "categoria": "Macrocategoria",
                "nome": "Componente",
                "qt": "Quantità",
                "prezzo_unit": st.column_config.NumberColumn("Listino Unit. (€)", format="%.2f €"),
                "totale": st.column_config.NumberColumn("Totale (€)", format="%.2f €")
            },
            use_container_width=True,
            hide_index=True
        )
        if st.button("🗑️ Svuota Distinta Componenti"):
            st.session_state.carrello_hw = []
            st.session_state.pdf_pronto = None
            st.rerun()
    else:
        st.info("Nessun articolo inserito. Seleziona una macrocategoria e premi '➕ Aggiungi'.")

    st.subheader("4. Canoni e Servizi di Telepresenza BOR")
    
    nodi_cam = sum(item['qt'] for item in st.session_state.carrello_hw if item['tipo_nodo'] == 'Camera')
    tariffe_core = [(4, 100.0), (8, 150.0), (16, 200.0), (32, 300.0), (48, 400.0), (64, 500.0)]
    quota_tele = 500.0 + ((nodi_cam - 64) // 16) * 100.0 if nodi_cam > 64 else 100.0
    for lim, tar in tariffe_core:
        if nodi_cam <= lim:
            quota_tele = tar
            break
            
    help_desk_tiers = [(8, 25.0), (16, 35.0), (32, 45.0), (48, 60.0), (64, 75.0)]
    quota_hd = 75.0
    for lim, tar in help_desk_tiers:
        if nodi_cam <= lim:
            quota_hd = tar
            break
            
    costo_chat = 15.0
    base_core = quota_tele + quota_hd + costo_chat

    moltiplicatori = {
        "Su Inserimento (Zero Presenza)": 1.00,
        "Fascia Oraria Notturna (22-06)": 1.05,
        "Su Inserimento (Con Presenza)": 1.20,
        "H24 Senza Presenza": 1.35,
        "H24 Con Presenza": 1.50
    }
    canoni_calcolati = {nome: round(base_core * mult * k_ambiente, 2) for nome, mult in moltiplicatori.items()}

    st.write(f"Nodi Video: **{nodi_cam}** | Base Core Calcolata: **Euro {canoni_calcolati['Su Inserimento (Zero Presenza)']:.2f} / mese**")

    servizi_mensili_disponibili = df_servizi[df_servizi['Macrocategoria'].str.contains('Mensili|Canoni', na=False)]
    servizi_selezionati = []
    
    cols_serv = st.columns(2)
    idx_s = 0
    for _, s_row in servizi_mensili_disponibili.iterrows():
        with cols_serv[idx_s % 2]:
            attivo = st.checkbox(f"{s_row['Nome Articolo']} (+{s_row['Prezzo Unitario Listino']:.2f} €/mese)")
            if attivo:
                servizi_selezionati.append({
                    "codice": s_row['Codice Prodotto'],
                    "nome": s_row['Nome Articolo'],
                    "prezzo": float(s_row['Prezzo Unitario Listino'])
                })
        idx_s += 1

# ==========================================
# GENERAZIONE E DOWNLOAD PREVENTIVO PDF
# ==========================================
st.markdown("---")
st.header("5. Riepilogo Economico & Esportazione PDF")

if st.session_state.carrello_hw:
    tot_hw = sum(item['totale'] for item in st.session_state.carrello_hw)
    nodi_tot = sum(item['qt'] for item in st.session_state.carrello_hw if item['tipo_nodo'] in ['Camera', 'Audio', 'MSB_Fog', 'MSB_Sos', 'MSB_Gate'])
    assistenza = calcola_assistenza_bor(nodi_tot)
    totale_finale = tot_hw + assistenza

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Totale Hardware di Listino", f"Euro {tot_hw:,.2f}")
    m2.metric("Ingegnerizzazione Inclusa", f"Euro {assistenza:,.2f}")
    m3.metric("Offerta a Corpo Finita", f"Euro {totale_finale:,.2f} + IVA")
    m4.metric("Nodi Rete Totali", f"{nodi_tot} Nodi")

    st.write("")
    
    if st.button("🚀 GENERA PREVENTIVO PDF UFFICIALE", type="primary", use_container_width=True):
        nome_pulito = f"Memorandum_BOR_{cliente.strip().replace(' ', '_') if cliente else 'Proposta'}.pdf"
        bytes_generati = genera_pdf_memorandum(
            cliente, agente, note, acconto, tipo_contratto,
            st.session_state.carrello_hw, servizi_selezionati, canoni_calcolati
        )
        st.session_state.pdf_pronto = bytes_generati
        st.session_state.pdf_nomefile = nome_pulito

    if st.session_state.pdf_pronto is not None:
        st.success(f"🎉 **Preventivo pronto per il download: {st.session_state.pdf_nomefile}**")
        st.download_button(
            label="📥 CLICCA QUI PER SCARICARE IL PREVENTIVO PDF (2 PAGINE)",
            data=st.session_state.pdf_pronto,
            file_name=st.session_state.pdf_nomefile,
            mime="application/pdf",
            type="secondary",
            use_container_width=True
        )
else:
    st.warning("Aggiungi almeno un componente hardware alla distinta per poter generare e scaricare il PDF.")
