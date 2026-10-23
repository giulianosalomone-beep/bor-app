import streamlit as st
import pandas as pd
from fpdf import FPDF
import datetime
import os

# ==========================================
# 1. CATALOGO NATIVO IN MEMORIA (92 PRODOTTI + 26 SERVIZI)
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
    ("BOR-DataRack18", "Rack 18\" Pre-Assemblato con Dispositivi BOR", "Armadio Rack", 850.0, "Passivo"),
    ("BOR-DataRack22", "Rack 22\" Pre-Assemblato con Dispositivi BOR", "Armadio Rack", 1055.0, "Passivo"),
    ("BOR-Ripiano-Rack", "Ripiano Fisso per Armadio Rack", "Armadio Rack", 28.0, "Passivo"),
    ("BOR-Patch-Panel", "Patch Panel 24 Porte Cat.6", "Armadio Rack", 45.0, "Passivo"),
    ("BOR-Passacavi-Rack", "Pannello Passacavi 1U con Spazzola", "Armadio Rack", 18.0, "Passivo"),
    ("BOR-Multipresa-Rack", "Multipresa Rack 8 Posti Schuko con Interruttore", "Armadio Rack", 42.0, "Passivo"),
    ("BOR-Guida-Rack", "Kit Guide Laterali di Supporto Apparati", "Armadio Rack", 35.0, "Passivo"),
    ("BOR-Termostato-Rack", "Unita di Ventilazione a Tetto con Termostato", "Armadio Rack", 85.0, "Passivo"),
    ("BOR-Cavi-Patch-Kit", "Kit 10 Cavi Patch Cat.6 UTP 0.5m", "Armadio Rack", 22.0, "Passivo"),
    ("BOR-Serratura-Rack", "Serratura di Sicurezza con Chiave Cifrata", "Armadio Rack", 25.0, "Passivo"),
    ("BOR-Luce-LED-Rack", "Barra LED 1U Magnetica per Interno Rack", "Armadio Rack", 38.0, "Passivo"),
    ("BOR-Kit-Gabbie", "Set 50 Viti e Dadi a Gabbia M6 per Rack", "Armadio Rack", 15.0, "Passivo"),
    ("BOR-Ruote-Rack", "Kit 4 Ruote Piroettanti con Freno per Rack", "Armadio Rack", 48.0, "Passivo"),
    ("BOR-Zoccolo-Rack", "Zoccolo di Rialzo Base Rack da Pavimento", "Armadio Rack", 65.0, "Passivo"),
    ("BOR-AudioServer", "Kit Audio Amplificatore da Rack", "Kit per la Gestione da remoto", 647.0, "Passivo"),
    ("BOR-MobileLink", "Modulo di Comunicazione Ridondante 4G", "Kit per la Gestione da remoto", 213.0, "Passivo"),
    ("BOR-CyberFirewall", "Firewall Balancer Cybersecurity", "Protezione Rete & Blackout", 354.0, "Passivo"),
    ("BOR-PowerBackup20", "Gruppo di Continuita Online 2000VA", "Protezione Rete & Blackout", 600.0, "Passivo"),
    ("BOR-PowerBackup30", "Gruppo di Continuita Online 3000VA", "Protezione Rete & Blackout", 600.0, "Passivo"),
    ("BOR-PowBack30/27", "Gruppo di Continuita Online 3000VA/2700W", "Protezione Rete & Blackout", 1093.0, "Passivo"),
    ("BOR-PowPack30/27", "Pacco Batterie per UPS Online", "Protezione Rete & Blackout", 240.0, "Passivo"),
    ("BOR-SmartControl", "Controller con Tags & App My BOR", "Controller & App", 115.0, "Passivo"),
    ("BOR-SmartControlPlus", "Controller Aggiuntivo", "Controller & App", 230.0, "Passivo"),
    ("BOR-TwoWayAudio-In", "Terminale Audio Bidirezionale da Interni", "Audio Diffusione e Deterrenza", 375.0, "Audio"),
    ("BOR-TwoWayAudio-Out", "Terminale Audio Bidirezionale da Esterni", "Audio Diffusione e Deterrenza", 356.0, "Audio"),
    ("BOR-T-Audio10W", "Diffusore Audio a Tubo 10W", "Audio Diffusione e Deterrenza", 65.0, "Audio"),
    ("BOR-P-Audio10W", "Diffusore Audio a Parete 5/10W", "Audio Diffusione e Deterrenza", 65.0, "Audio"),
    ("BOR-D-Audio506", "Diffusore Audio 506", "Audio Diffusione e Deterrenza", 65.0, "Audio"),
    ("BOR-T-Audio30W", "Tromba Audio di Potenza 30W IP66", "Audio Diffusione e Deterrenza", 95.0, "Audio"),
    ("BOR-PoeNetwork", "Switch POE Collegamento Dati", "Infrastruttura di Rete", 70.0, "Passivo"),
    ("BOR-FiberNetwork", "Switch per Collegamenti in Fibra", "Infrastruttura di Rete", 297.0, "Passivo"),
    ("BOR-ModuliSFP", "Moduli per la Fibra", "Infrastruttura di Rete", 32.0, "Passivo"),
    ("BOR-C-MediaConv-F", "Coppia di Media Converter con Moduli SFP", "Infrastruttura di Rete", 116.0, "Passivo"),
    ("BOR-1-MediaConv-F", "Media Converter con Modulo SFP", "Infrastruttura di Rete", 58.0, "Passivo"),
    ("BOR-JB-I-15", "Scatola di Giunzione per Telecamera Turret", "Accessori", 12.0, "Passivo"),
    ("BOR-JB-G-4SB", "Scatola di Giunzione per Telecamera Turret", "Accessori", 12.0, "Passivo"),
    ("BOR-JB-G-35", "Scatola di Giunzione per Telecamera Turret", "Accessori", 13.0, "Passivo"),
    ("BOR-JB-G-25", "Scatola di Giunzione per Telecamera Bullet", "Accessori", 22.0, "Passivo"),
    ("BOR-SP-W-15", "Staffa da Parete per Telecamera", "Accessori", 22.0, "Passivo"),
    ("BOR-SP-W-25", "Staffa da Parete per Telecamera", "Accessori", 22.0, "Passivo"),
    ("BOR-SP-C-15", "Staffa da Soffitto Telescopica", "Accessori", 29.0, "Passivo"),
    ("BOR-SP-P-15", "Adattatore Palo per Telecamera", "Accessori", 19.0, "Passivo"),
    ("BOR-SP-A-15", "Adattatore Angolo per Telecamera", "Accessori", 22.0, "Passivo"),
    ("BOR-MountingKit", "Kit Accessori e Box di Giunzione", "Accessori", 15.0, "Passivo"),
    ("BOR-WarningSign", "Cartello Monitore Dissuasione BOR", "Accessori", 0.0, "Passivo"),
    ("BOR-Alim-12V", "Alimentatore Stabilizzato 12V 2A", "Accessori", 18.0, "Passivo"),
    ("BOR-GateCheckMaster", "Modulo Gate Check per Varco Primario", "Controllo Varchi", 530.0, "MSB_Gate"),
    ("BOR-GateCheckPlus", "Sensore Gate Check per Varchi Aggiuntivi", "Controllo Varchi", 90.0, "MSB_Gate"),
    ("BOR-Coerc1-1", "Kit Anti Rapina 1 Lettore 1 Varco", "Sistemi Antirapina", 1480.0, "MSB_Sos"),
    ("BOR-Coerc2-1", "Kit Anti Rapina 2 Lettori 1 Varco", "Sistemi Antirapina", 1730.0, "MSB_Sos"),
    ("BOR-Coerc2-2", "Kit Anti rapina 2 Lettori 2 Varchi", "Sistemi Antirapina", 1900.0, "MSB_Sos"),
    ("BOR-Coerc4-2", "Kit Anti Rapina 4 Lettori 2 Varchi", "Sistemi Antirapina", 2150.0, "MSB_Sos"),
    ("BOR-C-Coercz", "Unita Centrale BOR per Servizi di Sicurezza", "Sistemi Antirapina", 790.0, "MSB_Sos"),
    ("BOR-T-Arap", "Telecomando Antirapina T-ARAP", "Sistemi Antirapina", 48.0, "MSB_Sos"),
    ("BOR-Puls-Sos", "Pulsante Antirapina Fisico Silenzioso da Banco", "Sistemi Antirapina", 35.0, "MSB_Sos"),
    ("BOR-T-Neb150", "Sistema Nebbiogeno da 150mc", "Nebbiogeni", 1639.0, "MSB_Fog"),
    ("BOR-T-Neb240", "Sistema Nebbiogeno da 240mc", "Nebbiogeni", 2139.0, "MSB_Fog"),
    ("BOR-T-Neb400", "Sistema Nebbiogeno da 400mc", "Nebbiogeni", 3025.0, "MSB_Fog"),
    ("BOR-T-Neb600", "Sistema Nebbiogeno da 600mc", "Nebbiogeni", 3795.0, "MSB_Fog"),
    ("BOR-T-Neb900", "Sistema Nebbiogeno da 900mc", "Nebbiogeni", 4950.0, "MSB_Fog"),
    ("BOR-AU150mq", "Nebbiogeno Specialistico 150mq", "Nebbiogeni", 2899.0, "MSB_Fog"),
    ("BOR-Kit-Neb-1", "Ripiano per Gestione Nebbiogeno", "Nebbiogeni", 160.0, "MSB_Fog"),
    ("BOR-PRL-AKBPR3", "Prolunga per Ugello Nebbiogeno -TEK-", "Nebbiogeni", 192.0, "MSB_Fog"),
    ("BOR-2-TEK-RIC-BAG06T", "Ricarica Nebbiogeno -TEK- 240m Cubici", "Nebbiogeni", 96.0, "MSB_Fog"),
    ("BOR-Staffa-Neb", "Staffa di Montaggio Orientabile per Nebbiogeno", "Nebbiogeni", 75.0, "MSB_Fog"),
    ("BOR-Ugello-Dev", "Ugello con Deviazione Angolare 45°", "Nebbiogeni", 55.0, "MSB_Fog"),
    ("BOR-Tamper-Neb", "Kit Protezione Antimanomissione e Strappo", "Nebbiogeni", 45.0, "MSB_Fog"),
    ("BOR-Batteria-Neb", "Batteria di Backup Dedicata per Unita Nebbiogena", "Nebbiogeni", 68.0, "MSB_Fog"),
    ("BOR-Liquido-Test", "Flacone Liquido Nebbiogeno di Prova per Collaudo", "Nebbiogeni", 35.0, "MSB_Fog"),
    ("BOR-AiVisionSetup", "Configurazione AI e Analisi Video Intelligente", "Servizi Attivazione", 250.0, "Passivo"),
    ("BOR-LabSetup", "Pre-Configurazione ed Assemblaggio Kit", "Servizi Attivazione", 150.0, "Passivo"),
    ("BOR-LiveTestingCalibration", "Collaudo On-Site ed Allaccio Piattaforme BOR", "Servizi Attivazione", 200.0, "Passivo"),
    ("BOR-ProjectManagement", "Direzione Lavori e Coordinamento Cantiere", "Servizi Attivazione", 650.0, "Passivo"),
    ("BOR-TechnicalDesign", "Progettazione Tecnica Esecutiva", "Servizi Attivazione", 250.0, "Passivo")
]

CATALOGO_SERVIZI = [
    ("BOR-H24-Stand-1", "Profilo H24 - Licenza Standard (1-4)", "Servizi di Teleportierato", 150.0),
    ("BOR-H24-Stand-2", "Profilo H24 - Licenza Standard (4-16)", "Servizi di Teleportierato", 210.0),
    ("BOR-H24-Stand-3", "Profilo H24 - Licenza Standard (16-32)", "Servizi di Teleportierato", 270.0),
    ("BOR-H24-Stand-4", "Profilo H24 - Licenza Standard (32-48)", "Servizi di Teleportierato", 330.0),
    ("BOR-H24-Stand-5", "Profilo H24 - Licenza Standard (48-64)", "Servizi di Teleportierato", 390.0),
    ("BOR-H24-Stand-6", "Profilo H24 - Licenza Standard (64-80)", "Servizi di Teleportierato", 450.0),
    ("BOR-H24-Stand-7", "Profilo H24 - Licenza Standard (80-96)", "Servizi di Teleportierato", 510.0),
    ("BOR-ACT-Stand-1", "Profilo Su Inserimento - Licenza Standard (1-4)", "Servizi di Teleportierato", 120.0),
    ("BOR-ACT-Stand-2", "Profilo Su Inserimento - Licenza Standard (4-16)", "Servizi di Teleportierato", 180.0),
    ("BOR-ACT-Stand-3", "Profilo Su Inserimento - Licenza Standard (16-32)", "Servizi di Teleportierato", 240.0),
    ("BOR-ACT-Stand-4", "Profilo Su Inserimento - Licenza Standard (32-48)", "Servizi di Teleportierato", 300.0),
    ("BOR-ACT-Stand-5", "Profilo Su Inserimento - Licenza Standard (48-64)", "Servizi di Teleportierato", 360.0),
    ("BOR-ACT-Stand-6", "Profilo Su Inserimento - Licenza Standard (64-80)", "Servizi di Teleportierato", 420.0),
    ("BOR-ACT-Stand-7", "Profilo Su Inserimento - Licenza Standard (80-96)", "Servizi di Teleportierato", 480.0),
    ("BOR-F-Time--Stand-1", "Profilo Fascia Oraria - Licenza Standard (1-4)", "Servizi di Teleportierato", 100.0),
    ("BOR-F-Time--Stand-2", "Profilo Fascia Oraria - Licenza Standard (4-16)", "Servizi di Teleportierato", 160.0),
    ("BOR-F-Time--Stand-3", "Profilo Fascia Oraria - Licenza Standard (16-32)", "Servizi di Teleportierato", 220.0),
    ("BOR-F-Time--Stand-4", "Profilo Fascia Oraria - Licenza Standard (32-48)", "Servizi di Teleportierato", 280.0),
    ("BOR-F-Time--Stand-5", "Profilo Fascia Oraria - Licenza Standard (48-64)", "Servizi di Teleportierato", 340.0),
    ("BOR-F-Time--Stand-6", "Profilo Fascia Oraria - Licenza Standard (64-80)", "Servizi di Teleportierato", 400.0),
    ("BOR-F-Time-Stand-7", "Profilo Fascia Oraria - Licenza Standard (80-96)", "Servizi di Teleportierato", 460.0),
    ("BOR-M-Tech", "Monitoraggio Tecnologico ed Assistenza Help Desk", "Servizi Mensili (Canoni)", 35.0),
    ("BOR-Chat-Mobile", "Chat Bidirezionale con i Guardiani BOR", "Servizi Mensili (Canoni)", 10.0),
    ("COERCIZ-SERV", "Servizio Antirapina con Centrale Operativa H24", "Servizi Mensili (Canoni)", 69.0),
    ("BOR-AlarmDetect", "Servizio di Ricezione Allarmi", "Servizi Mensili (Canoni)", 75.0),
    ("BOR-Svc-GateAlarmCheck", "Servizio di Controllo Varchi", "Servizi Mensili (Canoni)", 29.0)
]

# Converti in DataFrame in memoria (0.0001 secondi)
DF_PROD = pd.DataFrame(CATALOGO_HARDWARE, columns=['Codice Prodotto', 'Nome Articolo', 'Macrocategoria', 'Prezzo Unitario Listino', 'Tipo Nodo'])
DF_SERV = pd.DataFrame(CATALOGO_SERVIZI, columns=['Codice Prodotto', 'Nome Articolo', 'Macrocategoria', 'Prezzo Unitario Listino'])

# ==========================================
# GESTIONE TESTI E FORMATTAZIONE
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

def fmt_eur(val):
    return f"{val:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

def calcola_assistenza_bor(nodi_totali):
    tiers = [(4, 100.0), (8, 150.0), (16, 250.0), (32, 400.0), (48, 600.0)]
    for limite, tariffa in tiers:
        if nodi_totali <= limite:
            return tariffa
    return 800.0 + (nodi_totali - 48) * 15.0

# ==========================================
# GENERATORE PDF OTTIMIZZATO (MEMORANDUM BOR)
# ==========================================
class MemorandumBOR_PDF(FPDF):
    def __init__(self, cliente, agente, note_progetto):
        super().__init__()
        self.cliente = safe_str(cliente)
        self.agente = safe_str(agente)
        self.note_progetto = safe_str(note_progetto)

    def header(self):
        # Logo controllato in altezza: y=6, h=13 (non tocca la riga a y=24.5)
        if os.path.exists("logo_bor.png"):
            self.image("logo_bor.png", 10, 6, h=13)
        else:
            self.set_xy(10, 8)
            self.set_font('Arial', 'B', 18)
            self.set_text_color(30, 58, 138)
            self.cell(40, 10, 'BOR', 0, 0, 'L')

        self.set_xy(50, 8)
        self.set_font('Arial', 'B', 12)
        self.set_text_color(30, 58, 138)
        self.cell(0, 5.5, 'MEMORANDUM OPERATIVO E DI INVESTIMENTO', 0, 1, 'R')
        self.set_font('Arial', '', 8)
        self.set_text_color(100, 116, 139)
        self.cell(0, 4, 'Sistemi di Sicurezza in Telepresenza e Gestione Eventi Critici', 0, 1, 'R')
        
        self.set_draw_color(30, 58, 138)
        self.set_line_width(0.6)
        self.line(10, 24.5, 200, 24.5)
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
    pdf.cell(0, 3.5, safe_str(note) if note else "Configurazione calcolata su misura delle criticita del sito.", 0, 1)

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
    pdf.cell(186, 6.5, f"Euro {fmt_eur(totale_finale)} + IVA", 0, 1, 'C')
    
    pdf.set_xy(12, start_y + 15)
    pdf.set_font('Arial', '', 7.5)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(186, 3.5, f"Dotazione attiva: {nodi_cam} Nodi Telecamera | {nodi_totali} Nodi Totali di Rete Presidiati", 0, 1, 'C')
    pdf.set_xy(12, start_y + 18.5)
    pdf.cell(186, 3.5, f"Quota Servizi Ingegnerizzazione e Laboratorio inclusa a corpo (Euro {fmt_eur(assistenza)})", 0, 1, 'C')

    pdf.set_y(start_y + 28)

    # 2. Dettaglio Hardware
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

    # 3. Servizi inclusi (larghezza colonna 64 mm per evitare sovrapposizioni)
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
        pdf.cell(64, 3.8, f"[INCLUSO] {tit}:", 0, 0)
        pdf.set_font('Arial', '', 7)
        pdf.set_text_color(51, 65, 85)
        pdf.cell(0, 3.8, desc, 0, 1)

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
        pdf.cell(45, 5.5, f'Euro {fmt_eur(canone)} / mese', 1, 1, 'C')

    pdf.ln(3)

    # 5. Moduli MSB
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
            pdf.cell(0, 5, f'+ Euro {fmt_eur(s["prezzo"])} / mese', 0, 1, 'R')
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

    raw_output = pdf.output(dest='S')
    if isinstance(raw_output, str):
        return raw_output.encode('latin-1')
    return bytes(raw_output)

# ==========================================
# INTERFACCIA STREAMLIT ULTRA-RAPIDA
# ==========================================
st.set_page_config(page_title="BOR CPQ - Preventivatore Ufficiale", page_icon="🛡️", layout="wide")

if os.path.exists("logo_bor.png"):
    st.image("logo_bor.png", width=220)
st.title("Configuratore Preventivi & Memorandum BOR")

if "carrello_hw" not in st.session_state:
    st.session_state.carrello_hw = []

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
    
    macro_disponibili = sorted(DF_PROD['Macrocategoria'].unique())
    c1, c2, c3, c4 = st.columns([1.5, 2.5, 0.8, 1])
    
    with c1:
        cat_sel = st.selectbox("Macrocategoria", macro_disponibili)
    with c2:
        prodotti_filtrati = DF_PROD[DF_PROD['Macrocategoria'] == cat_sel]
        prod_sel = st.selectbox("Articolo", prodotti_filtrati['Nome Articolo'].tolist())
    with c3:
        qt_sel = st.number_input("Qt.", min_value=1, value=1, step=1)
    with c4:
        st.write("")
        st.write("")
        # Nessun st.rerun(): aggiunta istantanea in memoria
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

    # Visualizzazione distinta carrello
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
        
        b_col1, b_col2 = st.columns([1, 1])
        with b_col1:
            if st.button("🗑️ Rimuovi Ultimo Articolo", use_container_width=True):
                st.session_state.carrello_hw.pop()
        with b_col2:
            if st.button("⚠️ Svuota Intera Distinta", use_container_width=True):
                st.session_state.carrello_hw = []
    else:
        st.info("Nessun articolo inserito. Seleziona una macrocategoria e clicca '➕ Aggiungi'.")

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

    st.write(f"Nodi Video: **{nodi_cam}** | Canone Base Calcolato: **Euro {fmt_eur(canoni_calcolati['Su Inserimento (Zero Presenza)'])} / mese**")

    servizi_mensili_disponibili = DF_SERV[DF_SERV['Macrocategoria'].str.contains('Mensili|Canoni', na=False)]
    servizi_selezionati = []
    
    cols_serv = st.columns(2)
    idx_s = 0
    for _, s_row in servizi_mensili_disponibili.iterrows():
        with cols_serv[idx_s % 2]:
            attivo = st.checkbox(f"{s_row['Nome Articolo']} (+{s_row['Prezzo Unitario Listino']:.2f} €/mese)", key=f"serv_{s_row['Codice Prodotto']}")
            if attivo:
                servizi_selezionati.append({
                    "codice": s_row['Codice Prodotto'],
                    "nome": s_row['Nome Articolo'],
                    "prezzo": float(s_row['Prezzo Unitario Listino'])
                })
        idx_s += 1

# ==========================================
# RIEPILOGO ECONOMICO E TASTO PDF DIRETTO
# ==========================================
st.markdown("---")
st.header("5. Riepilogo Economico & Esportazione PDF")

ha_articoli = len(st.session_state.carrello_hw) > 0

if ha_articoli:
    tot_hw = sum(item['totale'] for item in st.session_state.carrello_hw)
    nodi_tot = sum(item['qt'] for item in st.session_state.carrello_hw if item['tipo_nodo'] in ['Camera', 'Audio', 'MSB_Fog', 'MSB_Sos', 'MSB_Gate'])
    assistenza = calcola_assistenza_bor(nodi_tot)
    totale_finale = tot_hw + assistenza

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Totale Hardware Listino", f"Euro {fmt_eur(tot_hw)}")
    m2.metric("Ingegnerizzazione Inclusa", f"Euro {fmt_eur(assistenza)}")
    m3.metric("Offerta a Corpo Finita", f"Euro {fmt_eur(totale_finale)} + IVA")
    m4.metric("Nodi Rete Totali", f"{nodi_tot} Nodi")

    st.write("")
    nome_pulito = f"Memorandum_BOR_{cliente.strip().replace(' ', '_') if cliente else 'Proposta'}.pdf"

    pdf_bytes = genera_pdf_memorandum(
        cliente, agente, note, acconto, tipo_contratto,
        st.session_state.carrello_hw, servizi_selezionati, canoni_calcolati
    )

    st.download_button(
        label="🚀 SCARICA PREVENTIVO PDF UFFICIALE (2 PAGINE)",
        data=pdf_bytes,
        file_name=nome_pulito,
        mime="application/pdf",
        type="primary",
        use_container_width=True
    )
else:
    st.info("👆 Seleziona un componente hardware e clicca **➕ Aggiungi** per comporre l'offerta e sbloccare il download.")
    st.download_button(
        label="📥 Aggiungi almeno un componente per scaricare il PDF",
        data=b"",
        disabled=True,
        use_container_width=True
    )
