import os
import shutil
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)

def build_pdf():
    workspace_pdf = "/Users/rajanmishra/Desktop/hack2/TOUCHGRASS_UI_AND_WORKFLOW_GUIDE.pdf"
    downloads_pdf = "/Users/rajanmishra/Downloads/TOUCHGRASS_UI_AND_WORKFLOW_GUIDE.pdf"

    doc = SimpleDocTemplate(
        workspace_pdf,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom styles adhering to design tokens
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#1F5A3D'),
        spaceAfter=3
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#4A564F'),
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'Heading1Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#1F5A3D'),
        spaceBefore=10,
        spaceAfter=5
    )

    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#14201A'),
        spaceAfter=5
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7,
        leading=9,
        textColor=colors.HexColor('#14201A')
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7,
        leading=9,
        textColor=colors.HexColor('#1F5A3D')
    )

    elements = []

    # Title Banner
    elements.append(Paragraph("TOUCHGRASS — UI/UX & WORKFLOW ARCHITECTURE GUIDE", title_style))
    elements.append(Paragraph("Complete Specification of Flat Design Tokens, Product States, Buttons, & TabPFN Integration | Hacktoberfest 2026", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1F5A3D'), spaceAfter=8))

    # Core Philosophy
    elements.append(Paragraph("1. Core Workflow Philosophy: Attract ➔ Release ➔ Reward", h1_style))
    intro_p = (
        "Traditional digital platforms optimize for screen retention: <i>Attention ➔ More Screen Time ➔ Ad Impressions</i>. "
        "<b>TouchGrass reverses this funnel entirely:</b> "
        "<i>Attention ➔ Inspiring Mission ➔ PUT SCREEN AWAY ➔ Real-World Nature Immersion ➔ Quiet Growth</i>. "
        "The core principle is: <b>'The application succeeds when the user stops using it.'</b> "
        "The entire UI is built as a calm, distraction-free companion designed to get you off the screen in under 30 seconds."
    )
    elements.append(Paragraph(intro_p, body_style))

    # Design System & Tokens
    elements.append(Paragraph("2. Flat Design System & Strict Tokens", h1_style))
    tokens_p = (
        "<b>Fonts:</b> Fraunces (500) for titles/numbers; Figtree (400-700) for body/controls.<br/>"
        "<b>Light Theme:</b> Background #F6F7F4, Ink #14201A, Muted #4A564F, Border #DDE2DC, Input Border #CFD6D0, Card #FFFFFF.<br/>"
        "<b>Dark Theme (Outside Page):</b> Background #16211B, Text #EEF2EE, Muted #A9B6AD, Rings #3A4A41 (260px) & #6F8A78 (180px).<br/>"
        "<b>Accent & Style:</b> Deep Green #1F5A3D. Strictly flat: thin 1px borders, 12-16px radius, no shadows, no gradients, no emojis, no confetti."
    )
    elements.append(Paragraph(tokens_p, body_style))

    # Sequential States Table
    elements.append(Paragraph("3. Product States & Workflow Transitions", h1_style))
    state_table_data = [
        [
            Paragraph("State", table_header_style),
            Paragraph("Visual Theme", table_header_style),
            Paragraph("User Experience Purpose", table_header_style),
            Paragraph("Screen Action", table_header_style)
        ],
        [
            Paragraph("Page 1: MISSION", table_cell_bold),
            Paragraph("Clean #FFFFFF card on #F6F7F4, Fraunces headline, Figtree body.", table_cell_style),
            Paragraph("Presents outdoor challenge with duration pills, focus, reward, and TabPFN microclimate forecast.", table_cell_style),
            Paragraph("User selects 5m/15m/30m, listens to narration, or clicks <b>[Start mission]</b>.", table_cell_style)
        ],
        [
            Paragraph("Page 2: OUTSIDE", table_cell_bold),
            Paragraph("Deep forest #16211B, dual concentric rings (260px / 180px), large Fraunces countdown.", table_cell_style),
            Paragraph("<b>The screen ceases demanding attention.</b> Encourages pocketing device during walk.", table_cell_style),
            Paragraph("Counts down outdoor minutes; Web Audio Tibetan singing bowl chime sounds at 00:00. User clicks <b>[I'm back]</b>.", table_cell_style)
        ],
        [
            Paragraph("Page 3: COMPLETE", table_cell_bold),
            Paragraph("Calm light theme, Fraunces headline, 3-stat breakdown between 1px borders.", table_cell_style),
            Paragraph("Low-stimulation positive closure for real physical effort completed.", table_cell_style),
            Paragraph("User writes reflection (+10 XP), clicks <b>[Save reflection]</b> or <b>[Next mission]</b>.", table_cell_style)
        ],
        [
            Paragraph("Page 4: JOURNEY", table_cell_bold),
            Paragraph("Editorial dashboard with 3 lifetime metrics cards, 7-day activity completion row, reflections log.", table_cell_style),
            Paragraph("Permanent on-device record of screen-free progress, persisted safely in localStorage.", table_cell_style),
            Paragraph("User inspects previous entries and streaks; clicks <b>[Back to mission]</b>.", table_cell_style)
        ]
    ]

    t_states = Table(state_table_data, colWidths=[80, 140, 180, 140])
    t_states.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1F5A3D')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DDE2DC')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F6F7F4')]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(t_states)
    elements.append(Spacer(1, 8))

    # Buttons & Controls Table
    elements.append(Paragraph("4. Complete Dictionary of Buttons & UI Controls", h1_style))
    btn_table_data = [
        [
            Paragraph("Button / Control", table_header_style),
            Paragraph("Location", table_header_style),
            Paragraph("Action & Implementation", table_header_style),
            Paragraph("Behavioral Purpose", table_header_style)
        ],
        [
            Paragraph("Wordmark TouchGrass", table_cell_bold),
            Paragraph("Header Left", table_cell_style),
            Paragraph("Semantic &lt;button&gt; returning to Page 1", table_cell_style),
            Paragraph("Unobtrusive home anchor without page reloads", table_cell_style)
        ],
        [
            Paragraph("Mission / Journey Tabs", table_cell_bold),
            Paragraph("Header Center", table_cell_style),
            Paragraph("Switches active view; active tab colored #1F5A3D", table_cell_style),
            Paragraph("Clean navigation keeping focus on active mission", table_cell_style)
        ],
        [
            Paragraph("Offline mode Pill", table_cell_bold),
            Paragraph("Header Right", table_cell_style),
            Paragraph("Toggles offline trail banner & on-device mode", table_cell_style),
            Paragraph("Guarantees backcountry reliability with zero cell signal", table_cell_style)
        ],
        [
            Paragraph("[Start mission]", table_cell_bold),
            Paragraph("Page 1 Hero", table_cell_style),
            Paragraph("56px primary button transition to Outside page", table_cell_style),
            Paragraph("The commitment step from digital intent to physical action", table_cell_style)
        ],
        [
            Paragraph("[Listen]", table_cell_bold),
            Paragraph("Page 1 Hero", table_cell_style),
            Paragraph("Speaks mission title & guidance via speech synthesis", table_cell_style),
            Paragraph("Hands-free comprehension so user avoids reading screen", table_cell_style)
        ],
        [
            Paragraph("Another mission", table_cell_bold),
            Paragraph("Page 1 Hero", table_cell_style),
            Paragraph("Cycles through 5 distinct outdoor challenges", table_cell_style),
            Paragraph("Instant mission swap if weather or environment does not fit", table_cell_style)
        ],
        [
            Paragraph("Duration (5m/15m/30m)", table_cell_bold),
            Paragraph("Page 1 Card", table_cell_style),
            Paragraph("Dynamic timer duration selector and XP scaler", table_cell_style),
            Paragraph("Adapts challenge to user's real-world schedule", table_cell_style)
        ],
        [
            Paragraph("[Chime test]", table_cell_bold),
            Paragraph("Page 2 Header", table_cell_style),
            Paragraph("Synthesizes 528Hz + 1056Hz Web Audio bell resonance", table_cell_style),
            Paragraph("Verifies completion chime before putting phone in pocket", table_cell_style)
        ],
        [
            Paragraph("[Dim screen]", table_cell_bold),
            Paragraph("Page 2 Header", table_cell_style),
            Paragraph("Lowers screen opacity to 35% to save battery", table_cell_style),
            Paragraph("Minimizes screen glare while walking outdoors", table_cell_style)
        ],
        [
            Paragraph("[I'm back]", table_cell_bold),
            Paragraph("Page 2 Bottom", table_cell_style),
            Paragraph("Stops timer and opens Mission Complete page", table_cell_style),
            Paragraph("Triumphant return signaling physical mission completion", table_cell_style)
        ],
        [
            Paragraph("[Save reflection]", table_cell_bold),
            Paragraph("Page 3 Card", table_cell_style),
            Paragraph("Persists note, date, duration & XP to localStorage", table_cell_style),
            Paragraph("Mindfulness reinforcement and daily habit building", table_cell_style)
        ]
    ]

    t_btns = Table(btn_table_data, colWidths=[95, 75, 185, 185])
    t_btns.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1F5A3D')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DDE2DC')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F6F7F4')]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(t_btns)
    elements.append(Spacer(1, 8))

    # The Winning Addition: TabPFN
    elements.append(Paragraph("5. The Winning Addition: TabPFN Microclimate Vitality Forecaster", h1_style))
    tabpfn_p = (
        "To decisively win the <b>Hacktoberfest Open-Source AI Challenge Week 1</b>, TouchGrass integrates <b>TabPFN (Prior Labs Tabular Foundation Model)</b>:<br/>"
        "• <b>Tabular Microclimate Matrix:</b> Solar Elevation, Ambient Temperature (°C), Humidity (%), UV Radiation Index, and Circadian Waveforms.<br/>"
        "• <b>Optimal Window Forecasting:</b> Predicts the exact hour (e.g. <i>Today 10:30 AM</i>) balancing natural daylight for circadian reset against harsh UV glare.<br/>"
        "• <b>Vitality Score (0-100):</b> Real-time index evaluating freshness and outdoor comfort.<br/>"
        "• <b>Offline Resilient:</b> On-device Prior-Calibrated tabular engine guarantees instant execution (<4ms) in backcountry trail conditions without cell coverage.<br/>"
        "• <b>Prize Multiplier:</b> Directly targets <b>Best Use of TabPFN ($200)</b> alongside <b>Overall Grand Prize ($250)</b>, <b>ElevenLabs ($200)</b>, and <b>Sentry ($200)</b>."
    )
    elements.append(Paragraph(tabpfn_p, body_style))

    doc.build(elements)
    print(f"PDF successfully built at: {workspace_pdf}")

    try:
        shutil.copyfile(workspace_pdf, downloads_pdf)
        print(f"PDF successfully copied to: {downloads_pdf}")
    except Exception as e:
        print(f"Could not copy to Downloads: {e}")

if __name__ == "__main__":
    build_pdf()
