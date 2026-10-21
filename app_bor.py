import streamlit as st
import pdfplumber
import re
from fpdf import FPDF
import tempfile
import datetime
import os
from PIL import Image

def safe_str(testo):
    if not testo:
        return ""
    conversione = {
        'à': "a'", 'á': "a'", 'è': "e'", 'é': "e'", 'ì': "i'", 'í': "i'",
        'ò': "o'", 'ó': "o'", 'ù': "u'", 'ú': "u'", '€': "Euro", '’': "'",
        '“': '"', '”': '"', '–': '-'
    }
    for k, v in conversione.items():
        testo = testo.replace(k, v)
    return testo.encode('latin-1', 'replace').decode('latin-1')

TARIFFE_CORE = [(4, 100.0), (8, 150.0), (16, 200.0), (32, 300.0), (48, 400.0), (64, 500.0)]
HELP_DESK_TIERS = [(8, 25.0), (16, 35.0), (32, 45.0), (48, 60.0), (64, 75.0)]
COSTO_CHAT = 15.0

MOLTIPLICATORI_PROFILO = {
    "Su Inserimento (Zero Presenza)": 1.00,
    "Fascia Oraria Notturna (22-06)": 1.05,
    "Su Inserimento (Con Presenza)": 1.20,
    "H24 Senza Presenza": 1.35,
    "H24 Con Presenza": 1.50
}
ASSISTENZA_BOR_TIERS = [(4, 100.0), (8, 150.0), (16, 250.0), (32, 400.0), (48, 600.0)]

class MemorandumBOR_PDF(FPDF):
    def __init__(self, cliente, agente, sede, note_progetto):
        super().__init__()
        self.cliente = safe_str(cliente)
        self.agente = safe_str(agente)
        self.sede = safe_str(sede)
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
        self.ln(7)

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
        self.set_font('Arial', 'B', 9)
        self.set_fill_color(30, 58, 138)
        self.set_text_color(255, 255, 255)
        self.cell(0, 6, f'  {titolo}', 0, 1, 'L', True)
        self.ln(2)

def genera_pdf_bytes(dati_soluzioni, k_ambiente, tipo_contratto, msb_rilevati, cliente, agente, sede, note, acconto_proposto):
    pdf = MemorandumBOR_PDF(cliente, agente, sede, note)
    pdf.set_auto_page_break(auto=False, margin=12)
    
    pdf.add_page()
    pdf.set_fill_color(248, 250, 252)
    pdf.set_draw_color(226, 232, 240)
    pdf.rect(10, 27, 190, 24, 'FD')
    
    pdf.set_xy(12, 29)
    pdf.set_font('Arial', 'B', 8)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(25, 4, 'Cliente / Ditta:', 0, 0)
    pdf.set_font('Arial', '', 8)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(70, 4, safe_str(cliente) if cliente else 'Da specificare', 0, 0)
    
    pdf.set_font('Arial', 'B', 8)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(28, 4, 'Security Manager:', 0, 0)
    pdf.set_font('Arial', '', 8)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 4, safe_str(agente) if agente else 'Team Tecnico BOR', 0, 1)

    pdf.set_xy(12, 34)
    pdf.set_font('Arial', 'B', 8)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(25, 4, 'Sede Impianto:', 0, 0)
    pdf.set_font('Arial', '', 8)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(70, 4, safe_str(sede) if sede else 'Come da sopralluogo', 0, 0)

    pdf.set_font('Arial', 'B', 8)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(28, 4, 'Data & Regime:', 0, 0)
    pdf.set_font('Arial', '', 8)
    pdf.set_text_color(30, 41, 59)
    data_str = datetime.datetime.now().strftime("%d/%m/%Y")
    pdf.cell(0, 4, f'{data_str} | {safe_str(tipo_contratto)}', 0, 1)

    pdf.set_xy(12, 39)
    pdf.set_font('Arial', 'B', 8)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(25, 4, 'Note Operative:', 0, 0)
    pdf.set_font('Arial', 'I', 7)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(0, 4, safe_str(note) if note else 'Configurazione su misura in base all\'analisi dei varchi e vulnerabilita.', 0, 1)

    pdf.set_y(54)
    pdf.box_sezione("1. DIMENSIONAMENTO INFRASTRUTTURA HARDWARE (A CORPO)")
    pdf.set_font('Arial', '', 8)
    pdf.set_text_color(51, 65, 85)
    pdf.multi_cell(0, 4, "L'investimento include la fornitura degli apparati, dorsali dati, firewall di bilanciamento e protezione blackout. Prezzo globale a corpo escluso cablaggio fisico (affidabile a partner BOR o ad elettricista di fiducia).")
    pdf.ln(2)

    col_w = 190 / len(dati_soluzioni)
    start_x = 10
    start_y = pdf.get_y()
    
    idx = 0
    for nome_sol, sol in dati_soluzioni.items():
        x_pos = start_x + (idx * col_w)
        pdf.set_fill_color(241, 245, 249)
        pdf.set_draw_color(203, 213, 225)
        pdf.rect(x_pos, start_y, col_w - 2, 32, 'FD')
        
        pdf.set_xy(x_pos, start_y + 2)
        pdf.set_font('Arial', 'B', 9)
        pdf.set_text_color(30, 58, 138)
        pdf.cell(col_w - 2, 5, f"[  ] OPZIONE {nome_sol}", 0, 1, 'C')
        
        pdf.set_xy(x_pos, start_y + 8)
        pdf.set_font('Arial', 'B', 11)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(col_w - 2, 7, f"Euro {sol['totale_finale']:,.2f}", 0, 1, 'C')
        
        pdf.set_xy(x_pos, start_y + 16)
        pdf.set_font('Arial', '', 7)
        pdf.set_text_color(71, 85, 105)
        pdf.cell(col_w - 2, 4, f"Nodi Telecamera: {sol['dati']['nodi_cam']}", 0, 1, 'C')
        pdf.set_x(x_pos)
        pdf.cell(col_w - 2, 4, f"Nodi Totali Rete: {sol['dati']['nodi_totali']}", 0, 1, 'C')
        pdf.set_x(x_pos)
        pdf.cell(col_w - 2, 4, "+ Assistenza BOR Inclusa", 0, 1, 'C')
        idx += 1

    pdf.set_y(start_y + 36)
    pdf.box_sezione("2. SERVIZI DI INGEGNERIZZAZIONE E ATTIVAZIONE SISTEMA (INCLUSI)")
    pdf.set_font('Arial', '', 7.5)
    pdf.set_text_color(30, 41, 59)
    
    servizi_elenco = [
        ("Progettazione Tecnica Esecutiva", "Analisi vulnerabilita', coni visivi e stesura del piano planimetrico di copertura."),
        ("Pre-Configurazione in Laboratorio", "Assemblaggio a banco, cablaggio rack e stress-test di tutti gli apparati prima della posa."),
        ("Configurazione AI & Analisi Neurale", "Tracciamento perimetri virtuali avanzati a bordo camera per abbattimento totale falsi allarmi."),
        ("Direzione Lavori e Coordinamento", "Fornitura schemi esecutivi e supervisione delle maestranze/elettricista sul cantiere."),
        ("Collaudo On-Site & Allaccio Remoto", "Orientamento ottiche congiunto con i tecnici remoti e allaccio crittografato alla Centrale.")
    ]
    
    for tit, desc in servizi_elenco:
        pdf.set_font('Arial', 'B', 8)
        pdf.set_text_color(30, 58, 138)
        pdf.cell(52, 4.2, f"[INCLUSO] {tit}:", 0, 0)
        pdf.set_font('Arial', '', 7.5)
        pdf.set_text_color(51, 65, 85)
        pdf.cell(0, 4.2, desc, 0, 1)

    pdf.ln(2)
    pdf.set_fill_color(254, 242, 242)
    pdf.set_draw_color(254, 202, 202)
    pdf.rect(10, pdf.get_y(), 190, 14, 'FD')
    pdf.set_xy(12, pdf.get_y() + 2)
    pdf.set_font('Arial', 'B', 7.5)
    pdf.set_text_color(185, 28, 28)
    pdf.cell(0, 4, "POLITICA DI POSA IN OPERA FISICA:", 0, 1)
    pdf.set_font('Arial', '', 7)
    pdf.set_text_color(69, 10, 10)
    pdf.multi_cell(0, 3.5, "La posa canaline e stesura cavi e' esclusa dal presente modulo e puo' essere affidata all'elettricista di fiducia del cliente (guidato dalla nostra Direzione Lavori) oppure appaltata a un Installatore Partner Certificato BOR con preventivo a parte.")

    pdf.add_page()
    pdf.box_sezione("3. CANONE MENSILE TELEPRESENZA E GUARDIANIA VIRTUALE")
    pdf.set_font('Arial', '', 8)
    pdf.set_text_color(51, 65, 85)
    pdf.multi_cell(0, 4, "Il servizio comprende: Telepresenza su piattaforma BOR, Help Desk tecnologico costante da remoto e Canale Chat Bidirezionale prioritario con i Guardiani Virtuali.")
    pdf.ln(2)

    sol_rif = list(dati_soluzioni.values())[-1]
    n_cam_rif = sol_rif["dati"]["nodi_cam"]

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
    for nome_prof, k_prof in MOLTIPLICATORI_PROFILO.items():
        canone = calcola_canone(n_cam_rif, k_prof, k_ambiente)
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

    if msb_rilevati:
        pdf.box_sezione("4. UPGRADE SERVIZI PERSONALIZZATI (MSB)")
        pdf.set_font('Arial', '', 7.5)
        pdf.set_text_color(51, 65, 85)
        for msb_nome, msb_prezzo in msb_rilevati:
            pdf.cell(15, 5, '[   ]', 0, 0, 'C')
            pdf.set_font('Arial', 'B', 8)
            pdf.set_text_color(30, 41, 59)
            pdf.cell(115, 5, safe_str(msb_nome), 0, 0, 'L')
            pdf.set_font('Arial', 'B', 8)
            pdf.set_text_color(30, 58, 138)
            pdf.cell(0, 5, f'+ Euro {msb_prezzo:,.2f} / mese', 0, 1, 'R')
        pdf.ln(2)

    pdf.box_sezione("5. CLAUSOLE DI SALVAGUARDIA, GARANZIE E ACCONTO")
    pdf.set_fill_color(248, 250, 252)
    pdf.set_draw_color(226, 232, 240)
    pdf.rect(10, pdf.get_y(), 190, 32, 'FD')
    
    curr_y = pdf.get_y() + 2
    pdf.set_xy(12, curr_y)
    pdf.set_font('Arial', 'B', 7.5)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(0, 3.5, "CLAUSOLA DI BLOCCO BUDGET E RECESSO GARANTITO (20%):", 0, 1)
    pdf.set_font('Arial', '', 7)
    pdf.set_text_color(51, 65, 85)
    acconto_val = safe_str(acconto_proposto) if acconto_proposto else "_______________"
    testo_clausola = (
        f"A conferma delle condizioni esposte, viene versato un acconto di Euro {acconto_val} a titolo di prenotazione "
        "slot e predisposizione centrale. Qualora il progetto esecutivo finale dovesse comportare una variazione del budget "
        "hardware superiore al 20%, il Cliente avra' diritto al recesso immediato con rimborso integrale dell'acconto."
    )
    pdf.multi_cell(186, 3.2, testo_clausola)
    
    pdf.set_xy(12, curr_y + 14)
    pdf.set_font('Arial', 'B', 7.5)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(0, 3.5, "REGIME DI GARANZIA TECNOLOGICA:", 0, 1)
    pdf.set_font('Arial', '', 7)
    pdf.set_text_color(51, 65, 85)
    garanzia_txt = (
        f"Copertura applicata: {safe_str(tipo_contratto)}. Include la sostituzione o riparazione di apparati difettosi "
        "rilevati dalla telemetria del nostro Help Desk durante l'intero periodo di sottoscrizione attiva del servizio."
    )
    pdf.multi_cell(186, 3.2, garanzia_txt)

    pdf.set_y(curr_y + 34)
    pdf.set_font('Arial', 'B', 8)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(95, 5, 'Per il Cliente (Firma per Accettazione Budget):', 0, 0, 'L')
    pdf.cell(95, 5, 'Per BOR S.r.l. (Il Security Manager):', 0, 1, 'L')
    pdf.ln(9)
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

def analizza_pdf_goose(file_pdf):
    articoli = []
    totale_importo_hardware = 0.0
    nodi_cam = 0
    nodi_totali = 0
    trigger_msb = set()

    with pdfplumber.open(file_pdf) as pdf:
        for pagina in pdf.pages:
            testo = pagina.extract_text()
            if not testo:
                continue
            for riga in testo.split('\n'):
                match = re.search(r'^([A-Z0-9_\-\+]+)\s+(.+?)\s+NR\s+(\d+)\s+([\d\.,]+)', riga)
                if match:
                    codice = match.group(1)
                    descrizione = match.group(2)
                    qt = int(match.group(3))
                    importo_str = match.group(4).replace('.', '').replace(',', '.')
                    try:
                        importo = float(importo_str)
                    except ValueError:
                        importo = 0.0

                    if any(serv in codice for serv in ['BORAiVision', 'BOR-Lab', 'Live Testing', 'ProjectManagement', 'TechnicalDesign', 'H24', 'CHAT', 'MON-TEC']):
                        continue

                    articoli.append({"codice": codice, "descrizione": descrizione, "qt": qt, "importo": importo})
                    totale_importo_hardware += importo

                    if codice.startswith('TC') or 'Camera' in descrizione or codice.startswith('BOR-Vision'):
                        nodi_cam += qt
                        nodi_totali += qt
                    elif codice.startswith('BOR-TwoWay') or codice.startswith('BOR-ActiveSpeaker'):
                        nodi_totali += qt
                    elif codice.startswith('COERCIZ') or codice.startswith('KITRCA') or codice.startswith('AU'):
                        nodi_totali += qt

                    if 'COERCIZ' in codice or 'T-ARAP' in codice:
                        trigger_msb.add(("MSB Antirapina H24", 69.0))
                    if 'KITRCA' in codice:
                        trigger_msb.add(("MSB Controllo Varchi Gate Check", 29.0))
                    if 'AU' in codice:
                        trigger_msb.add(("MSB Attivazione Nebbiogeni", 39.0))

    return {
        "articoli": articoli,
        "totale_hw": totale_importo_hardware,
        "nodi_cam": nodi_cam,
        "nodi_totali": nodi_totali,
        "trigger_msb": trigger_msb
    }

def calcola_canone(nodi_cam, k_profilo, k_ambiente):
    quota_tele = 500.0 + ((nodi_cam - 64) // 16) * 100.0 if nodi_cam > 64 else 100.0
    for limite, tariffa in TARIFFE_CORE:
        if nodi_cam <= limite:
            quota_tele = tariffa
            break

    quota_hd = 75.0
    for limite, tariffa in HELP_DESK_TIERS:
        if nodi_cam <= limite:
            quota_hd = tariffa
            break

    c_core = quota_tele + quota_hd + COSTO_CHAT
    return round(c_core * k_profilo * k_ambiente, 2)

def calcola_assistenza_bor(nodi_totali):
    for limite, tariffa in ASSISTENZA_BOR_TIERS:
        if nodi_totali <= limite:
            return tariffa
    return 800.0 + (nodi_totali - 48) * 15.0
icona_bor = (Image.open("logo_bor.png") if os.path.exists("logo_bor.png") else None

    icona_bor = (Image.open("logo_bor.png") if os.path.exists("logo_bor.png") else None)

st.set_page_config(
    page_title="BOR Security - Generatore Memorandum",
    page_icon=icona_bor,
    layout="wide",)
if os.path.exists("logo_bor.png"):
    st.image("logo_bor.png", width=260)
st.title("Generatore Memorandum Commerciale")

if "pdf_pronto" not in st.session_state:
    st.session_state.pdf_pronto = False
    st.session_state.pdf_bytes = None
    st.session_state.pdf_nomefile = "Memorandum_BOR.pdf"
    st.session_state.dati_soluzioni = None

col_sx, col_dx = st.columns([1, 2])

with col_sx:
    st.subheader("1. Dati Intestazione Documento")
    cliente = st.text_input("Ragione Sociale / Nome Cliente", placeholder="Es. Rossi & Figli S.p.A.")
    sede = st.text_input("Sede Impianto", placeholder="Es. Via Roma 12, Caserta")
    agente = st.text_input("Security Manager (Agente)", placeholder="Es. Giuliano Salomone")
    acconto = st.text_input("Acconto Proposto (Euro)", placeholder="Es. 1.500,00")
    note = st.text_area("Note e Personalizzazioni (Sopralluogo)", placeholder="Es. Attenzione al varco nord...")

    st.subheader("2. Parametri Tecnici e Rischio")
    tipo_contratto = st.radio("Tipologia Contratto", ["Business (Garanzia 12 mesi)", "Residenziale (Garanzia 24 mesi)"])
    
    st.markdown("**Fattori di Complessita' Ambientale:**")
    f_traffico = st.checkbox("Traffico continuo / Movimenti frequenti (+5%)")
    f_fornitori = st.checkbox("Transito frequente fornitori / Accessi merci (+10%)")
    f_multinucleo = st.checkbox("Piu' nuclei familiari / Sede condivisa (+15%)")
    
    k_ambiente = 1.0 + (0.05 if f_traffico else 0) + (0.10 if f_fornitori else 0) + (0.15 if f_multinucleo else 0)

with col_dx:
    st.subheader("3. Caricamento Distinte Tecniche Goose")
    pdf_base = st.file_uploader("Preventivo Goose - Soluzione BASE", type=["pdf"])
    pdf_media = st.file_uploader("Preventivo Goose - Soluzione MEDIA", type=["pdf"])
    pdf_full = st.file_uploader("Preventivo Goose - Soluzione FULL", type=["pdf"])

    if st.button("🚀 ELABORA E GENERA MEMORANDUM PDF", type="primary"):
        file_caricati = [("BASE", pdf_base), ("MEDIA", pdf_media), ("FULL", pdf_full)]
        file_validi = [f for f in file_caricati if f[1] is not None]

        if not file_validi:
            st.error("⚠️ Carica almeno un file PDF di Goose prima di procedere.")
        else:
            dati_soluzioni = {}
            msb_globali = set()

            for nome, file in file_validi:
                res = analizza_pdf_goose(file)
                assistenza = calcola_assistenza_bor(res["nodi_totali"])
                totale_finale = res["totale_hw"] + assistenza
                dati_soluzioni[nome] = {"dati": res, "assistenza": assistenza, "totale_finale": totale_finale}
                msb_globali.update(res["trigger_msb"])

            nome_file_pulito = f"Memorandum_BOR_{cliente.strip().replace(' ', '_') if cliente else 'Bozza'}.pdf"
            
            pdf_bytes = genera_pdf_finale(dati_soluzioni, k_ambiente, tipo_contratto, msb_globali, cliente, agente, sede, note, acconto)
            
            st.session_state.pdf_pronto = True
            st.session_state.pdf_bytes = pdf_bytes
            st.session_state.pdf_nomefile = nome_file_pulito
            st.session_state.dati_soluzioni = dati_soluzioni

if st.session_state.pdf_pronto and st.session_state.pdf_bytes is not None:
    st.markdown("---")
    st.success("🎉 **Il Memorandum PDF e' stato generato con successo ed e' pronto per la stampa!**")
    
    st.download_button(
        label="📥 CLICCA QUI PER SCARICARE IL MEMORANDUM PDF UFFICIALE (2 PAGINE)",
        data=st.session_state.pdf_bytes,
        file_name=st.session_state.pdf_nomefile,
        mime="application/pdf",
        type="primary"
    )
    
    st.markdown("---")
    st.header("📋 ANTEPRIMA DEI VALORI CALCOLATI A CORPO")
    cols = st.columns(len(st.session_state.dati_soluzioni))
    idx = 0
    for nome, sol in st.session_state.dati_soluzioni.items():
        with cols[idx]:
            st.subheader(f"Opzione {nome}")
            st.metric("Investimento a Corpo", f"Euro {sol['totale_finale']:,.2f} + IVA")
            st.write(f"- Nodi Video Rilevati: **{sol['dati']['nodi_cam']}**")
            st.write(f"- Quota Ingegnerizzazione Inclusa: Euro {sol['assistenza']:,.2f}")
        idx += 1
