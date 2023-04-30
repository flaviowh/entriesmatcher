import pytest
from unittest.mock import Mock
import os
from datetime import datetime
from decimal import Decimal
import pytz

from .entriesmatcher import EntriesMatcher
from .readers.pdf.bb_parser import BBpdfParser
from .readers.ofxreader import OFXStatement, MultipleOFXReader
from .db_interface import FakeAccountDB

from .testdata import sheet_entries, statement_entries

from environs import Env  # new
env = Env()  # new
env.read_env()  # new


# PATHS
DESKTOP = os.path.join(os.path.expanduser('~'), 'Desktop')
bb_pdf = rf"{DESKTOP}\work\demonstração\study\EXTRATO BB 01-2023.pdf"
bb_ofx = rf"{DESKTOP}\Work\demonstração\study\EXTRATO BB 01-2023.ofx"


# TEST PARSERS

class TestBBpdfParser:
    def test_bb_pdf_parser(self):
        bb_pdf_parser = BBpdfParser(bb_pdf)
        assert bb_pdf_parser.total_transactions() == Decimal("98352.42")

    def test_bb_pdf_parser_and_ofx_reader_match(self):
        bb_pdf_parser = BBpdfParser(bb_pdf)
        pdf_df = bb_pdf_parser.to_dataframe()
        bb_ofx_parser = OFXStatement(bb_ofx)
        ofx_df = bb_ofx_parser.to_dataframe()
        assert len(bb_pdf_parser.all_entries()) == len(
            bb_ofx_parser.all_entries())
        assert pdf_df.value.sum() == ofx_df.value.sum()

# TEST READERS


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
        assert statements[0].start_date == datetime(
            2022, 12, 30, 0, 0, tzinfo=pytz.UTC)
        assert statements[0].end_date == datetime(
            2023, 1, 31, 0, 0, tzinfo=pytz.UTC)


# TEST MATCHER

class TestEntriesMatcher:
    @pytest.fixture
    def matcher_obj(self) -> EntriesMatcher:
        fake_statement_reader = Mock()
        fake_statement_reader.entries_by_account.return_value = statement_entries
        fake_sheet_reader = Mock()
        fake_sheet_reader.entries_by_account.return_value = sheet_entries
        return EntriesMatcher(fake_statement_reader, fake_sheet_reader, FakeAccountDB())

    def test_matches_count(self, matcher_obj):
        matcher = matcher_obj
        statement_full_entries = matcher.all_entries()
        unmatched = matcher.unmatched_entries
        assert len(statement_full_entries) == 10
        assert len(unmatched) == 3
        assert matcher.match_count == 7

    def test_entries_data(self, matcher_obj):
        full_entries = matcher_obj.all_entries()
        received = full_entries[0]
        paid = full_entries[1]
        assert received.history.startswith("received")
        assert received.credit == "2"
        assert paid.history.startswith("paid")
        assert paid.debit == "259"