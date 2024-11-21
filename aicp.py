import sys
import math
import re
import urllib.request
from bs4 import BeautifulSoup as bs
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext
import PyPDF2
import nltk
import spacy
from transformers import pipeline
from rouge_score import rouge_scorer

nltk.download('wordnet')

# Initialize variables
nlp = spacy.load('en_core_web_sm')

# Initialize the BART summarization model from Hugging Face's Transformers library
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Function to read text file
def file_text(filepath):
    with open(filepath) as f:
        text = f.read().replace("\n", '')
        return text

# Function to read PDF file
def pdfReader(pdf_path):
    with open(pdf_path, 'rb') as pdfFileObject:
        pdfReader = PyPDF2.PdfReader(pdfFileObject)
        count = len(pdfReader.pages)

        text = ""
        for i in range(count):
            page = pdfReader.pages[i]
            text += page.extract_text()

        return text

# Function to read Wikipedia page
def wiki_text(url):
    scrap_data = urllib.request.urlopen(url)
    article = scrap_data.read()
    parsed_article = bs(article, 'lxml')
    paragraphs = parsed_article.find_all('p')
    article_text = ""

    for p in paragraphs:
        article_text += p.text

    article_text = re.sub(r'\[[0-9]*\]', '', article_text)
    return article_text

# Function to generate AI-based summary using BART model
def summarize_text():
    global text
    try:
        if not text.strip():
            messagebox.showwarning("Warning", "Input text is empty.")
            return

        # Get the max_length and min_length from the sliders
        max_length = max_length_var.get()
        min_length = min_length_var.get()

        # Truncate the text if it's too long for the model
        max_input_length = 1024  # Adjust based on the model's limitations
        if len(text) > max_input_length:
            messagebox.showwarning("Warning", f"Input text is too long. Truncating to the first {max_input_length} characters.")
            text_to_summarize = text[:max_input_length]
        else:
            text_to_summarize = text

        # Generate summary
        summary_result = summarizer(text_to_summarize, max_length=max_length, min_length=min_length, do_sample=False)
        summary = summary_result[0]['summary_text']

        # Split the summary into sentences
        doc = nlp(summary)
        sentences = [sent.text.strip() for sent in doc.sents]

        # Format the sentences as bullet points
        bullet_point_summary = ''
        for sentence in sentences:
            bullet_point_summary += f"• {sentence}\n"

        summary_text.delete(1.0, END)
        summary_text.insert(END, bullet_point_summary)

        # Word counts
        original_words = text.split()
        original_len = len(original_words)
        summary_len = len(summary.split())

        word_count_label.config(text=f"Original Word Count: {original_len} | Summary Word Count: {summary_len}")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# Functions to load text
def load_text_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        global text
        text = file_text(file_path)
        input_text.delete(1.0, END)
        input_text.insert(END, text)

def load_pdf_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        global text
        text = pdfReader(file_path)
        input_text.delete(1.0, END)
        input_text.insert(END, text)

def load_wiki_url():
    wiki_url = url_entry.get()
    if wiki_url:
        global text
        text = wiki_text(wiki_url)
        input_text.delete(1.0, END)
        input_text.insert(END, text)

# Styling Options
def set_style(widget, bg_color, fg_color, font_style):
    widget.config(bg=bg_color, fg=fg_color, font=font_style)

# Setting up the GUI
root = Tk()
root.title("AI-Powered Text Summarizer")
root.geometry("900x700")

# Define color scheme
bg_color = "#2C3E50"
fg_color = "#ECF0F1"
button_bg = "#3498DB"
button_fg = "#FFFFFF"
font_title = ("Helvetica", 16, "bold")
font_text = ("Helvetica", 12)
font_button = ("Helvetica", 12, "bold")

root.config(bg=bg_color)

# Frame for Input Text
input_frame = LabelFrame(root, text="Input Text", padx=10, pady=10, bg=bg_color, fg=fg_color, font=font_title)
input_frame.pack(padx=10, pady=10, fill="both", expand=True)

input_text = scrolledtext.ScrolledText(input_frame, height=10, wrap=WORD, bg="#34495E", fg=fg_color, font=font_text, insertbackground="white")
input_text.pack(fill="both", expand=True)

# Frame for Summary
summary_frame = LabelFrame(root, text="Summary", padx=10, pady=10, bg=bg_color, fg=fg_color, font=font_title)
summary_frame.pack(padx=10, pady=10, fill="both", expand=True)

summary_text = scrolledtext.ScrolledText(summary_frame, height=10, wrap=WORD, bg="#34495E", fg=fg_color, font=font_text, insertbackground="white")
summary_text.pack(fill="both", expand=True)

# Frame for Buttons
button_frame = Frame(root, bg=bg_color)
button_frame.pack(padx=10, pady=10)

load_text_button = Button(button_frame, text="Load Text File", command=load_text_file, bg=button_bg, fg=button_fg, font=font_button, relief="raised")
load_text_button.grid(row=0, column=0, padx=10, pady=5)

load_pdf_button = Button(button_frame, text="Load PDF File", command=load_pdf_file, bg=button_bg, fg=button_fg, font=font_button, relief="raised")
load_pdf_button.grid(row=0, column=1, padx=10, pady=5)

url_label = Label(button_frame, text="Wiki URL:", bg=bg_color, fg=fg_color, font=font_text)
url_label.grid(row=0, column=2)

url_entry = Entry(button_frame, width=40, font=font_text, bg="#34495E", fg=fg_color, insertbackground="white")
url_entry.grid(row=0, column=3, padx=10)

load_wiki_button = Button(button_frame, text="Load Wiki Article", command=load_wiki_url, bg=button_bg, fg=button_fg, font=font_button, relief="raised")
load_wiki_button.grid(row=0, column=4, padx=10, pady=5)

summarize_button = Button(root, text="Summarize Text", command=summarize_text, bg="#E74C3C", fg=button_fg, font=font_button, relief="raised", pady=5)
summarize_button.pack(pady=10)

word_count_label = Label(root, text="", bg=bg_color, fg=fg_color, font=font_text)
word_count_label.pack(pady=10)

# In your GUI setup
max_length_var = IntVar(value=150)
min_length_var = IntVar(value=50)

def submit_feedback():
    # Collect and store feedback
    pass


# Start the GUI event loop
root.mainloop()