from openupgradelib import openupgrade

field_renames = [
    ("account.tax.registry", "account_tax_registry", "type", "layout_type"),
]


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_fields(env, field_renames)
