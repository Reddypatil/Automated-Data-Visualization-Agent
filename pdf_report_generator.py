import pandas as pd
import streamlit as st
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io
from datetime import datetime

def create_pdf_report(df: pd.DataFrame, analysis_summary: dict) -> bytes:
    """Generate comprehensive PDF report"""
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#764ba2'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    story = []
    
    # Title
    story.append(Paragraph("📊 DataWizard Analysis Report", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Report metadata
    metadata_style = ParagraphStyle('Metadata', parent=styles['Normal'], fontSize=10, textColor=colors.grey)
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", metadata_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Executive Summary
    story.append(Paragraph("Executive Summary", heading_style))
    summary_text = f"This report presents an analysis of {len(df)} records with {len(df.columns)} variables."
    story.append(Paragraph(summary_text, styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Dataset Overview
    story.append(Paragraph("Dataset Overview", heading_style))
    
    overview_data = [
        ['Metric', 'Value'],
        ['Total Rows', str(len(df))],
        ['Total Columns', str(len(df.columns))],
        ['Numeric Columns', str(len(df.select_dtypes(include=['number']).columns))],
        ['Categorical Columns', str(len(df.select_dtypes(include=['object']).columns))],
        ['Memory Usage (MB)', f"{df.memory_usage(deep=True).sum() / 1024**2:.2f}"],
        ['Duplicate Rows', str(df.duplicated().sum())],
        ['Missing Values', str(df.isnull().sum().sum())],
    ]
    
    overview_table = Table(overview_data, colWidths=[3*inch, 2*inch])
    overview_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    story.append(overview_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Column Information
    story.append(Paragraph("Column Information", heading_style))
    
    col_data = [['Column', 'Type', 'Non-Null', 'Unique']]
    for col in df.columns[:10]:  # Limit to first 10 columns
        col_data.append([
            col[:20],
            str(df[col].dtype),
            str(df[col].count()),
            str(df[col].nunique())
        ])
    
    col_table = Table(col_data, colWidths=[1.5*inch, 1.2*inch, 1.2*inch, 1.2*inch])
    col_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#764ba2')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    
    story.append(col_table)
    story.append(PageBreak())
    
    # Statistics Summary
    story.append(Paragraph("Statistical Summary", heading_style))
    
    numeric_stats = df.describe().round(2)
    stats_data = [[''] + list(df.columns[:5])]  # Limit columns
    
    for idx, row in numeric_stats.iterrows():
        stats_data.append([str(idx)] + [f"{val:.2f}" if pd.notna(val) else 'N/A' 
                                       for val in row[:5]])
    
    stats_table = Table(stats_data, colWidths=[1*inch, 1*inch, 1*inch, 1*inch, 1*inch, 1*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
    ]))
    
    story.append(stats_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Analysis Notes
    story.append(Paragraph("Analysis Notes", heading_style))
    notes = "This report provides comprehensive overview of the dataset including data quality metrics, statistical summaries, and column information. Further analysis can be performed using the DataWizard platform."
    story.append(Paragraph(notes, styles['Normal']))
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

def pdf_report_ui(df: pd.DataFrame):
    """Main PDF report UI"""
    st.markdown("## 📄 PDF Report Generation")
    
    if st.button("🔧 Generate PDF Report"):
        try:
            with st.spinner("Generating PDF..."):
                analysis_summary = {
                    'rows': len(df),
                    'cols': len(df.columns),
                    'numeric': len(df.select_dtypes(include=['number']).columns),
                }
                
                pdf_bytes = create_pdf_report(df, analysis_summary)
                
                st.download_button(
                    label="📥 Download PDF Report",
                    data=pdf_bytes,
                    file_name=f"DataWizard_Report_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf"
                )
                st.success("✅ PDF generated successfully")
        except Exception as e:
            st.error(f"Error generating PDF: {str(e)}")
