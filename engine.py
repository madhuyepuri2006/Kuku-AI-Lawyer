"""Problem 2 AI Lawyer engine: router + deadline rules + document templates + citation guard (all plain code, no model)."""
import json, re, os, datetime as dt
KB = {e["id"]: e for e in json.load(open(os.path.join(os.path.dirname(__file__), "kb.json"), encoding="utf-8"))}

ROUTES = {
 "rti": ["rti","right to information","information from","सूचना का अधिकार","जानकारी माँगनी","தகவல் உரிமை","তথ্য অধিকার","pio","government office"],
 "upi_fraud": ["upi","paytm","phonepe","gpay","google pay","scam","fraud","otp","phishing","ठगी","धोखाधड़ी","पैसे कट","மோசடி","প্রতারণা","cyber","debited without"],
 "salary": ["salary","wages","unpaid","full and final","f&f","experience letter","relieving","pf ","provident","तनख्वाह","वेतन","சம்பளம்","বেতন","employer","company has not paid"],
}
def route(text):
    t = text.lower()
    s = {k: sum(w in t for w in v) for k, v in ROUTES.items()}
    best = max(s, key=s.get)
    return best if s[best] > 0 else "other"

def add_working_days(d, n):
    while n:
        d += dt.timedelta(days=1)
        if d.weekday() < 5: n -= 1
    return d

def deadlines(issue, facts):
    """facts: dict of ISO dates. Returns list of (label, date_str, kb_id). Holidays ignored."""
    D = lambda k: dt.date.fromisoformat(facts[k]) if facts.get(k) else None
    out = []
    if issue == "rti" and D("rti_filed"):
        reply = D("rti_filed") + dt.timedelta(days=30)
        out.append(("PIO reply due", reply.isoformat(), "RTI-7"))
        base = D("rti_reply") or reply
        out.append(("Last day for first appeal", (base + dt.timedelta(days=30)).isoformat(), "RTI-19"))
    if issue == "upi_fraud" and D("fraud_noticed"):
        out.append(("Report to bank by (3 working days)", add_working_days(D("fraud_noticed"), 3).isoformat(), "RBI-2017"))
        out.append(("Call 1930 / cybercrime.gov.in", "immediately", "UPI-1930"))
    if issue == "salary" and D("salary_due"):
        d = D("salary_due")
        try: lim = d.replace(year=d.year + 3)
        except ValueError: lim = d.replace(year=d.year + 3, day=28)
        out.append(("Civil-suit limitation (about)", lim.isoformat(), "SAL-LIMIT"))
    return out

def kb_for(issue):
    return [e for e in KB.values() if e["topic"] in (issue, "any")]

# ---- templates: filled by code; missing facts stay as [PLACEHOLDERS] so nothing is invented
def P(v, name): return v if v else f"[{name}]"
def draft(issue, f):
    if issue == "rti":
        return f"""To,\nThe Public Information Officer,\n{P(f.get('authority'),'DEPARTMENT / OFFICE')}\n\nSubject: Application under Section 6(1) of the Right to Information Act, 2005\n\nSir/Madam,\nI request the following information:\n{P(f.get('info_sought'),'LIST EACH QUESTION SEPARATELY')}\nPeriod: {P(f.get('period'),'FROM - TO')}\n\nI enclose the application fee of {P(f.get('fee'),'Rs 10 / BPL certificate')}. Please send the information to the address below.\n\n{P(f.get('name'),'YOUR NAME')}\n{P(f.get('address'),'ADDRESS, PHONE')}\nDate: {P(f.get('rti_filed'),'DATE')}"""
    if issue == "salary":
        return f"""To,\n{P(f.get('employer'),'EMPLOYER NAME AND ADDRESS')}\n\nSubject: Demand for unpaid dues\n\nI worked with you as {P(f.get('role'),'DESIGNATION')} from {P(f.get('joined'),'JOINING DATE')} to {P(f.get('left'),'LAST WORKING DATE')}. The following dues remain unpaid: {P(f.get('amount'),'AMOUNT AND MONTHS')} (due since {P(f.get('salary_due'),'DUE DATE')}).\n\nPlease pay within 15 days of this letter. Otherwise I will approach the Labour Department and take other legal steps.\n\nEnclosed: appointment letter, payslips, bank statements.\n\n{P(f.get('name'),'YOUR NAME')}, {P(f.get('address'),'ADDRESS, PHONE')}"""
    if issue == "upi_fraud":
        return f"""To,\nThe Branch Manager / Nodal Officer, {P(f.get('bank'),'BANK NAME')}\n\nSubject: Report of unauthorised transaction - request to block and reverse\n\nI report an unauthorised transaction of {P(f.get('amount'),'AMOUNT')} on {P(f.get('fraud_noticed'),'DATE/TIME')} from account ending {P(f.get('acct_last4'),'LAST 4 DIGITS')}. I did not authorise it or share my OTP/PIN with anyone [CONFIRM THIS IS TRUE]. Transaction/UTR reference: {P(f.get('utr'),'UTR')}.\n\nPlease block further debits, freeze the receiving account where possible, and give me a complaint number. I have also reported on 1930 / cybercrime.gov.in (ref: {P(f.get('cyber_ref'),'REF NO')}).\n\n{P(f.get('name'),'YOUR NAME')}, {P(f.get('phone'),'PHONE')}"""
    return "This tool does not draft documents for this kind of problem. Please see a lawyer or your District Legal Services Authority (NALSA 15100)."

# ---- citation guard
CITE = re.compile(r"\[([A-Z0-9\-]+)\]")
SECT = re.compile(r"\b(?:section|sec\.?|s\.|article)\s*(\d+[A-Za-z]?(?:\(\d+\))?)", re.I)
CASE = re.compile(r"\b(?:AIR\s*\d{4}|\d{4}\s*SCC|v\.|vs\.?)\s", re.I)
PROMISE = re.compile(r"\b(guarantee[sd]?|definitely win|100%|certain(ly)? (to )?win|you will win)\b", re.I)
def guard(text, allowed_ids):
    v = []
    cited = set(CITE.findall(text))
    for c in cited:
        if c not in KB: v.append(f"unknown citation [{c}]")
        elif c not in allowed_ids: v.append(f"citation [{c}] not allowed for this issue")
    corpus = " ".join(KB[c]["text"] for c in cited if c in KB)
    for m in SECT.finditer(text):
        num = m.group(1)
        if not re.search(r"(?<![\w])" + re.escape(num.split("(")[0]) + r"(?![\w])", corpus):
            v.append(f"section/article '{m.group(0)}' not supported by cited notes")
    if CASE.search(text): v.append("possible case-law citation (not allowed)")
    if PROMISE.search(text): v.append("outcome promise")
    return v

# ---- model adapter (swappable)
def llm(system, user):
    p = os.getenv("LLM_PROVIDER", "anthropic"); m = os.getenv("LLM_MODEL", "claude-sonnet-4-6" if p == "anthropic" else "gpt-4o-mini")
    if p == "anthropic":
        import anthropic
        return anthropic.Anthropic().messages.create(model=m, max_tokens=900, system=system, messages=[{"role": "user", "content": user}]).content[0].text
    from openai import OpenAI
    r = OpenAI(base_url=os.getenv("LLM_BASE_URL") or None).chat.completions.create(model=m, messages=[{"role": "system", "content": system}, {"role": "user", "content": user}])
    return r.choices[0].message.content

EXPLAIN_SYS = """You explain legal options to an ordinary person in India in THEIR language, in plain words, max 180 words.
Use ONLY the NOTES. Cite note ids like [RTI-7]. Never mention a section, case or amount that is not in the notes. If unsure, say you cannot verify.
Structure: 1) what this means for you 2) your next 3 steps 3) when you need a real lawyer. Never promise results.
NOTES:\n"""
def explain(issue, story, retries=1):
    notes = kb_for(issue); allowed = {e["id"] for e in notes}
    sysmsg = EXPLAIN_SYS + "\n".join(f"[{e['id']}] {e['text']}" for e in notes)
    out = llm(sysmsg, story); viol = guard(out, allowed)
    while viol and retries:
        retries -= 1
        out = llm(sysmsg, story + "\n\nYour last answer broke these rules: " + "; ".join(viol) + ". Rewrite fixing them."); viol = guard(out, allowed)
    return out, viol
