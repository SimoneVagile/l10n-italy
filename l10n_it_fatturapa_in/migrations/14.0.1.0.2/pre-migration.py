from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    if not version:
        return
    openupgrade.logged_query(
        env.cr,
        """
    ALTER TABLE fatturapa_attachment_in
        ADD COLUMN IF NOT EXISTS invoices_date character varying
    """,
    )

    if openupgrade.column_exists(env.cr, "account_invoice", "ftpa_withholding_amount"):
        openupgrade.copy_columns(
            env.cr,
            {
                "account_invoice": [
                    ("ftpa_withholding_amount", None, None),
                ],
            },
        )
    if not openupgrade.column_exists(
        env.cr, "account_invoice", "ftpa_withholding_type"
    ):
        openupgrade.copy_columns(
            env.cr,
            {
                "account_invoice": [
                    ("ftpa_withholding_type", None, None),
                ],
            },
        )
