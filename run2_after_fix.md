# Raw output: run2_after_fix (2026-11-08 13:54)


## Router
- **R1** PASS: input='Mere office ne 3 mahine se salary nahi di aur experience letter bhi rok liya' -> salary (expected salary)
- **R2** PASS: input='मुझे सरकारी दफ्तर से सूचना का अधिकार के तहत जानकारी माँगनी है' -> rti (expected rti)
- **R3** PASS: input='Someone called, took my OTP and 12,000 was debited from my UPI account' -> upi_fraud (expected upi_fraud)
- **R4** PASS: input='என் சம்பளம் இரண்டு மாதமாக வரவில்லை' -> salary (expected salary)
- **R5** PASS: input='মোবাইলে প্রতারণা করে আমার টাকা কেটে নিয়েছে' -> upi_fraud (expected upi_fraud)
- **R6** PASS: input='My neighbour is playing loud music every night' -> other (expected other)

## Deadline rules
- **D1** PASS: {'rti_filed': '2026-09-01'} -> {'PIO reply due': '2026-10-01', 'Last day for first appeal': '2026-10-31'} (expected {'PIO reply due': '2026-10-01', 'Last day for first appeal': '2026-10-31'})
- **D2** PASS: {'fraud_noticed': '2026-11-05'} -> {'Report to bank by (3 working days)': '2026-11-10', 'Call 1930 / cybercrime.gov.in': 'immediately'} (expected {'Report to bank by (3 working days)': '2026-11-10'})
- **D3** PASS: {'salary_due': '2026-03-31'} -> {'Civil-suit limitation (about)': '2029-03-31'} (expected {'Civil-suit limitation (about)': '2029-03-31'})
- **D4** PASS: {'salary_due': '2024-02-29'} -> {'Civil-suit limitation (about)': '2027-02-28'} (expected {'Civil-suit limitation (about)': '2027-02-28'})

## Citation guard (planted bad answers must be caught, clean ones must pass)
- **G1** PASS: text='The PIO must reply in 30 days [RTI-7]. If not, file a first appeal within 30 days [RTI-19].' -> violations=[]
- **G2** PASS: text='Under Section 420A of the RTI Act the PIO can be fined Rs 1 lakh.' -> violations=["section/article 'Section 420A' not supported by cited notes"]
- **G3** PASS: text='As held in Sharma v. State Bank, you will get a full refund [RBI-2017].' -> violations=['possible case-law citation (not allowed)']
- **G4** PASS: text='Per [XYZ-99] your employer must pay interest.' -> violations=['unknown citation [XYZ-99]']
- **G5** PASS: text='I guarantee you will win this case [SAL-FORUM].' -> violations=['outcome promise']
- **G6** PASS: text='File a complaint with the Labour Commissioner [SAL-FORUM]. Use RTI notes [RTI-7].' -> violations=['citation [RTI-7] not allowed for this issue']
- **G7** PASS: text='Section 7(1) says the PIO must reply within 30 days [RTI-7].' -> violations=[]
- **G8** PASS: text='Section 8 exempts all information about government salaries [RTI-6].' -> violations=["section/article 'Section 8' not supported by cited notes"]

**Offline checks passed: 18/18**