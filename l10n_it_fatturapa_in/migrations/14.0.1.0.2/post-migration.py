#  Copyright 2021 Alfredo Zamora - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade
from psycopg2 import sql


@openupgrade.migrate()
def migrate(env, version):
    if not version:
        return
    openupgrade.load_data(
        env.cr, "l10n_it_fatturapa_in", "migrations/14.0.1.0.2/noupdate_changes.xml"
    )

    openupgrade.logged_query(
        env.cr,
        """
update account_move
set
    fatturapa_attachment_in_id = inv.fatturapa_attachment_in_id,
    inconsistencies = inv.inconsistencies,
    e_invoice_amount_untaxed = inv.e_invoice_amount_untaxed,
    e_invoice_amount_tax = inv.e_invoice_amount_tax,
    e_invoice_amount_total = inv.e_invoice_amount_total,
    e_invoice_reference = inv.e_invoice_reference,
    e_invoice_date_invoice = inv.e_invoice_date_invoice,
    e_invoice_force_validation = inv.e_invoice_force_validation
from account_invoice inv
where
    account_move.id = inv.move_id;
    """,
    )

    openupgrade.logged_query(
        env.cr,
        """
update einvoice_line
set
    invoice_id = am.id
from account_invoice inv
    join account_move am on am.id = inv.move_id
where
    invoice_id = inv.id;
    """,
    )

    create_withholding_data_lines(env)


def create_withholding_data_lines(env):
    """
    Create ftpa_withholding_ids from ftpa_withholding_type
    and ftpa_withholding_amount
    """
    column_wht_amount = openupgrade.get_legacy_name("withholding_tax_amount")
    # column_wht_amount = openupgrade.get_legacy_name("ftpa_withholding_amount")
    # column_wht_type = openupgrade.get_legacy_name("ftpa_withholding_type")
    exists = openupgrade.column_exists(env.cr, "account_invoice", column_wht_amount)
    mapping = {
        "name": "ai.ftpa_withholding_type",
        "invoice_id": "ai.move_id",
        "create_uid": "ai.create_uid",
        "create_date": "ai.create_date",
        "write_date": "ai.write_date",
        "write_uid": "ai.write_uid",
    }
    if exists:
        mapping.update(
            {
                "amount": "ai.{ftpa_withholding_amount}".format(
                    ftpa_withholding_amount=column_wht_amount
                )
            }
        )
    query = """
        INSERT INTO withholding_data_line
        ({columns})
        SELECT {values}
        FROM account_invoice AS ai
        WHERE ai.ftpa_withholding_type IS NOT NULL;""".format(
        columns=",".join(mapping.keys()),
        values=",".join(mapping.values()),
    )
    openupgrade.logged_query(env.cr, sql.SQL(query))
