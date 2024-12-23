# AI-Powered Text Summarizer

This project is a graphical user interface (GUI) application for text summarization using artificial intelligence (AI) models. It enables users to load text from various sources (text files, PDF documents, and Wikipedia articles), summarize the content, and view word count comparisons between the original and summarized texts.

## Features

- **Text Summarization**: Leverages the BART model from Hugging Face's Transformers library for accurate and concise summaries.
- **Multi-Source Input**:
  - Load text from `.txt` files
  - Extract text from PDF documents
  - Fetch content from Wikipedia articles using URLs
- **Interactive GUI**: Built with Python's `tkinter`, offering an intuitive interface for loading text, generating summaries, and viewing results.
- **Customizable Summary Length**: Users can adjust the `max_length` and `min_length` parameters for summaries.
- **Word Count Metrics**: Displays the word count of both the original and summarized texts.

## License
- This project is licensed under the MIT License.

## Acknowledgements

- Hugging Face Transformers
- NLTK
- SpaCy

## Requirements

To run the application, make sure you have Python 3.8 or higher and the following dependencies installed:

- `tkinter` (built-in with Python)
- `nltk`
- `spacy`
- `transformers`
- `PyPDF2`
- `beautifulsoup4`
- `lxml`
- `rouge-score`

Install all dependencies by running:

```bash
pip install -r requirements.txt

# Text-Summarizer-Project
# Text-Summarizer-Project
