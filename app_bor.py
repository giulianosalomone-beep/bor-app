import streamlit as st
import pdfplumber
import re
from fpdf import FPDF
import tempfile
import datetime
import os

# ==========================================
# GESTIONE SICURA DEI TESTI PER IL PDF
# ==========================================
def safe_str(testo):
    if not testo:
        return ""
    conversione = {
        'à': "a'", 'á': "a'", 'è': "e'", 'é': "e'", 'ì': "i'", 'í': "i'",
        'ò': "o'", 'ó': "o'", 'ù': "u'", 'ú': "u'", '€': "Euro", '’': "'",
        '“': '"', '”': '"', '–': '-', '\t': ' '
    }
    for k, v in conversione.items():
        testo = testo.replace(k, v)
    return testo.encode('latin-1', 'replace').decode('latin-1')

# ==========================================
# CONFIGURAZIONE PARAMETRI E TARIFFE BOR
# ==========================================
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

# ==========================================
# MOTORE DI CATEGORIZZAZIONE ARTICOLI
# ==========================================
def categorizza_componente(codice, desc):
    c_upper = codice.upper()
    d_upper = desc.upper()
    
    if any(s in c_upper for s in ['AIVISION', 'LABSETUP', 'LIVETESTING', 'PROJECTMANAGEMENT', 'TECHNICALDESIGN', 'LIVE TESTING']):
        return "Servizi Attivazione"
    
    if any(k in c_upper for k in ['COERCIZ', 'ARAP', 'GATECHECK', 'KITRCA', 'AU150', 'NEB', 'TEK', 'PRL']) or \
       any(k in d_upper for k in ['GATE CHECK', 'NEBBIOGENO', 'ANTIRAPINA', 'COERCIZIONE', 'BIOMETRICO', 'RICARICA']):
        return "Controllo Varchi e Dissuasione Attiva"
        
    if c_upper.startswith('TC') or 'VISIONSERVER' in c_upper or any(k in d_upper for k in ['NVR', 'TURRET', 'CAMERA', 'BULLET', 'DOME', 'OMNIVIEW']):
        return "Videosorveglianza"
        
    if any(k in c_upper for k in ['DATARACK', 'AUDIOSERVER', 'MOBILELINK', 'RACK']) or \
       any(k in d_upper for k in ['RACK', 'GUARDIAN SERVER', '4G', 'GESTIONE DA REMOTO']):
        return "Rack e Kit per la Gestione da remoto"
        
    if any(k in c_upper for k in ['TWOWAYAUDIO', 'ACTIVESPEAKER', 'AUDIO', 'SPEAKER']) or \
       any(k in d_upper for k in ['AUDIO', 'DIFFUSORE', 'DETERRENZA ATTIVA', 'VOCALE', 'ALTOPARLANTE']):
        return "Audio e Diffusione"
        
    if 'FIREWALL' in c_upper or 'CYBER' in c_upper or 'FIREWALL' in d_upper or 'CYBERSECURITY' in d_upper:
        return "Protezione Dati e Rete"
        
    if any(k in c_upper for k in ['POENETWORK', 'FIBERNETWORK', 'SWITCH', 'FIBRA']) or \
       any(k in d_upper for k in ['SWITCH', 'POE', 'FIBRA']):
        return "Infrastruttura di Rete"
        
    if any(k in c_upper for k in ['POWERBACKUP', 'UPS']) or any(k in d_upper for k in ['UPS', 'CONTINUITA', 'BLACKOUT']):
        return "Protezione Blackout"
        
    return "Accessori"

# ==========================================
# CLASSE PDF MEMORANDUM BOR
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

def genera_pdf_finale(dati_soluzioni, k_ambiente, tipo_contratto, msb_rilevati, cliente, agente, note, acconto_proposto):
    pdf = MemorandumBOR_PDF(cliente, agente, note)
    pdf.set_auto_page_break(auto=False, margin=10)
    
    # ------------------ PAGINA 1 ------------------
    pdf.add_page()
    
    # Intestazione Automatica
    pdf.set_fill_color(248, 250, 252)
    pdf.set_draw_color(226, 232, 240)
    pdf.rect(10, 26, 190, 18, 'FD')
    
    pdf.set_xy(12, 28)
    pdf.set_font('Arial', 'B', 8)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(24, 3.5, 'Cliente / Ditta:', 0, 0)
    pdf.set_font('Arial', 'B', 8)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(82, 3.5, safe_str(cliente) if cliente else 'Come da distinta tecnica', 0, 0)
    
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
    pdf.cell(82, 3.5, f'{data_str} | Proposta Riservata', 0, 0)

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
    pdf.cell(0, 3.5, safe_str(note) if note else "Configurazione su misura in base all'analisi dei varchi e criticita'.", 0, 1)

    pdf.set_y(47)

    # 1. Investimento Hardware a Corpo
    pdf.box_sezione("1. DIMENSIONAMENTO INFRASTRUTTURA HARDWARE (A CORPO)")
    col_w = 190 / len(dati_soluzioni)
    start_x = 10
    start_y = pdf.get_y()
    
    idx = 0
    for nome_sol, sol in dati_soluzioni.items():
        x_pos = start_x + (idx * col_w)
        pdf.set_fill_color(241, 245, 249)
        pdf.set_draw_color(203, 213, 225)
        pdf.rect(x_pos, start_y, col_w - 2, 24, 'FD')
        
        pdf.set_xy(x_pos, start_y + 1.5)
        pdf.set_font('Arial', 'B', 8.5)
        pdf.set_text_color(30, 58, 138)
        pdf.cell(col_w - 2, 4.5, f"[  ] OPZIONE {nome_sol}", 0, 1, 'C')
        
        pdf.set_xy(x_pos, start_y + 6.5)
        pdf.set_font('Arial', 'B', 10.5)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(col_w - 2, 6, f"Euro {sol['totale_finale']:,.2f}", 0, 1, 'C')
        
        pdf.set_xy(x_pos, start_y + 13.5)
        pdf.set_font('Arial', '', 7)
        pdf.set_text_color(71, 85, 105)
        pdf.cell(col_w - 2, 3.5, f"Nodi Video: {sol['dati']['nodi_cam']} | Nodi Rete: {sol['dati']['nodi_totali']}", 0, 1, 'C')
        pdf.set_x(x_pos)
        pdf.cell(col_w - 2, 3.5, "+ Servizi Attivazione BOR Inclusi", 0, 1, 'C')
        idx += 1

    pdf.set_y(start_y + 27)

    # 2. Dettaglio Dotazione per Macrocategorie
    pdf.box_sezione("2. COMPONENTI HARDWARE SUDDIVISI PER MACROCATEGORIE")
    sol_rif = list(dati_soluzioni.values())[-1]
    macro_map = sol_rif["dati"]["per_categoria"]
    
    for cat_nome, prods in macro_map.items():
        if cat_nome == "Servizi Attivazione" or not prods:
            continue
        pdf.set_font('Arial', 'B', 7.5)
        pdf.set_text_color(30, 58, 138)
        pdf.cell(48, 3.8, f"- {cat_nome}:", 0, 0)
        
        dettagli_str = ", ".join([f"{p['qt']}x {p['desc']}" for p in prods])
        pdf.set_font('Arial', '', 7)
        pdf.set_text_color(51, 65, 85)
        pdf.multi_cell(0, 3.8, safe_str(dettagli_str))

    pdf.ln(2)

    # 3. Servizi BOR per l'Attivazione del Sistema
    pdf.box_sezione("3. SERVIZI BOR PER L'ATTIVAZIONE DEL SISTEMA (INCLUSI)")
    servizi_elenco = [
        ("Progettazione Tecnica Esecutiva", "Analisi vulnerabilita', coni visivi e piano planimetrico di copertura."),
        ("Pre-Configurazione in Laboratorio", "Assemblaggio a banco, cablaggio rack e stress-test dispositivi pre-installazione."),
        ("Configurazione AI & Analisi Neurale", "Tracciamento perimetri virtuali a bordo camera per abbattimento totale falsi allarmi."),
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
    pdf.multi_cell(186, 3, "La stesura cavi e posa fisica e' esclusa e puo' essere affidata all'elettricista di fiducia del cliente (guidato dalla nostra Direzione Lavori) oppure preventivata separatamente con Installatore Partner Certificato BOR.")

    # ------------------ PAGINA 2 ------------------
    pdf.add_page()

    # 4. Canoni Telepresenza
    pdf.box_sezione("4. CANONE MENSILE TELEPRESENZA E GUARDIANIA VIRTUALE")
    pdf.set_font('Arial', '', 7.5)
    pdf.set_text_color(51, 65, 85)
    pdf.multi_cell(0, 3.5, "Il servizio comprende: Telepresenza attiva su piattaforma BOR, Help Desk tecnologico costante da remoto e Canale Chat Bidirezionale prioritario con i Guardiani Virtuali.")
    pdf.ln(2)

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
        pdf.box_sezione("5. UPGRADE SERVIZI PERSONALIZZATI (MSB)")
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

    # 6. Clausole, Garanzie e Firme
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
    acconto_val = safe_str(acconto_proposto) if acconto_proposto else "_______________"
    testo_clausola = (
        f"A conferma delle condizioni esposte, viene versato un acconto di Euro {acconto_val} a titolo di prenotazione "
        "slot e predisposizione centrale. Qualora il progetto finale dovesse comportare una variazione del budget "
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
# PARSER PDF GOOSE
# ==========================================
def analizza_pdf_goose(file_pdf):
    articoli = []
    totale_importo_hardware = 0.0
    nodi_cam = 0
    nodi_totali = 0
    trigger_msb = set()
    cliente_estratto = ""
    per_categoria = {
        "Videosorveglianza": [],
        "Rack e Kit per la Gestione da remoto": [],
        "Audio e Diffusione": [],
        "Infrastruttura di Rete": [],
        "Protezione Dati e Rete": [],
        "Protezione Blackout": [],
        "Controllo Varchi e Dissuasione Attiva": [],
        "Accessori": [],
        "Servizi Attivazione": []
    }

    with pdfplumber.open(file_pdf) as pdf:
        for idx_pag, pagina in enumerate(pdf.pages):
            testo = pagina.extract_text()
            if not testo:
                continue
            
            if idx_pag == 0 and not cliente_estratto:
                match_cl = re.search(r'INTESTATO\s+A\s*\n+([^\n\r]+)', testo, re.IGNORECASE)
                if match_cl:
                    candidato = match_cl.group(1).strip()
                    if not candidato.startswith(('TEL', 'CODICE', 'EMAIL', 'IBAN')):
                        cliente_estratto = candidato

            for riga in testo.split('\n'):
                match = re.search(r'^([A-Z0-9_\-\+]+)\s+(.+?)\s+NR\s+(\d+)\s+([\d\.,]+)', riga)
                if match:
                    codice = match.group(1)
                    descrizione = match.group(2).strip()
                    qt = int(match.group(3))
                    importo_str = match.group(4).replace('.', '').replace(',', '.')
                    try:
                        importo = float(importo_str)
                    except ValueError:
                        importo = 0.0

                    if any(serv in codice for serv in ['H24', 'CHAT', 'MON-TEC', 'BORGUARD']):
                        continue

                    cat = categorizza_componente(codice, descrizione)
                    per_categoria[cat].append({"codice": codice, "desc": descrizione, "qt": qt})

                    if cat == "Servizi Attivazione":
                        continue

                    articoli.append({"codice": codice, "descrizione": descrizione, "qt": qt, "importo": importo, "cat": cat})
                    totale_importo_hardware += importo

                    if cat == "Videosorveglianza":
                        if not 'VISIONSERVER' in codice.upper():
                            nodi_cam += qt
                        nodi_totali += qt
                    elif cat in ["Audio e Diffusione", "Controllo Varchi e Dissuasione Attiva"]:
                        nodi_totali += qt

                    if 'COERCIZ' in codice or 'T-ARAP' in codice:
                        trigger_msb.add(("MSB Antirapina H24", 69.0))
                    if 'KITRCA' in codice or 'GATECHECK' in codice:
                        trigger_msb.add(("MSB Controllo Varchi Gate Check", 29.0))
                    if 'AU' in codice or 'NEB' in codice:
                        trigger_msb.add(("MSB Attivazione Nebbiogeni", 39.0))

    return {
        "articoli": articoli,
        "totale_hw": totale_importo_hardware,
        "nodi_cam": nodi_cam,
        "nodi_totali": nodi_totali,
        "trigger_msb": trigger_msb,
        "cliente": cliente_estratto,
        "per_categoria": per_categoria
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

# ==========================================
# INTERFACCIA STREAMLIT
# ==========================================
st.set_page_config(page_title="BOR Security - Generatore Memorandum", page_icon="logo_bor.png" if os.path.exists("logo_bor.png") else None, layout="wide")

if "pdf_bytes" not in st.session_state:
    st.session_state.pdf_bytes = None
    st.session_state.pdf_nomefile = "Memorandum_BOR.pdf"
    st.session_state.dati_soluzioni = None
    st.session_state.cliente_estratto = ""

if os.path.exists("logo_bor.png"):
    st.image("logo_bor.png", width=220)
st.title("Generatore Memorandum Commerciale")

col_sx, col_dx = st.columns([1, 2])

with col_sx:
    st.subheader("1. Dati Gestionali Offerta")
    agente = st.text_input("Security Manager (Agente)", placeholder="Es. Giuliano Salomone")
    acconto = st.text_input("Acconto Proposto (Euro)", placeholder="Es. 1.500,00")
    note = st.text_area("Note e Personalizzazioni Esecutive", placeholder="Es. Riconfigurazione varchi perimetrali...")

    st.subheader("2. Parametri Tecnici e Rischio")
    tipo_contratto = st.radio("Tipologia Contratto", ["Business (Garanzia 12 mesi)", "Residenziale (Garanzia 24 mesi)"])
    
    st.markdown("**Fattori di Complessita' Ambientale:**")
    f_traffico = st.checkbox("Traffico continuo / Movimenti frequenti (+5%)")
    f_fornitori = st.checkbox("Transito frequente fornitori / Accessi merci (+10%)")
    f_multinucleo = st.checkbox("Piu' nuclei familiari / Sede condivisa (+15%)")
    
    k_ambiente = 1.0 + (0.05 if f_traffico else 0) + (0.10 if f_fornitori else 0) + (0.15 if f_multinucleo else 0)

with col_dx:
    st.subheader("3. Caricamento Distinte Tecniche Goose")
    st.info("Trascina qui i PDF esportati da Goose. I componenti verranno categorizzati in automatico e l'intestatario estratto dal documento.")
    pdf_base = st.file_uploader("Preventivo Goose - Soluzione BASE", type=["pdf"])
    pdf_media = st.file_uploader("Preventivo Goose - Soluzione MEDIA", type=["pdf"])
    pdf_full = st.file_uploader("Preventivo Goose - Soluzione FULL", type=["pdf"])

    file_caricati = [("BASE", pdf_base), ("MEDIA", pdf_media), ("FULL", pdf_full)]
    file_validi = [f for f in file_caricati if f[1] is not None]

    st.markdown("---")
    
    # PULSANTE FISSO IN EVIDENZA
    if st.button("🚀 ELABORA E GENERA MEMORANDUM PDF", type="primary", use_container_width=True):
        if not file_validi:
            st.warning("⚠️ Carica almeno un file PDF di Goose prima di elaborare.")
        else:
            dati_soluzioni = {}
            msb_globali = set()
            cliente_finale = ""

            for nome, file in file_validi:
                res = analizza_pdf_goose(file)
                assistenza = calcola_assistenza_bor(res["nodi_totali"])
                totale_finale = res["totale_hw"] + assistenza
                dati_soluzioni[nome] = {"dati": res, "assistenza": assistenza, "totale_finale": totale_finale}
                msb_globali.update(res["trigger_msb"])
                if not cliente_finale and res["cliente"]:
                    cliente_finale = res["cliente"]

            nome_file_pulito = f"Memorandum_BOR_{cliente_finale.strip().replace(' ', '_') if cliente_finale else 'Bozza'}.pdf"
            
            pdf_bytes = genera_pdf_finale(dati_soluzioni, k_ambiente, tipo_contratto, msb_globali, cliente_finale, agente, note, acconto)
            
            st.session_state.pdf_bytes = pdf_bytes
            st.session_state.pdf_nomefile = nome_file_pulito
            st.session_state.dati_soluzioni = dati_soluzioni
            st.session_state.cliente_estratto = cliente_finale

    # SE GENERATO, MOSTRA DOWNLOAD ED ELENCO MACROCATEGORIE
    if st.session_state.pdf_bytes is not None:
        st.success(f"🎉 **Memorandum pronto per: {st.session_state.cliente_estratto or 'Cliente Rilevato'}**")
        st.download_button(
            label="📥 SCARICA IL TUO MEMORANDUM PDF UFFICIALE (2 PAGINE)",
            data=st.session_state.pdf_bytes,
            file_name=st.session_state.pdf_nomefile,
            mime="application/pdf",
            type="primary",
            use_container_width=True
        )
        
        st.markdown("---")
        st.header("📋 SINTESI ECONOMICA A CORPO")
        cols = st.columns(len(st.session_state.dati_soluzioni))
        idx = 0
        for nome, sol in dati_soluzioni.items():
            with cols[idx]:
                st.subheader(f"Opzione {nome}")
                st.metric("Investimento Infrastruttura", f"Euro {sol['totale_finale']:,.2f} + IVA")
                st.write(f"- Nodi Video Rilevati: **{sol['dati']['nodi_cam']}**")
                st.write(f"- Quota Ingegnerizzazione Inclusa: Euro {sol['assistenza']:,.2f}")
            idx += 1

        st.markdown("---")
        st.header("🔍 COMPONENTI RAGGRUPPATI PER MACROCATEGORIA")
        for nome_opz, sol_obj in st.session_state.dati_soluzioni.items():
            with st.expander(f"Visualizza distinta categorizzata: Opzione {nome_opz}", expanded=True):
                cat_dict = sol_obj["dati"]["per_categoria"]
                for c_name, p_list in cat_dict.items():
                    if c_name != "Servizi Attivazione" and p_list:
                        st.markdown(f"**{c_name}:**")
                        for p in p_list:
                            st.write(f"- {p['qt']}x {p['desc']}")
