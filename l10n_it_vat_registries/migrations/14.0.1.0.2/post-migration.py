#  Copyright 2021 Alfredo Zamora - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.load_data(
        env.cr, "l10n_it_vat_registries", "migrations/14.0.1.0.2/noupdate_changes.xml"
    )

    openupgrade.logged_query(
        env.cr,
        """
update account_tax
set exclude_from_registries = atc.exclude_from_registries
from account_tax_code atc
where base_code_id = atc.id;
    """,
    )
