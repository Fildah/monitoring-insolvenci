"""Added active parametr to user

Revision ID: c7daf77d6b22
Revises: 86efb051419a
Create Date: 2021-08-02 08:12:32.187604

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'c7daf77d6b22'
down_revision = '86efb051419a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('active', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'active')
    # ### end Alembic commands ###
