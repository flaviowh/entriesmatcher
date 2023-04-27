from .pdftools.bb_parser import BBpdfParser
from datetime import datetime
import pytz
from decimal import Decimal
from ofxreader import OFXStatement, MultipleOFXReader
import pytest
import os
from environs import Env  # new
env = Env()  # new
env.read_env()  # new


# PATHS
DESKTOP = os.path.join(os.path.expanduser('~'), 'Desktop')
bb_pdf = rf"{DESKTOP}\work\demonstração\study\EXTRATO BB 01-2023 PDF (01-02-2023).pdf"
bb_pdf2 = rf"{DESKTOP}\work\demonstração\01-2022\EXTRATO - JANEIRO-22.pdf"
bb_ofx = rf"{DESKTOP}\Work\demonstração\study\EXTRATO BB 01-2023 OFX (01-02-2023).ofx"


# TEST PARSERS

class TestBBpdfParser:
    def test_bb_pdf_parser(self):
        bb_pdf_parser = BBpdfParser(bb_pdf)
        bb_pdf_parser2 = BBpdfParser(bb_pdf2)
        assert bb_pdf_parser.total_transactions() == Decimal("98352.42")
        assert bb_pdf_parser2.total_transactions() == Decimal("0")

    def test_bb_pdf_parser_and_ofx_reader_match(self):
        bb_pdf_parser = BBpdfParser(bb_pdf)
        pdf_df = bb_pdf_parser.to_dataframe()
        bb_ofx_parser = OFXStatement(bb_ofx)
        ofx_df = bb_ofx_parser.to_dataframe()
        assert len(bb_pdf_parser.all_entries()) == len(bb_ofx_parser.all_entries())
        assert pdf_df.value.sum() == ofx_df.value.sum()
        

class TestOFXStatement:
    @pytest.fixture
    def ofx_statement(self):
        return OFXStatement(bb_ofx)

    def test_all_entries(self, ofx_statement):
        entries = ofx_statement.all_entries()
        selected = 10
        assert len(entries) == 122
        assert entries[selected].date == "05/01/2023"
        assert entries[selected].value == Decimal("-46.08")
        assert entries[selected].history == "PAGAMENTO DE BOLETO"
        assert entries[selected].bank_id == env.str("TEST_BB_ID")


class TestMultipleOFXReader:
    @pytest.fixture
    def multiple_ofx_reader(self):
        abs_path = fr"{DESKTOP}\Work\demonstração\study\multi ofx reader test"
        return MultipleOFXReader(abs_path)

    def test_all_entries(self, multiple_ofx_reader):
        entries = multiple_ofx_reader.all_entries()
        assert len(entries) == 152

    def test_entries_by_account(self, multiple_ofx_reader):
        entries = multiple_ofx_reader.entries_by_account()
        assert len(entries) == 2
        assert entries[env.str("TEST_BB_ID")][0].date == "04/01/2023"

    def test_statements(self, multiple_ofx_reader):
        statements = multiple_ofx_reader.statements()
        assert len(statements) == 2
        assert statements[0].start_date == datetime(2022, 12, 30, 0, 0, tzinfo=pytz.UTC)
        assert statements[0].end_date == datetime(2023, 1, 31, 0, 0, tzinfo=pytz.UTC)
