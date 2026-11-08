from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.colors import HexColor

out='Solution_Doc_Problem2.pdf'
doc=SimpleDocTemplate(out,pagesize=A4,rightMargin=16*mm,leftMargin=16*mm,topMargin=13*mm,bottomMargin=13*mm,title='Kuku AI Generalist Assignment - Problem 2: Build an AI Lawyer')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='MainTitle', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=20, leading=23, alignment=TA_CENTER, textColor=HexColor('#17365D'), spaceAfter=3))
styles.add(ParagraphStyle(name='Sub', parent=styles['Normal'], fontSize=8.5, leading=11, alignment=TA_CENTER, textColor=colors.HexColor('#555555'), spaceAfter=8))
styles.add(ParagraphStyle(name='H', parent=styles['Heading2'], fontSize=11, leading=13, textColor=HexColor('#17365D'), spaceBefore=5, spaceAfter=3))
styles.add(ParagraphStyle(name='Body2', parent=styles['BodyText'], fontSize=8.3, leading=10.7, spaceAfter=3))
styles.add(ParagraphStyle(name='Small', parent=styles['BodyText'], fontSize=7.5, leading=9.2, spaceAfter=2))
styles.add(ParagraphStyle(name='Tiny', parent=styles['BodyText'], fontSize=6.8, leading=8.1))
P=lambda s,st='Body2': Paragraph(s,styles[st])
story=[]
story += [P('AI Lawyer Prototype','MainTitle'), P('Selected assignment: Problem 2 — Build an AI Lawyer','Sub'), P('<b>Name:</b> Yepuri Madhu &nbsp;&nbsp; <b>Roll no:</b> 23145099 &nbsp;&nbsp; <b>Branch:</b> Metallurgy, IIT BHU','Small')]
story += [P('1. Problem and scope','H')]
story += [P('People often struggle to take the first step on everyday legal problems because the process, deadlines and paperwork are confusing. I scoped this prototype to three narrow workflows: (1) RTI application / delayed response, (2) UPI or online payment fraud, and (3) unpaid salary or full-and-final dues. Other matters are explicitly out of scope and receive a safe referral message.','Body2')]
story += [P('2. What I built','H')]
data=[
 [P('<b>Step</b>','Small'),P('<b>Implementation</b>','Small'),P('<b>Reason</b>','Small')],
 [P('Issue routing','Small'),P('Python keyword rules with English, Hindi, Tamil and Bengali terms; unknown issue routes to “not covered”.','Small'),P('Predictable and inexpensive; avoids pretending to cover all law.','Small')],
 [P('Date calculations','Small'),P('Code calculates indicative RTI response / appeal dates, an indicative UPI reporting window and an approximate salary-claim limitation date.','Small'),P('Date arithmetic is deterministic; holidays and legal exceptions remain limitations.','Small')],
 [P('Document drafts','Small'),P('Issue-specific templates fill user-provided facts; missing information remains visible as [PLACEHOLDERS].','Small'),P('Avoids inventing facts and produces an editable starting point.','Small')],
 [P('Plain-language explanation','Small'),P('Optional swappable LLM adapter; model receives only the issue notes and user story.','Small'),P('Uses the model for language and explanation, not date arithmetic.','Small')],
 [P('Citation guard','Small'),P('Python checks configured note IDs, unsupported section patterns, possible case citations and outcome promises; retries once.','Small'),P('A limited safety layer that flags selected risks; it cannot prove legal correctness.','Small')],
]
t=Table(data,colWidths=[27*mm,91*mm,60*mm],repeatRows=1)
t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#DCE6F1')),('GRID',(0,0),(-1,-1),0.35,HexColor('#AAB7C4')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
story += [t, P('3. Assumptions and user experience','H'), P('The prototype is text-based; voice input is not implemented. The user supplies a short narrative and optional dates / details. The interface warns users not to enter Aadhaar, full bank or card numbers, passwords or OTPs. The generated drafts must be reviewed and completed before sending.','Body2')]
story += [PageBreak(), P('Problem 2: Build an AI Lawyer — Evaluation and limitations','MainTitle')]
story += [P('4. Testing and observed results','H'), P('The supplied offline suite contains 18 checks: 6 routing examples, 4 date-arithmetic examples (including a leap-day case), and 8 citation-guard examples. The final run passed <b>18/18</b>. The first recorded run passed 17/18; a section-number matching issue was corrected and the suite was rerun. The raw outputs are included in raw_outputs/.','Body2')]
story += [P('What the tests establish: the programmed examples behave as expected. What they do not establish: that the legal notes are current, that a generated explanation is legally correct, or that a user will obtain a particular outcome.','Body2')]
story += [P('Model evaluation status: not completed in this package. The optional six-story model run requires an API key and manual scoring for language match, supported citations, no invented law, useful next steps, lawyer escalation and no outcome promises. No model-quality score is claimed.','Body2')]
story += [P('5. Safety, limitations and honest failure modes','H'), P('All nine entries in kb.json are currently marked <b>unverified</b>. Their source URLs are recorded, but they have not been independently checked for current applicability. The prototype must not be used as legal advice. In particular, state-specific labour rules, current RBI/bank procedures, fees, limitation exceptions and holidays require official verification. The UPI date is an indicative reminder, not a guarantee of zero liability.','Body2')]
story += [P('Keyword routing can miss paraphrases or misclassify ambiguous stories. The citation guard catches only selected patterns; it cannot detect every incorrect statement in prose. Date calculations depend on user-supplied dates and simplified assumptions. A qualified lawyer or legal-aid service should review case-specific decisions and documents.','Body2')]
story += [P('6. Scaling and next steps','H'), P('For real use, maintain a source register with official URL, jurisdiction, last-verified date and reviewer; add state-specific rules; re-verify notes on a schedule; expand tests with real anonymised scenarios; evaluate each model on a human-scored test set; add document upload and voice input only after privacy and consent controls; and keep a human legal professional in the loop. Model provider and model can be changed through environment variables.','Body2')]
story += [P('7. Tools used and where AI got it wrong','H'), P('Python and Gradio implement the prototype; an optional Anthropic / OpenAI-compatible API provides explanations. AI assistance was used for drafting and iteration. During testing, the first citation-guard implementation incorrectly rejected a valid Section 7(1) reference because of punctuation handling; test G7 exposed it and the matching rule was fixed. The model can also confidently state legal details from memory, so the design restricts it to supplied notes and keeps those notes visibly unverified.','Body2')]
story += [Spacer(1,4), P('<b>Important notice:</b> AI Lawyer Prototype is an educational prototype, not a lawyer, legal opinion or emergency service. Verify all legal information with current official sources and a qualified professional before acting.','Small')]

def footer(canvas, doc):
    canvas.saveState(); canvas.setFont('Helvetica',7); canvas.setFillColor(HexColor('#666666'))
    canvas.drawString(16*mm,8*mm,'Kuku AI Generalist Assignment | Problem 2')
    canvas.drawRightString(A4[0]-16*mm,8*mm,f'Page {doc.page}')
    canvas.restoreState()

doc.build(story,onFirstPage=footer,onLaterPages=footer)
