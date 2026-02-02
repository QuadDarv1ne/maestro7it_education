from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import Color
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
import json
from datetime import datetime

def generate_pdf_report(user, test_result, results):
    """Generate PDF report for test results"""
    
    # Create buffer
    buffer = io.BytesIO()
    
    # Create document
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=20,
        textColor=Color(0.2, 0.4, 0.8)
    )
    
    normal_style = styles['Normal']
    normal_style.fontSize = 12
    normal_style.spaceAfter = 12
    
    # Title
    title = "Профессиональная ориентация"
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 20))
    
    # User info
    user_info = f"""
    <b>Пользователь:</b> {user.username}<br/>
    <b>Email:</b> {user.email}<br/>
    <b>Дата тестирования:</b> {test_result.created_at.strftime('%d.%m.%Y %H:%M')}<br/>
    """
    
    if test_result.methodology == 'klimov':
        user_info += "<b>Методика:</b> Дифференциально-диагностический опросник Климова<br/>"
        user_info += f"<b>Всего вопросов:</b> {results['total_questions']}<br/>"
    else:
        user_info += "<b>Методика:</b> Опросник профессиональных предпочтений Холланда<br/>"
        user_info += f"<b>Всего вопросов:</b> {results['total_questions']}<br/>"
    
    story.append(Paragraph(user_info, normal_style))
    story.append(Spacer(1, 20))
    
    # Main results
    if test_result.methodology == 'klimov':
        story.append(Paragraph("Ваша профессиональная стихия:", subtitle_style))
        dominant_category = results['dominant_category']
        percentage = (results['max_score'] / (results['total_questions'] * 3)) * 100
        
        main_result = f"""
        <b><font color="green" size="18">{dominant_category}</font></b><br/>
        <b>Уровень соответствия:</b> {percentage:.1f}%<br/>
        """
        story.append(Paragraph(main_result, normal_style))
        
    else:
        story.append(Paragraph("Ваши профессиональные типы:", subtitle_style))
        for category, score in results['top_categories']:
            percentage = (score / (results['total_questions'] * 3)) * 100
            result_text = f"""
            <b><font color="blue">{category}</font></b> - {percentage:.1f}%<br/>
            """
            story.append(Paragraph(result_text, normal_style))
    
    story.append(Spacer(1, 20))
    
    # Detailed scores table
    story.append(Paragraph("Подробные результаты:", subtitle_style))
    
    # Prepare table data
    table_data = [['Категория', 'Баллы', 'Процент', 'Интерпретация']]
    
    for category, score in results['scores'].items():
        percentage = (score / (results['total_questions'] * 3)) * 100
        
        if test_result.methodology == 'klimov':
            if category == results['dominant_category']:
                interpretation = "Высокая склонность"
            elif score >= (results['total_questions'] * 3 * 0.6):
                interpretation = "Средняя склонность"
            else:
                interpretation = "Низкая склонность"
        else:
            if category in [cat for cat, _ in results['top_categories']]:
                interpretation = "Основной тип"
            elif score >= (results['total_questions'] * 3 * 0.5):
                interpretation = "Умеренная склонность"
            else:
                interpretation = "Низкая склонность"
        
        table_data.append([category, str(score), f"{percentage:.1f}%", interpretation])
    
    # Create table
    table = Table(table_data, colWidths=[4*cm, 2*cm, 2.5*cm, 4*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), Color(0.2, 0.4, 0.8)),
        ('TEXTCOLOR', (0, 0), (-1, 0), Color(1, 1, 1)),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), Color(0.95, 0.95, 0.95)),
        ('GRID', (0, 0), (-1, -1), 1, Color(0.8, 0.8, 0.8)),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))
    
    story.append(table)
    story.append(Spacer(1, 20))
    
    # Recommendations
    story.append(Paragraph("Рекомендации:", subtitle_style))
    recommendation_html = test_result.recommendation.replace('<h3>', '<b>').replace('</h3>', '</b><br/>')
    recommendation_html = recommendation_html.replace('<p>', '').replace('</p>', '<br/>')
    recommendation_html = recommendation_html.replace('<strong>', '<b>').replace('</strong>', '</b>')
    story.append(Paragraph(recommendation_html, normal_style))
    
    # Footer
    story.append(Spacer(1, 30))
    footer = f"""
    <i>Отчет сгенерирован автоматически {datetime.now().strftime('%d.%m.%Y %H:%M')}</i><br/>
    <i>Система профессиональной ориентации "МойПрофСтарт"</i>
    """
    story.append(Paragraph(footer, styles['Italic']))
    
    # Build PDF
    doc.build(story)
    
    # Get PDF data
    pdf_data = buffer.getvalue()
    buffer.close()
    
    return pdf_data