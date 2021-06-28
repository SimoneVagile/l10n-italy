#  Copyright 2021 Alfredo Zamora - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    if not version:
        return

    openupgrade.logged_query(
        env.cr,
        """
update account_tax at
set at.exclude_from_registries = atc.exclude_from_registries
from account_tax_code atc
where at.base_code_id = atc.id;
    """,
    )
