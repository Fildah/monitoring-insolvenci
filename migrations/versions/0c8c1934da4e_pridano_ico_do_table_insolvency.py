"""Pridano ICO do table Insolvency

Revision ID: 0c8c1934da4e
Revises: f5b9d9ec643a
Create Date: 2021-07-25 18:45:54.726378

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '0c8c1934da4e'
down_revision = 'f5b9d9ec643a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('insolvency', sa.Column('ico', sa.String(length=8), nullable=True))
    op.create_index(op.f('ix_insolvency_ico'), 'insolvency', ['ico'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_insolvency_ico'), table_name='insolvency')
    op.drop_column('insolvency', 'ico')
    # ### end Alembic commands ###
