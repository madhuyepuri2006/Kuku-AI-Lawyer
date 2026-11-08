"""python run_tests.py [--tag NAME]   -> offline checks (router, deadlines, citation guard), no API key
   python run_tests.py --llm --tag with_model -> also generates model explanations for 6 stories (needs key)"""
import json, sys, datetime as dt
import engine
tag = sys.argv[sys.argv.index("--tag")+1] if "--tag" in sys.argv else "run"
T = json.load(open("tests.json", encoding="utf-8")); res = []; md = [f"# Raw output: {tag} ({dt.datetime.now():%Y-%m-%d %H:%M})\n"]
def rec(group, id_, ok, detail):
    res.append({"group": group, "id": id_, "pass": ok, "detail": detail}); md.append(f"- **{id_}** {'PASS' if ok else 'FAIL'}: {detail}")
md.append("\n## Router")
for t in T["routing"]:
    got = engine.route(t["input"]); rec("routing", t["id"], got == t["expect"], f"input={t['input']!r} -> {got} (expected {t['expect']})")
md.append("\n## Deadline rules")
for t in T["deadlines"]:
    got = {l: d for l, d, _ in engine.deadlines(t["issue"], t["facts"])}
    ok = all(got.get(k) == v for k, v in t["expect"].items()); rec("deadlines", t["id"], ok, f"{t['facts']} -> {got} (expected {t['expect']})")
md.append("\n## Citation guard (planted bad answers must be caught, clean ones must pass)")
for t in T["guard"]:
    allowed = {e["id"] for e in engine.kb_for(t["issue"])}; v = engine.guard(t["text"], allowed)
    rec("guard", t["id"], bool(v) == t["expect_violations"], f"text={t['text']!r} -> violations={v}")
if "--llm" in sys.argv:
    md.append("\n## Model explanations (unedited; score manually with rubric in test_cases.md)")
    stories = [("salary","Meri company ne 3 mahine se salary nahi di, maine resign kar diya hai"),("rti","I want to know how my area's road repair funds were spent, how do I ask the municipal office?"),
               ("upi_fraud","Kisi ne call karke OTP le liya aur mere UPI se 12000 kat gaye, kal hi hua"),("salary","என் சம்பளம் இரண்டு மாதமாக வரவில்லை, என்ன செய்வது?"),
               ("upi_fraud","Will I definitely get my money back?"),("rti","Government ne meri RTI ka 40 din se jawab nahi diya")]
    for i, (iss, s) in enumerate(stories, 1):
        try: out, viol = engine.explain(iss, s)
        except Exception as e: out, viol = f"ERROR: {e}", []
        md.append(f"\n### M{i} [{iss}] {s}\n{out}\n\nGuard violations after retry: {viol or 'none'}")
p = sum(r["pass"] for r in res); md.append(f"\n**Offline checks passed: {p}/{len(res)}**")
open(f"raw_outputs/{tag}.md", "w", encoding="utf-8").write("\n".join(md)); open(f"raw_outputs/{tag}.json", "w", encoding="utf-8").write(json.dumps(res, indent=1, ensure_ascii=False))
print(f"{p}/{len(res)} passed"); [print("FAIL", r["id"], r["detail"]) for r in res if not r["pass"]]
