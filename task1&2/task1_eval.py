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


print(f"{'Tool':<15} | {'File':<15} | {'WER Score':<10} | {'Time (s)':<10}")
print("-" * 60)
for r in results:
    print(f"{r['Tool']:<15} | {r['File']:<15} | {r['WER']:.4f}     | {r['Time']:.4f}")

# CALCULATE AVERAGES AND DETERMINE WINNER
print("\n" + "=" * 60)
print("SUMMARY STATISTICS")
print("=" * 60)

tools = ["PyMuPDF", "pdfplumber", "pypdf"]
summary = {}

for tool in tools:
    tool_results = [r for r in results if r['Tool'] == tool]
    avg_wer = sum(r['WER'] for r in tool_results) / len(tool_results)
    avg_time = sum(r['Time'] for r in tool_results) / len(tool_results)
    summary[tool] = {"avg_wer": avg_wer, "avg_time": avg_time}
    print(f"{tool:<15} | Avg WER: {avg_wer:.4f} | Avg Time: {avg_time:.4f}s")

# Determine winner based on balanced score (accuracy * speed)
print("\n" + "=" * 60)
print("OVERALL WINNER")
print("=" * 60)

best_accuracy = min(summary.items(), key=lambda x: x[1]["avg_wer"])
best_speed = min(summary.items(), key=lambda x: x[1]["avg_time"])
best_balanced = min(summary.items(), key=lambda x: x[1]["avg_wer"] + (x[1]["avg_time"] / 10))

print(f"Best Accuracy:  {best_accuracy[0]} (WER: {best_accuracy[1]['avg_wer']:.4f})")
print(f"Best Speed:     {best_speed[0]} (Time: {best_speed[1]['avg_time']:.4f}s)")
print(f"Best Overall:   {best_balanced[0]} (Balanced Score: {best_balanced[1]['avg_wer'] + (best_balanced[1]['avg_time'] / 10):.4f})")