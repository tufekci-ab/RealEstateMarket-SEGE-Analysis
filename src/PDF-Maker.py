# pdf_report_generator.py
import pandas as pd
from fpdf import FPDF
import os

# Create PDF object
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# Ana Başlık
pdf.set_font("Arial", style="B", size=16)
pdf.cell(0, 10, "Exploratory Data Analysis Report", ln=True, align='C')
pdf.ln(10)

# Summary Statistics
summary_stats = pd.read_csv("eda_outputs/summary.csv", index_col=0)

pdf.set_font("Arial", size=12)
pdf.cell(0, 10, "Summary Statistics:", ln=True)
pdf.set_font("Arial", size=10)
pdf.cell(0, 10, "Note: K = Thousand, M = Million", ln=True)
pdf.set_font("Courier", size=7)

col_width = pdf.w / (len(summary_stats.columns) + 1) - 2
pdf.set_fill_color(220, 220, 220)
pdf.set_font("Courier", 'B', 7)
pdf.cell(col_width, 8, "Variable", border=1, fill=True)
for col in summary_stats.columns:
    pdf.cell(col_width, 8, col[:10], border=1, fill=True)
pdf.ln()

pdf.set_font("Courier", size=7)
for idx, row in summary_stats.iterrows():
    pdf.cell(col_width, 8, str(idx)[:12], border=1)
    for val in row:
        pdf.cell(col_width, 8, str(val), border=1)
    pdf.ln()

# Function to add grouped plots
def add_grouped_plots(title, plot_type):
    plot_dir = "eda_outputs/plots"
    plots = [f for f in os.listdir(plot_dir) if f.startswith(plot_type)]
    plots.sort()

    cols = 2
    rows = 3
    cell_w = 95
    cell_h = 80
    margin_x = 10
    margin_y = 20

    for i, plot_file in enumerate(plots):
        if i % (cols * rows) == 0:
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.set_xy(10, 10)
            pdf.cell(0, 10, title, ln=True)

        row = (i % (cols * rows)) // cols
        col = i % cols
        x = margin_x + col * cell_w
        y = margin_y + row * cell_h
        pdf.set_xy(x, y)
        pdf.set_font("Arial", size=8)
        pdf.cell(cell_w, 5, plot_file.replace(".png", ""), ln=True, align='C')
        pdf.image(f"{plot_dir}/{plot_file}", x=x, y=y+5, w=cell_w-5, h=cell_h-15)

# Add Histograms, QQ plots, Boxplots
add_grouped_plots("Histograms:", "hist_")
add_grouped_plots("Q-Q Plots:", "qq_")
add_grouped_plots("Boxplots:", "box_")

# Add Correlation Matrix
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(0, 10, "Correlation Matrix:", ln=True)
pdf.image("eda_outputs/plots/correlation_matrix.png", w=180)

# Add Normality Test Table
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(0, 10, "Normality Test Summary Table:", ln=True)
pdf.set_font("Courier", size=9)
with open("eda_outputs/normality_results.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.encode("latin-1", errors="ignore").decode("latin-1")
        pdf.multi_cell(0, 5, line)

# Add Q-Q R2 Scores
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(0, 10, "Q-Q Plot R² Scores (Descending):", ln=True)
pdf.set_font("Courier", size=10)
with open("eda_outputs/qq_r2_scores.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.encode("latin-1", errors="ignore").decode("latin-1")
        pdf.multi_cell(0, 5, line)

# Save PDF
pdf.output("EDA_Report.pdf")
print("EDA_Report.pdf successfully created!")
