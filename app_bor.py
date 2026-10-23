import streamlit as st
import pandas as pd
from fpdf import FPDF
import datetime
import os

# ==========================================
# 1. CATALOGO NATIVO IN MEMORIA (VELOCISSIMO)
# ==========================================
CATALOGO_HARDWARE = [
    ("BOR-VisionServer4", "NVR 4 Canali con Hard Disk 2TB", "Videosorveglianza", 790.0, "NVR"),
    ("BOR-VisionServer16", "NVR 16 Canali con Hard Disk 2TB", "Videosorveglianza", 1190.0, "NVR"),
    ("BOR-TC15LE-28-H", "Telecamera Turret 5MP 2.8mm", "Videosorveglianza", 239.0, "Camera"),
    ("BOR-TC25LB-2812-H", "Telecamera Bullet 5MP Varifocal 2.8 to 12mm", "Videosorveglianza", 249.0, "Camera"),
    ("BOR-TC35LB-2812-H", "Telecamera Turret 5MP Varifocal 2.8 to 12mm", "Videosorveglianza", 249.0, "Camera"),
    ("BOR-TC5SB-16KM-10", "Telecamera Turret 5MP OmniView 180°", "Videosorveglianza", 269.0, "Camera"),
    ("BOR-TC5EB-12KM-10", "Telecamera Bullet 5MP Varifocal 5 to 60mm", "Videosorveglianza", 575.0, "Camera"),
    ("BOR-TC4SB-28-I0", "Mini Dome 4MP da Interni", "Videosorveglianza", 249.0, "Camera"),
    ("BOR-TCPKC-Z28", "Telecamera Bullet Lettura Targa", "Videosorveglianza", 959.0, "Camera"),
    ("BOR-TTB-3MM", "Telecamera Bullet Termica Bi-Spectrum 3mm", "Videosorveglianza", 759.0, "Camera"),
    ("BOR-TTB-7MM", "Telecamera Bullet Termica Bi-Spectrum 7mm", "Videosorveglianza", 890.0, "Camera"),
    ("BOR-PTZ-4X", "Telecamera PTZ 4X da Esterni", "Videosorveglianza", 399.0, "Camera"),
    ("BOR-PTZ-25X", "Telecamera PTZ 25X da Esterni", "Videosorveglianza", 890.0, "Camera"),
    ("BOR-HardDisk-4TB", "Hard Disk di Espansione 4TB", "Videosorveglianza", 145.0, "Passivo"),
    ("BOR-LicenzePack", "Licenza PRO AI per Analisi Video Avanzata", "Licenze Analisi Video", 1017.0, "Passivo"),
    ("BOR-DataRack9", "Rack 9\" Pre-Assemblato con Dispositivi BOR", "Armadio Rack", 623.0, "Passivo"),
    ("BOR-DataRack12", "Rack 12\" Pre-Assemblato con Dispositivi BOR", "Armadio Rack", 739.0, "Passivo"),
    ("BOR-DataRack15", "Rack 15\" Pre-Assemblato con Dispositivi BOR", "Armadio Rack", 815.0, "Passivo"),
    ("BOR-AudioServer", "Kit Audio Amplificatore da Rack", "Kit per la Gestione da remoto", 647.0, "Passivo"),
    ("BOR-MobileLink", "Modulo di Comunicazione Ridondante 4G", "Kit per la Gestione da remoto", 213.0, "Passivo"),
    ("BOR-CyberFirewall", "Firewall Balancer Cybersecurity", "Protezione Rete & Blackout", 354.0, "Passivo"),
    ("BOR-PowerBackup20", "Gruppo di Continuita Online 2000VA", "Protezione Rete & Blackout", 600.0, "Passivo"),
    ("BOR-SmartControl", "Controller con Tags & App My BOR", "Controller & App", 115.0, "Passivo"),
    ("BOR-TwoWayAudio-In", "Terminale Audio Bidirezionale da Interni", "Audio Diffusione e Deterrenza", 375.0, "Audio"),
    ("BOR-TwoWayAudio-Out", "Terminale Audio Bidirezionale da Esterni", "Audio Diffusione e Deterrenza", 356.0, "Audio"),
    ("BOR-T-Audio10W", "Diffusore Audio a Tubo 10W", "Audio Diffusione e Deterrenza", 65.0, "Audio"),
    ("BOR-P-Audio10W", "Diffusore Audio a Parete 5/10W", "Audio Diffusione e Deterrenza", 65.0, "Audio"),
    ("BOR-PoeNetwork", "Switch POE Collegamento Dati", "Infrastruttura di Rete", 70.0, "Passivo"),
    ("BOR-FiberNetwork", "Switch per Collegamenti in Fibra", "Infrastruttura di Rete", 297.0, "Passivo"),
    ("BOR-MountingKit", "Kit Accessori e Box di Giunzione", "Accessori", 15.0, "Passivo"),
    ("BOR-WarningSign", "Cartello Monitore Dissuasione BOR", "Accessori", 0.0, "Passivo"),
    ("BOR-GateCheckMaster", "Modulo Gate Check per Varco Primario", "Controllo Varchi", 530.0, "MSB_Gate"),
    ("BOR-Coerc1-1", "Kit Anti Rapina 1 Lettore 1 Varco", "Sistemi Antirapina", 1480.0, "MSB_Sos"),
    ("BOR-T-Arap", "Telecomando Antirapina T-ARAP", "Sistemi Antirapina", 48.0, "MSB_Sos"),
    ("BOR-T-Neb150", "Sistema Nebbiogeno da 150mc", "Nebbiogeni", 1639.0, "MSB_Fog"),
    ("BOR-AU150mq", "Nebbiogeno Specialistico 150mq", "Nebbiogeni", 2899.0, "MSB_Fog"),
    ("BOR-AiVisionSetup", "Configurazione AI e Analisi Video Intelligente", "Servizi Attivazione", 250.0, "Passivo"),
    ("BOR-LabSetup", "Pre-Configurazione ed Assemblaggio Kit", "Servizi Attivazione", 150.0, "Passivo"),
    ("BOR-LiveTestingCalibration", "Collaudo On-Site ed Allaccio Piattaforme BOR", "Servizi Attivazione", 200.0, "Passivo"),
    ("BOR-ProjectManagement", "Direzione Lavori e Coordinamento Cantiere", "Servizi Attivazione", 650.0, "Passivo"),
    ("BOR-TechnicalDesign", "Progettazione Tecnica Esecutiva", "Servizi Attivazione", 250.0, "Passivo")
]

CATALOGO_SERVIZI = [
    ("BOR-H24-Stand-1", "Profilo H24 - Licenza Standard", "Servizi di Teleportierato", 150.0),
    ("BOR-ACT-Stand-1", "Profilo Su Inserimento - Licenza Standard", "Servizi di Teleportierato", 120.0),
    ("BOR-F-Time--Stand-1", "Profilo Fascia Oraria - Licenza Standard", "Servizi di Teleportierato", 100.0),
    ("BOR-M-Tech", "Monitoraggio Tecnologico ed Assistenza Help Desk", "Servizi Mensili (Canoni)", 35.0),
    ("BOR-Chat-Mobile", "Chat Bidirezionale con i Guardiani BOR", "Servizi Mensili (Canoni)", 10.0),
    ("COERCIZ-SERV", "Servizio Antirapina con Centrale Operativa H24", "Servizi Mensili (Canoni)", 69.0),
    ("BOR-AlarmDetect", "Servizio di Ricezione Allarmi", "Servizi Mensili (Canoni)", 75.0),
    ("BOR-Svc-GateAlarmCheck", "Servizio di Controllo Varchi", "Servizi Mensili (Canoni)", 29.0)
]

DF_PROD = pd.DataFrame(CATALOGO_HARDWARE, columns=['Codice Prodotto', 'Nome Articolo', 'Macrocategoria', 'Prezzo Unitario Listino', 'Tipo Nodo'])
DF_SERV = pd.DataFrame(CATALOGO_SERVIZI, columns=['Codice Prodotto', 'Nome Articolo', 'Macrocategoria', 'Prezzo Unitario Listino'])

# ==========================================
# FUNZIONI FORMAT E PDF
# ==========================================
def safe_str(testo):
    if not testo or pd.isna(testo): return ""
    conversione = {'à': "a'", 'á': "a'", 'è': "e'", 'é': "e'", 'ì': "i'", 'í': "i'", 'ò': "o'", 'ó': "o'", 'ù': "u'", 'ú': "u'", '€': "Euro", '’': "'", '“': '"', '”': '"', '–': '-', '\t': ' '}
    testo = str(testo)
    for k, v in conversione.items(): testo = testo.replace(k, v)
    return testo.encode('latin-1', 'replace').decode('latin-1')

def fmt_eur(val):
    return f"{val:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

class PropostaBOR_PDF(FPDF):
    def header(self):
        if os.path.exists("logo_bor.png"):
            self.image("logo_bor.png", 10, 6, h=12)
        else:
            self.set_xy(10, 8)
            self.set_font('Arial', 'B', 18)
            self.set_text_color(30, 58, 138)
            self.cell(40, 10, 'BOR', 0, 0, 'L')
        self.set_xy(50, 8)
        self.set_font('Arial', 'B', 12)
        self.set_text_color(30, 58, 138)
        self.cell(0, 5.5, 'PIANO DI INVESTIMENTO E MEMORANDUM OPERATIVO', 0, 1, 'R')
        self.set_font('Arial', '', 8)
        self.set_text_color(100, 116, 139)
        self.cell(0, 4, 'Documento Riservato', 0, 1, 'R')
        self.set_draw_color(30, 58, 138)
        self.set_line_width(0.6)
        self.line(10, 22, 200, 22)
        self.ln(6)

    def footer(self):
        self.set_y(-12)
        self.set_draw_color(226, 232, 240)
        self.set_line_width(0.3)
        self.line(10, 285, 200, 285)
        self.set_font('Arial', 'I', 7)
        self.set_text_color(148, 163, 184)
        self.cell(95, 8, 'BOR S.r.l. - Preventivo ad uso interno e riservato', 0, 0, 'L')
        self.cell(95, 8, f'Pagina {self.page_no()}', 0, 0, 'R')

    def box_sezione(self, titolo):
        self.set_font('Arial', 'B', 8.5)
        self.set_fill_color(30, 58, 138)
        self.set_text_color(255, 255, 255)
        self.cell(0, 5.5, f'  {titolo}', 0, 1, 'L', True)
        self.ln(1.5)

def genera_pdf_commerciale(dati_testata, soluzioni):
    pdf = PropostaBOR_PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # BOX DATI COMMESSA
    pdf.set_fill_color(248, 250, 252)
    pdf.set_draw_color(226, 232, 240)
    pdf.rect(10, 26, 190, 18, 'FD')
    pdf.set_xy(12, 28)
    pdf.set_font('Arial', 'B', 8)
    pdf.set_text_color(30, 58, 138)
    
    pdf.cell(32, 3.5, 'Cliente/Ragione Soc:', 0, 0)
    pdf.set_font('Arial', '', 8)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(70, 3.5, safe_str(dati_testata['cliente']), 0, 0)
    
    pdf.set_font('Arial', 'B', 8)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(32, 3.5, 'Rif. Commessa CRM:', 0, 0)
    pdf.set_font('Arial', '', 8)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 3.5, safe_str(dati_testata['crm']), 0, 1)

    pdf.set_xy(12, 32.5)
    pdf.set_font('Arial', 'B', 8)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(32, 3.5, 'Tipologia Sito:', 0, 0)
    pdf.set_font('Arial', '', 8)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(70, 3.5, safe_str(dati_testata['sito']), 0, 0)

    pdf.set_font('Arial', 'B', 8)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(32, 3.5, 'Security Manager:', 0, 0)
    pdf.set_font('Arial', '', 8)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 3.5, safe_str(dati_testata['agente']), 0, 1)

    pdf.set_xy(12, 37)
    pdf.set_font('Arial', 'B', 8)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(32, 3.5, "Data Compilazione:", 0, 0)
    pdf.set_font('Arial', '', 8)
    pdf.set_text_color(15, 23, 42)
    data_str = datetime.datetime.now().strftime("%d/%m/%Y")
    pdf.cell(0, 3.5, data_str, 0, 1)

    pdf.ln(5)

    # 1. LIVELLO DI COPERTURA E SOLUZIONI PROPOSTE
    pdf.box_sezione("1. SOLUZIONI PROPOSTE PER IL SISTEMA BOR")
    
    for sol_name, carrello in soluzioni.items():
        if carrello:
            totale = sum(item['totale'] for item in carrello)
            # Riquadro Totale Soluzione
            pdf.set_fill_color(241, 245, 249)
            pdf.set_draw_color(30, 58, 138)
            pdf.set_font('Arial', 'B', 10)
            pdf.set_text_color(30, 58, 138)
            pdf.cell(190, 8, f"  [ X ] SOLUZIONE {sol_name.upper()}  -  Valore Imponibile: Euro {fmt_eur(totale)} + IVA", 1, 1, 'L', True)
            
            # Dettaglio Materiali
            pdf.set_font('Arial', 'B', 7.5)
            pdf.set_text_color(15, 23, 42)
            pdf.cell(190, 5, "    Dettaglio Fornitura Tecnologica:", 0, 1, 'L')
            
            pdf.set_font('Arial', '', 7.5)
            pdf.set_text_color(51, 65, 85)
            for item in carrello:
                pdf.cell(5, 4, "", 0, 0)
                pdf.cell(15, 4, f"{item['qt']}x", 0, 0, 'R')
                pdf.cell(170, 4, safe_str(f"{item['nome']} ({item['categoria']})"), 0, 1, 'L')
            
            # Box Appunti a penna per il commerciale
            pdf.ln(2)
            pdf.set_font('Arial', 'I', 7)
            pdf.set_text_color(148, 163, 184)
            pdf.cell(190, 4, "Spazio per personalizzazioni e note (da compilare a penna):", 0, 1, 'L')
            
            pdf.set_draw_color(203, 213, 225)
            # Creiamo un rettangolo tratteggiato fittizio (linee vicine)
            start_y = pdf.get_y()
            pdf.rect(10, start_y, 190, 15, 'D')
            pdf.set_y(start_y + 18)

    # 2. CONDIZIONI DI INVESTIMENTO (Ultima Pagina o in coda)
    pdf.ln(5)
    pdf.box_sezione("2. CONDIZIONI DI INVESTIMENTO E POSA IN OPERA")
    
    pdf.set_font('Arial', 'B', 8)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 5, "Modalita' di Acquisizione Hardware:", 0, 1)
    pdf.set_font('Arial', '', 8)
    pdf.cell(0, 5, "[   ] Acquisto Diretto a Budget Fissato", 0, 1)
    pdf.cell(0, 5, "[   ] Noleggio Operativo con Riscatto Finale ( Rata: Euro ________ / mese per ____ mesi )", 0, 1)
    pdf.ln(3)
    
    pdf.set_font('Arial', 'B', 8)
    pdf.cell(0, 5, "Installazione e Posa in Opera dei Dispositivi:", 0, 1)
    pdf.set_font('Arial', '', 8)
    pdf.cell(0, 5, "[   ] Affidata ad un Impiantista Partner Certificato BOR (Preventivata separatamente)", 0, 1)
    pdf.cell(0, 5, "[   ] Affidata ad un Impiantista Elettrico di fiducia del Cliente (Sotto Direzione Lavori BOR)", 0, 1)
    pdf.ln(3)

    # Policy 20%
    pdf.set_fill_color(254, 242, 242)
    pdf.set_draw_color(254, 202, 202)
    pdf.rect(10, pdf.get_y(), 190, 18, 'FD')
    pdf.set_xy(12, pdf.get_y() + 2)
    pdf.set_font('Arial', 'B', 7.5)
    pdf.set_text_color(185, 28, 28)
    pdf.cell(0, 3.5, "TUTELA DEL BUDGET ED ACCONTO DI PRENOTAZIONE:", 0, 1)
    pdf.set_font('Arial', '', 7)
    pdf.set_text_color(69, 10, 10)
    clausola = "Il Cliente versa un acconto per bloccare le condizioni e prenotare la centrale. Qualora il Progetto Esecutivo post-sopralluogo comporti una variazione hardware superiore al 20%, il Cliente ha facolta' di recedere ottenendo la restituzione integrale dell'acconto."
    pdf.multi_cell(186, 3.5, clausola)
    
    # Firme
    pdf.set_y(pdf.get_y() + 15)
    pdf.set_font('Arial', 'B', 8)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(95, 5, 'Per il Cliente (Firma per Accettazione):', 0, 0, 'L')
    pdf.cell(95, 5, 'Per BOR S.r.l. (Il Security Manager):', 0, 1, 'L')
    pdf.ln(8)
    pdf.set_font('Arial', '', 8)
    pdf.cell(95, 4, 'Firma: ____________________________________', 0, 0, 'L')
    pdf.cell(95, 4, 'Firma: ____________________________________', 0, 1, 'L')

    raw_output = pdf.output(dest='S')
    if isinstance(raw_output, str):
        return raw_output.encode('latin-1')
    return bytes(raw_output)

# ==========================================
# INTERFACCIA STREAMLIT
# ==========================================
st.set_page_config(page_title="BOR CPQ - Proposta Commerciale", page_icon="🛡️", layout="wide")
st.title("Generatore Proposta Commerciale BOR")

# Inizializza i 3 carrelli
if "hw_base" not in st.session_state: st.session_state.hw_base = []
if "hw_media" not in st.session_state: st.session_state.hw_media = []
if "hw_full" not in st.session_state: st.session_state.hw_full = []

# ==========================================
# STEP 1: DATI CRM E CLIENTE
# ==========================================
st.header("1. Dati Gestionali Commessa")
col1, col2, col3, col4 = st.columns(4)
with col1:
    crm_rif = st.text_input("Rif. Commessa CRM (Zoho)", placeholder="Es. COM-26034")
with col2:
    cliente = st.text_input("Cliente / Ragione Sociale", placeholder="Mario Rossi SPA")
with col3:
    tipologie = ["Azienda / Capannone", "Villa Indipendente", "Appartamento", "Condominio / Parco", "Negozio / Retail", "Esterno / Terreno agricolo", "Altro"]
    sito = st.selectbox("Tipologia Sito", tipologie)
with col4:
    agente = st.text_input("Security Manager", placeholder="Nome Cognome")

# ==========================================
# STEP 2: CREAZIONE SOLUZIONI (TABS)
# ==========================================
st.markdown("---")
st.header("2. Composizione Soluzioni")
st.info("💡 Aggiungi prodotti ai carrelli che desideri proporre. Nel PDF finale compariranno SOLO le soluzioni per cui hai inserito almeno un articolo.")

tab_base, tab_media, tab_full = st.tabs(["🟢 Soluzione Base (Essenziale)", "🟡 Soluzione Media (Equilibrata)", "🔴 Soluzione Full (Massima)"])

def ui_selettore_prodotti(lista_carrello, suffix):
    macro_disp = sorted(DF_PROD['Macrocategoria'].unique())
    c1, c2, c3, c4 = st.columns([1.5, 2.5, 0.8, 1])
    with c1:
        cat_sel = st.selectbox("Categoria", macro_disp, key=f"cat_{suffix}")
    with c2:
        prod_filtrati = DF_PROD[DF_PROD['Macrocategoria'] == cat_sel]
        prod_sel = st.selectbox("Articolo", prod_filtrati['Nome Articolo'].tolist(), key=f"prod_{suffix}")
    with c3:
        qt_sel = st.number_input("Qt.", min_value=1, value=1, step=1, key=f"qt_{suffix}")
    with c4:
        st.write("")
        st.write("")
        if st.button("➕ Aggiungi", key=f"add_{suffix}", use_container_width=True):
            riga = prod_filtrati[prod_filtrati['Nome Articolo'] == prod_sel].iloc[0]
            lista_carrello.append({
                "codice": riga['Codice Prodotto'], "nome": riga['Nome Articolo'],
                "categoria": riga['Macrocategoria'], "prezzo_unit": float(riga['Prezzo Unitario Listino']),
                "qt": int(qt_sel), "totale": float(riga['Prezzo Unitario Listino']) * int(qt_sel),
                "tipo_nodo": str(riga['Tipo Nodo'])
            })
            st.rerun()

    if lista_carrello:
        df_carrello = pd.DataFrame(lista_carrello)
        st.dataframe(
            df_carrello[['categoria', 'nome', 'qt', 'totale']],
            column_config={"totale": st.column_config.NumberColumn("Totale (€)", format="%.2f €")},
            use_container_width=True, hide_index=True
        )
        if st.button("🗑️ Rimuovi Ultimo Articolo", key=f"del_{suffix}"):
            lista_carrello.pop()
            st.rerun()

with tab_base: ui_selettore_prodotti(st.session_state.hw_base, "base")
with tab_media: ui_selettore_prodotti(st.session_state.hw_media, "media")
with tab_full: ui_selettore_prodotti(st.session_state.hw_full, "full")

# ==========================================
# STEP 3: GENERAZIONE PDF 
# ==========================================
st.markdown("---")
st.header("3. Generazione Proposta PDF")

soluzioni_attive = {}
if st.session_state.hw_base: soluzioni_attive["Base"] = st.session_state.hw_base
if st.session_state.hw_media: soluzioni_attive["Media"] = st.session_state.hw_media
if st.session_state.hw_full: soluzioni_attive["Full"] = st.session_state.hw_full

if soluzioni_attive:
    dati_testata = {
        "crm": crm_rif,
        "cliente": cliente,
        "sito": sito,
        "agente": agente
    }
    
    nome_file = f"Proposta_BOR_{cliente.strip().replace(' ', '_') if cliente else 'Standard'}.pdf"
    
    if st.download_button(
        label="🚀 SCARICA IL PDF DELLA PROPOSTA COMMERCIALE",
        data=genera_pdf_commerciale(dati_testata, soluzioni_attive),
        file_name=nome_file,
        mime="application/pdf",
        type="primary",
        use_container_width=True
    ):
        pass
else:
    st.info("Compila almeno una soluzione (Base, Media o Full) per generare il PDF.")
