import string
import unicodedata
import PyPDF2
import pdfplumber


class PDFreader:
    def read(self, pdf_path):
        if pdf_path.endswith(".pdf"):
            text = self._read_with_pypdf2(pdf_path)
            if self.is_valid(text):
                return text
            else:
                return self._read_with_pdfplumber(pdf_path)
        else:
            raise Exception(f"invalid PDF format for {pdf_path}")

    def _read_with_pdfplumber(self, pdf_path):
        with pdfplumber.open(pdf_path) as pdf:
            pages = []
            for pagen in pdf.pages:
                text = pagen.extract_text()
                if text is not None:
                    pages.append(text)
            text = '\n'.join(pages)
        return text

    def _read_with_pypdf2(self, pdf_path):
        pdfFileObj = open(pdf_path, 'rb')
        # creating a pdf reader object
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        pages = []
        for page in range(0, pdfReader.numPages):
            pageObj = pdfReader.getPage(page)
            # extracting text from page
            pagetxt = pageObj.extractText()
            pages.append(pagetxt)
        return '\n'.join(pages)

    def is_valid(self, text):
        return True if len(text) >=100 else False

    def unpunctuate(self, text):
        """Remove all diacritic marks from Latin base characters"""
        norm_txt = unicodedata.normalize('NFD', text)
        latin_base = False
        preserve = []
        for c in norm_txt:
            if unicodedata.combining(c) and latin_base:
                continue  # ignore diacritic on Latin base char
            preserve.append(c)
        # if it isn't a combining char, it's a new base char
            if not unicodedata.combining(c):
                latin_base = c in string.ascii_letters
        normalized = ''.join(preserve)
        return unicodedata.normalize('NFC', normalized)