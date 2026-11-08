"""Kuku AI Generalist Assignment — Problem 2: Build an AI Lawyer (Gradio prototype). Text-only prototype; not legal advice."""
import gradio as gr
import engine

LABEL = {"rti": "RTI application", "upi_fraud": "UPI / online fraud", "salary": "Unpaid salary / dues", "other": "Not covered"}
DATEKEY = {"rti": "rti_filed", "upi_fraud": "fraud_noticed", "salary": "salary_due"}

def run(story, key_date, who, name, amount, info_sought, period, fee, address,
        role, joined, left, phone, acct_last4, utr, cyber_ref, rti_reply):
    story = (story or "").strip()
    if not story:
        return "Need details", "Please describe what happened first.", "", "", "No legal analysis performed."
    issue = engine.route(story)
    if issue == "other":
        return LABEL[issue], "", "This prototype covers only RTI, UPI/online fraud and unpaid salary. For other issues, contact a qualified lawyer or District Legal Services Authority. NALSA helpline listed in the prototype notes: 15100.", "", "Out of scope; no legal conclusion generated."

    facts = {
        DATEKEY[issue]: (key_date or "").strip() or None,
        "authority": (who or "").strip() or None,
        "bank": (who or "").strip() or None,
        "employer": (who or "").strip() or None,
        "name": (name or "").strip() or None,
        "amount": (amount or "").strip() or None,
        "info_sought": (info_sought or "").strip() or None,
        "period": (period or "").strip() or None,
        "fee": (fee or "").strip() or None,
        "address": (address or "").strip() or None,
        "role": (role or "").strip() or None,
        "joined": (joined or "").strip() or None,
        "left": (left or "").strip() or None,
        "phone": (phone or "").strip() or None,
        "acct_last4": (acct_last4 or "").strip() or None,
        "utr": (utr or "").strip() or None,
        "cyber_ref": (cyber_ref or "").strip() or None,
        "rti_reply": (rti_reply or "").strip() or None,
    }
    try:
        dl = engine.deadlines(issue, facts)
        table = "\n".join(f"- **{label}**: {date} `[{kid}]`" for label, date, kid in dl)
        if not table:
            table = "Enter a valid key date (YYYY-MM-DD) to calculate an indicative date."
    except (ValueError, TypeError):
        table = "Invalid date. Use YYYY-MM-DD. No date calculation was made."

    try:
        explanation, violations = engine.explain(issue, story)
        guard_report = ("Citation guard passed its configured checks; this does NOT prove the legal explanation is correct."
                        if not violations else "WARNING — guard flagged: " + "; ".join(violations))
    except Exception as exc:
        explanation = "Model explanation unavailable. The draft and rule-based date output may still be available."
        guard_report = f"Model/guard not run ({type(exc).__name__}). Do not treat this as legal advice."

    draft = engine.draft(issue, facts)
    return LABEL[issue], table, explanation, draft, guard_report

with gr.Blocks(title="AI Lawyer Prototype") as ui:
    gr.Markdown("""# AI Lawyer Prototype
A small text-based prototype for **RTI applications, UPI/online fraud and unpaid salary/dues**.

**Important:** This is an educational prototype, not a lawyer or a source of legal advice. Its legal notes are unverified and must be checked against current official sources and the relevant state/bank rules before use. Do not enter Aadhaar, full bank/card numbers, passwords or OTPs. For active digital-payment fraud, contact your bank immediately and report through India's official cybercrime channels; do not wait for this tool.""")
    story = gr.Textbox(label="What happened? (describe in your own words)", lines=4, placeholder="Example: My employer has not paid my salary for two months...")
    with gr.Row():
        key_date = gr.Textbox(label="Key date (YYYY-MM-DD): RTI filed / fraud noticed / salary due")
        who = gr.Textbox(label="Relevant office / bank / employer")
    with gr.Row():
        name = gr.Textbox(label="Your name (optional)")
        amount = gr.Textbox(label="Amount (optional)")
    gr.Markdown("### Extra details for the draft (fill only the fields relevant to your issue)")
    with gr.Row():
        info_sought = gr.Textbox(label="RTI: exact information/questions sought")
        period = gr.Textbox(label="RTI: period (from–to)")
    with gr.Row():
        fee = gr.Textbox(label="RTI: fee/BPL details")
        rti_reply = gr.Textbox(label="RTI: date reply received (if any, YYYY-MM-DD)")
    with gr.Row():
        role = gr.Textbox(label="Salary: role/designation")
        joined = gr.Textbox(label="Salary: joining date")
        left = gr.Textbox(label="Salary: last working date")
    with gr.Row():
        address = gr.Textbox(label="Postal address (optional)")
        phone = gr.Textbox(label="Phone (optional)")
    with gr.Row():
        acct_last4 = gr.Textbox(label="UPI: last 4 digits only (optional)")
        utr = gr.Textbox(label="UPI: transaction/UTR reference (optional)")
        cyber_ref = gr.Textbox(label="UPI: cybercrime complaint reference (optional)")
    go = gr.Button("Generate guidance and draft", variant="primary")
    o1 = gr.Textbox(label="Detected issue")
    o2 = gr.Markdown(label="Indicative dates (check official rules)")
    o3 = gr.Textbox(label="Plain-language explanation (model; guarded, not verified)", lines=8)
    o4 = gr.Textbox(label="Draft document (review and complete placeholders before use)", lines=14)
    o5 = gr.Textbox(label="Guard / system status")
    inputs = [story, key_date, who, name, amount, info_sought, period, fee, address, role, joined, left, phone, acct_last4, utr, cyber_ref, rti_reply]
    go.click(run, inputs, [o1, o2, o3, o4, o5])

if __name__ == "__main__":
    ui.launch()
