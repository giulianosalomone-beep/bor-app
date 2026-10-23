import streamlit as st
import pandas as pd
from fpdf import FPDF
import datetime
import os

# ==========================================
# 1. CATALOGO NATIVO IN MEMORIA (92 HARDWARE + SERVIZI)
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

DF_PROD = pd.DataFrame(CATALOGO_HARDWARE, columns=['Codice Prodotto', 'Nome Articolo', 'Macrocategoria', 'Prezzo Unitario Listino', 'Tipo Nodo'])

# ==========================================
# 2. LOGICA TARIFFE TELEPRESENZA BOR
# ==========================================
def get_tier_rates(n_cam):
    if n_cam <= 4:
        return "1-4", 100.0, 120.0, 150.0
    elif n_cam <= 16:
        return "4-16", 160.0, 180.0, 210.0
    elif n_cam <= 32:
        return "16-32", 220.0, 240.0, 270.0
    elif n_cam <= 48:
        return "32-48", 280.0, 300.0, 330.0
    elif n_cam <= 64:
        return "48-64", 340.0, 360.0, 390.0
    elif n_cam <= 80:
        return "64-80", 400.0, 420.0, 450.0
    elif n_cam <= 96:
        return "80-96", 460.0, 480.0, 510.0
    else:
        extra_steps = (n_cam - 96 + 15) // 16
        return f">96 (+{extra_steps})", 460.0 + extra_steps*60.0, 480.0 + extra_steps*60.0, 510.0 + extra_steps*60.0

def safe_str(testo):
    if not testo or pd.isna(testo): return ""
    conversione = {'à': "a'", 'á': "a'", 'è': "e'", 'é': "e'", 'ì': "i'", 'í': "i'", 'ò': "o'", 'ó': "o'", 'ù': "u'", 'ú': "u'", '€': "Euro", '’': "'", '“': '"', '”': '"', '–': '-', '\t': ' '}
    testo = str(testo)
    for k, v in conversione.items(): testo = testo.replace(k, v)
    return testo.encode('latin-1', 'replace').decode('latin-1')

def fmt_eur(val):
    return f"{val:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# ==========================================
# 3. MOTORE PDF (2 PAGINE FORMAT COMMERCIALE)
# ==========================================
class OffertaBOR_PDF(FPDF):
    def header(self):
        if os.path.exists("logo_bor.png"):
            self.image("logo_bor.png", 10, 6, h=12)
        else:
            self.set_xy(10, 8)
            self.set_font('Arial', 'B', 18)
            self.set_text_color(30, 58, 138)
            self.cell(40, 10, 'BOR', 0, 0, 'L')
        self.set_xy(50, 8)
        self.set_font('Arial', 'B', 11.5)
        self.set_text_color(30, 58, 138)
        self.cell(0, 5.5, 'PIANO DI INVESTIMENTO E MEMORANDUM OPERATIVO', 0, 1, 'R')
        self.set_font('Arial', 'I', 8)
        self.set_text_color(100, 116, 139)
        self.cell(0, 4, 'Documento Riservato ad Uso Commerciale', 0, 1, 'R')
        self.set_draw_color(30, 58, 138)
        self.set_line_width(0.6)
        self.line(10, 22.5, 200, 22.5)
        self.ln(5)

    def footer(self):
        self.set_y(-12)
        self.set_draw_color(226, 232, 240)
        self.set_line_width(0.3)
        self.line(10, 285, 200, 285)
        self.set_font('Arial', 'I', 7)
        self.set_text_color(148, 163, 184)
        self.cell(95, 8, 'BOR S.r.l. - Proposta Commerciale Riservata', 0, 0, 'L')
        self.cell(95, 8, f'Pagina {self.page_no()} di 2', 0, 0, 'R')

    def box_sezione(self, titolo):
        self.set_font('Arial', 'B', 8.5)
        self.set_fill_color(30, 58, 138)
        self.set_text_color(255, 255, 255)
        self.cell(0, 5.5, f'  {titolo}', 0, 1, 'L', True)
        self.ln(1.5)

def genera_pdf_commerciale(dati_testata, soluzioni_attive, upgrade_selezionati):
    pdf = OffertaBOR_PDF()
    pdf.set_auto_page_break(auto=False, margin=10)
    
    # ------------------ PAGINA 1 ------------------
    pdf.add_page()
    
    # Box Dati Commessa
    pdf.set_fill_color(248, 250, 252)
    pdf.set_draw_color(226, 232, 240)
    pdf.rect(10, 25, 190, 22, 'FD')
    
    pdf.set_xy(12, 27)
    pdf.set_font('Arial', 'B', 8)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(32, 3.5, 'CLIENTE / RAG. SOC.:', 0, 0)
    pdf.set_font('Arial', 'B', 8)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(68, 3.5, safe_str(dati_testata.get('cliente', 'Destinatario')), 0, 0)
    
    pdf.set_font('Arial', 'B', 8)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(32, 3.5, 'RIF. COMMESSA BOR:', 0, 0)
    pdf.set_font('Arial', '', 8)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 3.5, safe_str(dati_testata.get('crm', 'N/D')), 0, 1)

    pdf.set_xy(12, 32)
    pdf.set_font('Arial', 'B', 8)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(32, 3.5, 'TIPOLOGIA SITO:', 0, 0)
    pdf.set_font('Arial', '', 8)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(68, 3.5, safe_str(dati_testata.get('sito', 'N/D')), 0, 0)

    pdf.set_font('Arial', 'B', 8)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(32, 3.5, 'TIPO COMMESSA:', 0, 0)
    pdf.set_font('Arial', 'B', 8)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 3.5, safe_str(dati_testata.get('tipo_commessa', 'Business')), 0, 1)

    pdf.set_xy(12, 37)
    pdf.set_font('Arial', 'B', 8)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(32, 3.5, 'SECURITY MANAGER:', 0, 0)
    pdf.set_font('Arial', '', 8)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(68, 3.5, safe_str(dati_testata.get('agente', 'Team Tecnico')), 0, 0)

    pdf.set_font('Arial', 'B', 8)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(32, 3.5, 'DATA PROPOSTA:', 0, 0)
    pdf.set_font('Arial', '', 8)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 3.5, datetime.datetime.now().strftime("%d/%m/%Y"), 0, 1)

    pdf.set_y(51)

    # 1. Soluzioni Hardware Proposte
    pdf.box_sezione("1. LIVELLO DI COPERTURA E SISTEMI BOR OGGETTO DELLA PROPOSTA")
    
    descrizioni_livelli = {
        "Base": "Protezione essenziale focalizzata sui punti critici di potenziale intrusione. Solitamente non comprende il perimetro.",
        "Media": "Configurazione equilibrata incentrata sulle aree esposte a maggior rischio. Copertura parziale dei varchi.",
        "Full": "Massima protezione perimetrale e volumetrica. Abbatte tutte le vulnerabilita' e azzera totalmente i punti ciechi."
    }
    
    for sol_nome, sol_info in soluzioni_attive.items():
        carrello = sol_info['carrello']
        n_cam = sol_info['n_cam']
        tot_hw = sum(item['totale'] for item in carrello)
        
        pdf.set_fill_color(241, 245, 249)
        pdf.set_draw_color(30, 58, 138)
        pdf.set_line_width(0.3)
        
        pdf.set_font('Arial', 'B', 8.5)
        pdf.set_text_color(30, 58, 138)
        pdf.cell(130, 6, f"  [   ] OPZIONE {sol_nome.upper()} ({n_cam} Nodi Telecamera)", 1, 0, 'L', True)
        pdf.set_font('Arial', 'B', 9.5)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(60, 6, f"Euro {fmt_eur(tot_hw)} + IVA  ", 1, 1, 'R', True)
        
        pdf.set_font('Arial', 'I', 7)
        pdf.set_text_color(100, 116, 139)
        pdf.cell(190, 4, f"    {descrizioni_livelli.get(sol_nome, '')}", 0, 1, 'L')
        
        pdf.set_font('Arial', '', 7)
        pdf.set_text_color(51, 65, 85)
        items_str = ", ".join([f"{item['qt']}x {item['nome']}" for item in carrello])
        pdf.multi_cell(190, 3.5, f"    Dotazione: {safe_str(items_str)}")
        pdf.ln(1.5)

    # 2. Box Personalizzazioni e note (compilazione a penna)
    pdf.ln(2)
    pdf.box_sezione("2. PERSONALIZZAZIONI E NOTE OPERATIVE (ANNOTAZIONI A PENNA)")
    note_y = pdf.get_y()
    pdf.set_draw_color(203, 213, 225)
    pdf.rect(10, note_y, 190, 35, 'D')
    
    pdf.set_font('Arial', 'I', 7)
    pdf.set_text_color(148, 163, 184)
    pdf.set_xy(12, note_y + 1.5)
    pdf.cell(0, 3.5, "Spazio riservato al Security Manager per annotazioni, varchi speciali o specifiche concordate col Cliente:", 0, 1)
    
    pdf.set_draw_color(226, 232, 240)
    for ly in [note_y + 11, note_y + 19, note_y + 27]:
        pdf.line(13, ly, 197, ly)

    # ------------------ PAGINA 2 ------------------
    pdf.add_page()
    
    is_business = str(dati_testata.get('tipo_commessa', '')).startswith('Business')
    MANDATORY_ADD = 35.0 + 10.0 # BOR-M-Tech + BOR-Chat-Mobile
    
    # 3. Servizi e Canoni
    pdf.box_sezione("3. PROFILO DI TELEPRESENZA E GUARDIANIA VIRTUALE")
    
    pdf.set_font('Arial', '', 7.5)
    pdf.set_text_color(51, 65, 85)
    info_txt = (
        "Il canone mensile garantisce il presidio della Centrale Operativa BOR, con allaccio crittografato della telemetria, "
        "gestione degli eventi di allarme e telecomando in tempo reale. Le tariffe sono calcolate in base al numero di telecamere "
        "e includono di default tutti i moduli tecnologici essenziali."
    )
    pdf.multi_cell(190, 3.4, info_txt)
    pdf.ln(2)

    # Tabella Comparativa Canoni per ciascuna soluzione attiva
    pdf.set_font('Arial', 'B', 7.5)
    pdf.set_fill_color(241, 245, 249)
    pdf.set_draw_color(203, 213, 225)
    
    col_w_sol = 45
    col_w_prof = 48 if is_business else 32
    
    pdf.cell(col_w_sol, 6, "Soluzione Hardware", 1, 0, 'C', True)
    pdf.cell(25, 6, "Nodi Video", 1, 0, 'C', True)
    pdf.cell(col_w_prof + (24 if is_business else 0), 6, "Su Inserimento", 1, 0, 'C', True)
    pdf.cell(col_w_prof + (24 if is_business else 0), 6, "Fascia Oraria Notturna", 1, 0, 'C', True)
    if not is_business:
        pdf.cell(col_w_prof + 13, 6, "H24 Premium (Residenziale)", 1, 0, 'C', True)
    pdf.ln()

    for sol_nome, sol_info in soluzioni_attive.items():
        n_cam = sol_info['n_cam']
        tier_str, f_time_base, act_base, h24_base = get_tier_rates(n_cam)
        
        canone_act = act_base + MANDATORY_ADD
        canone_ftime = f_time_base + MANDATORY_ADD
        canone_h24 = h24_base + MANDATORY_ADD
        
        pdf.set_font('Arial', 'B', 7.5)
        pdf.set_text_color(30, 58, 138)
        pdf.cell(col_w_sol, 6, f"  Opzione {sol_nome.upper()}", 1, 0, 'L')
        
        pdf.set_font('Arial', '', 7.5)
        pdf.set_text_color(51, 65, 85)
        pdf.cell(25, 6, f"{n_cam} cam ({tier_str})", 1, 0, 'C')
        
        pdf.set_font('Arial', 'B', 8)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(col_w_prof + (24 if is_business else 0), 6, f"[  ] Euro {fmt_eur(canone_act)}/m", 1, 0, 'C')
        pdf.cell(col_w_prof + (24 if is_business else 0), 6, f"[  ] Euro {fmt_eur(canone_ftime)}/m", 1, 0, 'C')
        if not is_business:
            pdf.cell(col_w_prof + 13, 6, f"[  ] Euro {fmt_eur(canone_h24)}/m", 1, 0, 'C')
        pdf.ln()

    pdf.ln(2.5)

    # Box Servizi Inclusi di Default (BOR-M-Tech + BOR-Chat-Mobile)
    inc_box_y = pdf.get_y()
    pdf.set_fill_color(248, 250, 252)
    pdf.set_draw_color(203, 213, 225)
    pdf.rect(10, inc_box_y, 190, 16, 'FD')
    
    pdf.set_xy(12, inc_box_y + 1.5)
    pdf.set_font('Arial', 'B', 7)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(0, 3.2, "SERVIZI TECNOLOGICI STANDARD INCLUSI DI DEFAULT NEL CANONE MENSILE:", 0, 1)
    
    pdf.set_font('Arial', '', 6.8)
    pdf.set_text_color(51, 65, 85)
    pdf.set_xy(12, inc_box_y + 5.2)
    pdf.cell(92, 3.2, "[X] Telepresenza e Portierato Virtuale su Piattaforma BOR", 0, 0)
    pdf.cell(92, 3.2, "[X] BOR-M-Tech Help Desk Tecnologico & Telemetria (Euro 35,00/m incluso)", 0, 1)
    
    pdf.set_xy(12, inc_box_y + 9)
    pdf.cell(92, 3.2, "[X] Attivazione Protocolli Security & Presidio Centrale", 0, 0)
    pdf.cell(92, 3.2, "[X] BOR-Chat-Mobile Canale Diretto Guardiani Virtuali (Euro 10,00/m incluso)", 0, 1)

    pdf.set_xy(12, inc_box_y + 12.5)
    pdf.cell(92, 3.2, "[X] Licenza Ufficiale App My BOR (Controllo da Smartphone)", 0, 0)
    pdf.cell(92, 3.2, "[X] Manutenzione Software e Firma Digitale Crittografata", 0, 1)

    pdf.set_y(inc_box_y + 19)

    # 4. Upgrade Opzionali BOR (MSB)
    pdf.box_sezione("4. UPGRADE SERVIZI PERSONALIZZATI OPZIONALI (MSB)")
    upgrades_disponibili = [
        ("Servizio Anti-Rapina con Centrale Operativa H24", 69.0),
        ("Servizio di Ricezione e Gestione Segnali di Allarme", 75.0),
        ("Servizio Controllo Varchi e Varchi Biometrici Gate Check", 29.0)
    ]
    for u_nome, u_prezzo in upgrades_disponibili:
        attivo = any(u['nome'] == u_nome for u in upgrade_selezionati)
        mark = "[ X ]" if attivo else "[   ]"
        pdf.cell(12, 4.2, mark, 0, 0, 'C')
        pdf.set_font('Arial', 'B' if attivo else '', 7.5)
        pdf.set_text_color(30, 58, 138 if attivo else 30)
        pdf.cell(130, 4.2, safe_str(u_nome), 0, 0, 'L')
        pdf.set_font('Arial', 'B', 7.5)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(45, 4.2, f"+ Euro {fmt_eur(u_prezzo)} / mese", 0, 1, 'R')

    pdf.ln(2)

    # 5. Condizioni di Investimento e Posa in Opera
    pdf.box_sezione("5. CONDIZIONI DI INVESTIMENTO, POSA IN OPERA E REGIME CONTRATTUALE")
    
    pdf.set_font('Arial', 'B', 7.5)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(95, 3.8, "Modalita' di Acquisizione Hardware:", 0, 0)
    pdf.cell(95, 3.8, "Installazione e Posa in Opera Dispositivi:", 0, 1)

    pdf.set_font('Arial', '', 7)
    pdf.set_text_color(51, 65, 85)
    pdf.cell(95, 3.6, "[   ] Acquisto Diretto a Budget Fissato", 0, 0)
    pdf.cell(95, 3.6, "[   ] Affidata ad Impiantista Partner Certificato BOR (A corpo)", 0, 1)

    pdf.cell(95, 3.6, "[   ] Noleggio Operativo (Rata: Euro _____ /m per ___ mesi)", 0, 0)
    pdf.cell(95, 3.6, "[   ] Affidata ad Elettricista del Cliente (Sotto Dir. Lavori BOR)", 0, 1)

    pdf.ln(1.5)

    # Tutela Budget (Clausola 20%)
    tutela_y = pdf.get_y()
    pdf.set_fill_color(254, 242, 242)
    pdf.set_draw_color(254, 202, 202)
    pdf.rect(10, tutela_y, 190, 15, 'FD')
    
    pdf.set_xy(12, tutela_y + 1.2)
    pdf.set_font('Arial', 'B', 6.8)
    pdf.set_text_color(185, 28, 28)
    pdf.cell(0, 3, "TUTELA DEL BUDGET ED ACCONTO DI PRENOTAZIONE (GARANZIA RECESSO 20%):", 0, 1)
    
    pdf.set_font('Arial', '', 6.3)
    pdf.set_text_color(69, 10, 10)
    tutela_txt = (
        "Il Cliente versa l'acconto di prenotazione per bloccare le condizioni economiche e riservare lo slot in Centrale. "
        "Qualora il Progetto Esecutivo post-sopralluogo dovesse far emergere variazioni del budget superiori al 20%, "
        "il Cliente avra' diritto di recedere immediatamente senza penali con rimborso integrale dell'acconto."
    )
    pdf.multi_cell(186, 2.9, tutela_txt)

    # Regime Garanzia
    pdf.set_y(tutela_y + 16.5)
    pdf.set_font('Arial', 'B', 7)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(32, 3.5, "Regime di Garanzia:", 0, 0)
    pdf.set_font('Arial', '', 7)
    pdf.set_text_color(51, 65, 85)
    garanzia_txt = (
        "Contratto Business: 12 Mesi con sostituzione apparati e tele-assistenza." if is_business
        else "Contratto Residenziale: 24 Mesi con sostituzione apparati e tele-assistenza."
    )
    pdf.cell(0, 3.5, garanzia_txt, 0, 1)

    # Firme
    pdf.set_y(tutela_y + 22)
    pdf.set_font('Arial', 'B', 7.5)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(95, 4, 'Per il Cliente (Firma per Accettazione):', 0, 0, 'L')
    pdf.cell(95, 4, 'Per BOR S.r.l. (Il Security Manager):', 0, 1, 'L')
    pdf.ln(5.5)
    pdf.set_font('Arial', '', 7.5)
    pdf.cell(95, 3.5, 'Firma: ____________________________________', 0, 0, 'L')
    pdf.cell(95, 3.5, 'Firma: ____________________________________', 0, 1, 'L')

    raw = pdf.output(dest='S')
    return raw.encode('latin-1') if isinstance(raw, str) else bytes(raw)

# ==========================================
# 4. INTERFACCIA STREAMLIT CPQ
# ==========================================
st.set_page_config(page_title="BOR CPQ - Preventivatore Ufficiale", page_icon="🛡️", layout="wide")

if os.path.exists("logo_bor.png"):
    st.image("logo_bor.png", width=220)
st.title("Generatore Proposta Commerciale BOR")

# Session state per soluzioni
if "hw_base" not in st.session_state: st.session_state.hw_base = []
if "hw_media" not in st.session_state: st.session_state.hw_media = []
if "hw_full" not in st.session_state: st.session_state.hw_full = []

# ----------------- STEP 1 -----------------
st.header("1. Dati Gestionali Commessa")
c1, c2, c3, c4, c5 = st.columns([1.2, 1.5, 1.2, 1.5, 1.2])

with c1:
    crm_rif = st.text_input("Rif. Commessa CRM (Zoho)", placeholder="Es. COM-26034")
with c2:
    cliente = st.text_input("Cliente / Ragione Sociale", placeholder="Es. Rossi Costruzioni Srl")
with c3:
    tipologie = ["Azienda / Capannone", "Villa Indipendente", "Appartamento", "Condominio / Parco", "Negozio / Retail", "Esterno / Terreno", "Altro"]
    sito = st.selectbox("Tipologia Sito", tipologie)
with c4:
    tipo_commessa = st.radio("Tipologia Commessa", ["Business (Garanzia 12 Mesi)", "Residenziale (Garanzia 24 Mesi)"], horizontal=True)
with c5:
    agente = st.text_input("Security Manager", placeholder="Giuliano Salomone")

is_business = tipo_commessa.startswith("Business")
if is_business:
    st.info("ℹ️ **Commessa Business Selezionata:** I profili abilitati sono *Su Inserimento* e *Fascia Oraria Notturna*. Il profilo *H24 Premium* è escluso.")
else:
    st.info("🏡 **Commessa Residenziale Selezionata:** Tutti i profili di Telepresenza (*H24 Premium*, *Su Inserimento*, *Fascia Oraria*) sono disponibili.")

# ----------------- STEP 2 -----------------
st.markdown("---")
st.header("2. Composizione Hardware Soluzioni")
st.caption("Aggiungi i materiali nelle opzioni desiderate. Il conteggio delle telecamere determinerà in automatico la fascia e i canoni.")

tab_base, tab_media, tab_full = st.tabs(["🟢 Soluzione Base (Essenziale)", "🟡 Soluzione Media (Equilibrata)", "🔴 Soluzione Full (Massima)"])

def ui_selettore_soluzione(lista_carrello, suffix, sol_name):
    macro_disp = sorted(DF_PROD['Macrocategoria'].unique())
    col1, col2, col3, col4 = st.columns([1.5, 2.5, 0.8, 1])
    
    with col1:
        cat_sel = st.selectbox("Categoria", macro_disp, key=f"cat_{suffix}")
    with col2:
        prod_filtrati = DF_PROD[DF_PROD['Macrocategoria'] == cat_sel]
        prod_sel = st.selectbox("Articolo", prod_filtrati['Nome Articolo'].tolist(), key=f"prod_{suffix}")
    with col3:
        qt_sel = st.number_input("Qt.", min_value=1, value=1, step=1, key=f"qt_{suffix}")
    with col4:
        st.write("")
        st.write("")
        if st.button("➕ Aggiungi", key=f"add_{suffix}", use_container_width=True):
            riga = prod_filtrati[prod_filtrati['Nome Articolo'] == prod_sel].iloc[0]
            lista_carrello.append({
                "codice": riga['Codice Prodotto'],
                "nome": riga['Nome Articolo'],
                "categoria": riga['Macrocategoria'],
                "prezzo_unit": float(riga['Prezzo Unitario Listino']),
                "qt": int(qt_sel),
                "totale": float(riga['Prezzo Unitario Listino']) * int(qt_sel),
                "tipo_nodo": str(riga['Tipo Nodo'])
            })
            st.rerun()

    if lista_carrello:
        df_c = pd.DataFrame(lista_carrello)
        st.dataframe(
            df_c[['categoria', 'nome', 'qt', 'totale']],
            column_config={
                "categoria": "Macrocategoria",
                "nome": "Articolo",
                "qt": "Quantità",
                "totale": st.column_config.NumberColumn("Totale (€)", format="%.2f €")
            },
            use_container_width=True, hide_index=True
        )
        
        # Conteggio Telecamere e visualizzazione canoni live
        n_cam = sum(p['qt'] for p in lista_carrello if p['tipo_nodo'] == 'Camera')
        tot_hw = sum(p['totale'] for p in lista_carrello)
        tier_str, f_base, a_base, h_base = get_tier_rates(n_cam)
        
        c_act = a_base + 45.0
        c_ftime = f_base + 45.0
        c_h24 = h_base + 45.0
        
        st.markdown(f"**Riepilogo Soluzione {sol_name}:** Imponibile Hardware: **Euro {fmt_eur(tot_hw)} + IVA** | Telecamere: **{n_cam}** (Fascia Licenza: **{tier_str}**)")
        
        if is_business:
            st.write(f"👉 Canoni Mensili Calcolati: **Su Inserimento:** Euro {fmt_eur(c_act)}/m | **Fascia Oraria (22-06):** Euro {fmt_eur(c_ftime)}/m *(Help Desk + Chat inclusi)*")
        else:
            st.write(f"👉 Canoni Mensili Calcolati: **H24 Premium:** Euro {fmt_eur(c_h24)}/m | **Su Inserimento:** Euro {fmt_eur(c_act)}/m | **Fascia Oraria:** Euro {fmt_eur(c_ftime)}/m *(Help Desk + Chat inclusi)*")
            
        b1, b2 = st.columns([1, 1])
        with b1:
            if st.button("🗑️ Rimuovi Ultimo Articolo", key=f"del_{suffix}"):
                lista_carrello.pop()
                st.rerun()
        with b2:
            if st.button("⚠️ Svuota Questa Soluzione", key=f"clear_{suffix}"):
                lista_carrello.clear()
                st.rerun()
    else:
        st.info(f"Nessun componente presente nella Soluzione {sol_name}. Aggiungi apparati dal menu sopra.")

with tab_base: ui_selettore_soluzione(st.session_state.hw_base, "base", "Base")
with tab_media: ui_selettore_soluzione(st.session_state.hw_media, "media", "Media")
with tab_full: ui_selettore_soluzione(st.session_state.hw_full, "full", "Full")

# ----------------- STEP 3 -----------------
st.markdown("---")
st.header("3. Upgrade Opzionali BOR (MSB)")
upg1 = st.checkbox("Servizio Anti-Rapina con Centrale Operativa H24 (+ 69,00 €/mese)")
upg2 = st.checkbox("Servizio di Ricezione e Gestione Segnali di Allarme (+ 75,00 €/mese)")
upg3 = st.checkbox("Servizio Controllo Varchi e Varchi Biometrici Gate Check (+ 29,00 €/mese)")

upgrades_selezionati = []
if upg1: upgrades_selezionati.append({"nome": "Servizio Anti-Rapina con Centrale Operativa H24", "prezzo": 69.0})
if upg2: upgrades_selezionati.append({"nome": "Servizio di Ricezione e Gestione Segnali di Allarme", "prezzo": 75.0})
if upg3: upgrades_selezionati.append({"nome": "Servizio Controllo Varchi e Varchi Biometrici Gate Check", "prezzo": 29.0})

# ----------------- STEP 4 -----------------
st.markdown("---")
st.header("4. Generazione Proposta PDF Ufficiale")

soluzioni_attive = {}
if st.session_state.hw_base:
    soluzioni_attive["Base"] = {
        "carrello": st.session_state.hw_base,
        "n_cam": sum(item['qt'] for item in st.session_state.hw_base if item['tipo_nodo'] == 'Camera')
    }
if st.session_state.hw_media:
    soluzioni_attive["Media"] = {
        "carrello": st.session_state.hw_media,
        "n_cam": sum(item['qt'] for item in st.session_state.hw_media if item['tipo_nodo'] == 'Camera')
    }
if st.session_state.hw_full:
    soluzioni_attive["Full"] = {
        "carrello": st.session_state.hw_full,
        "n_cam": sum(item['qt'] for item in st.session_state.hw_full if item['tipo_nodo'] == 'Camera')
    }

if soluzioni_attive:
    dati_testata = {
        "crm": crm_rif,
        "cliente": cliente,
        "sito": sito,
        "tipo_commessa": tipo_commessa,
        "agente": agente
    }
    
    nome_pdf = f"Proposta_BOR_{cliente.strip().replace(' ', '_') if cliente else 'Offerta'}.pdf"
    
    pdf_bytes = genera_pdf_commerciale(dati_testata, soluzioni_attive, upgrades_selezionati)
    
    st.download_button(
        label="🚀 SCARICA IL PREVENTIVO COMMERCIALE PDF (2 PAGINE)",
        data=pdf_bytes,
        file_name=nome_pdf,
        mime="application/pdf",
        type="primary",
        use_container_width=True
    )
else:
    st.warning("⚠️ Compila almeno una soluzione (Base, Media o Full) per abilitare il download del preventivo.")
