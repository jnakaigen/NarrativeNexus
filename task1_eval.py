import fitz  # PyMuPDF
import pdfplumber
import pypdf
import jiwer
import time

# FILES TO TEST (Replace with your actual filenames)
test_files = [
    {"pdf": "sample1.pdf", "truth": "truth_1.txt"},
    {"pdf": "sample2.pdf", "truth": "truth_2.txt"},
    {"pdf": "sample3.pdf", "truth": "truth_3.txt"},
]

results = []

for item in test_files:
    # Load Ground Truth
    with open(item["truth"], "r", encoding="utf-8") as f:
        reference_text = f.read().strip()

    # --- TEST 1: PyMuPDF ---
    start = time.time()
    doc = fitz.open(item["pdf"])
    hyp_text = ""
    # Only grabbing page 1 to match your quick ground truth
    hyp_text = doc[0].get_text().strip() 
    wer = jiwer.wer(reference_text, hyp_text)
    results.append({"Tool": "PyMuPDF", "File": item["pdf"], "WER": wer, "Time": time.time() - start})

    # --- TEST 2: pdfplumber ---
    start = time.time()
    with pdfplumber.open(item["pdf"]) as pdf:
        hyp_text = pdf.pages[0].extract_text().strip()
    wer = jiwer.wer(reference_text, hyp_text)
    results.append({"Tool": "pdfplumber", "File": item["pdf"], "WER": wer, "Time": time.time() - start})

    # --- TEST 3: pypdf ---
    start = time.time()
    reader = pypdf.PdfReader(item["pdf"])
    hyp_text = reader.pages[0].extract_text().strip()
    wer = jiwer.wer(reference_text, hyp_text)
    results.append({"Tool": "pypdf", "File": item["pdf"], "WER": wer, "Time": time.time() - start})

# PRINT REPORT FOR SUBMISSION
print(f"{'Tool':<15} | {'File':<15} | {'WER Score':<10} | {'Time (s)':<10}")
print("-" * 60)
for r in results:
    print(f"{r['Tool']:<15} | {r['File']:<15} | {r['WER']:.4f}     | {r['Time']:.4f}")