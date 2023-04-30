from datetime import datetime
from decimal import Decimal

from .readers.base import SheetEntry, StatementEntry


statement_entries = {"default": [
    StatementEntry(date="10/11/2022",
                    history="random statement text",
                    value=Decimal("320"),
                    bank_id="default"),
    StatementEntry(date="09/15/2022",
                    history="another statement text",
                    value=Decimal("-200.50"),
                    bank_id="default"),
    StatementEntry(date="08/23/2022",
                    history="some statement text",
                    value=Decimal("400.75"),
                    bank_id="default"),
    StatementEntry(date="07/01/2022",
                    history="statement text",
                    value=Decimal("1000"),
                    bank_id="default"),
    StatementEntry(date="06/20/2022",
                    history="statement entry",
                    value=Decimal("-150.25"),
                    bank_id="default"),
    StatementEntry(date="05/10/2022",
                    history="statement text again",
                    value=Decimal("450"),
                    bank_id="default"),
    StatementEntry(date="04/01/2022",
                    history="statement random text",
                    value=Decimal("-75"),
                    bank_id="default"),
    StatementEntry(date="03/15/2022",
                    history="statement text once more",
                    value=Decimal("200.50"),
                    bank_id="default"),
    StatementEntry(date="02/10/2022",
                    history="statement entry text",
                    value=Decimal("400.75"),
                    bank_id="default"),
    StatementEntry(date="01/01/2022",
                    history="statement final text",
                    value=Decimal("-500"),
                    bank_id="default")
]}

# create a list of 10 SheetEntry instances, 7 of which have matching date and value values
sheet_entries = {"default":
                 [
                     SheetEntry(date="10/11/2022",
                                history="random sheet text",
                                value=Decimal("300"),
                                description="SHEET BOLETO",
                                bank_id="default"),
                     SheetEntry(date="09/15/2022",
                                history="another sheet text",
                                value=Decimal("200.50"),
                                description="SHEET PAYMENT",
                                bank_id="default"),
                     SheetEntry(date="08/23/2022",
                                history="some sheet text",
                                value=Decimal("400.75"),
                                description="SHEET TRANSFER",
                                bank_id="default"),
                     SheetEntry(date="07/01/2022",
                                history="sheet text",
                                value=Decimal("1000"),
                                description="SHEET BOLETO",
                                bank_id="default"),
                     SheetEntry(date="06/20/2022",
                                history="sheet entry",
                                value=Decimal("-150.25"),
                                description="SHEET PAYMENT",
                                bank_id="default"),
                     SheetEntry(date="05/10/2022",
                                history="sheet text again",
                                value=Decimal("450"),
                                description="SHEET BOLETO",
                                bank_id="default"),
                     SheetEntry(date="04/01/2022",
                                history="sheet random text",
                                value=Decimal("-75"),
                                description="SHEET PAYMENT",
                                bank_id="default"),
                     SheetEntry(date="03/15/2022",
                                history="sheet text once more",
                                value=Decimal("200.50"),
                                description="SHEET TRANSFER",
                                bank_id="default"),
                     SheetEntry(date="02/10/2022",
                                history="sheet entry text",
                                value=Decimal("400.75"),
                                description="SHEET BOLETO",
                                bank_id="default"),
                     SheetEntry(date="01/01/2022",
                                history="sheet final text",
                                value=Decimal("500"),
                                description="SHEET PAYMENT",
                                bank_id="default")
                 ]
}

