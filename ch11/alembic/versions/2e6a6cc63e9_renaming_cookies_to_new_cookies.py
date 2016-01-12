"""Renaming cookies to new_cookies

Revision ID: 2e6a6cc63e9
Revises: 34044511331
Create Date: 2015-09-14 21:21:07.579264

"""

# revision identifiers, used by Alembic.
revision = '2e6a6cc63e9'
down_revision = '34044511331'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.rename_table('cookies', 'new_cookies')


def downgrade():
    op.rename_table('new_cookies', 'cookies')
