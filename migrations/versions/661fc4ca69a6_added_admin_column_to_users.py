"""Added admin column to users

Revision ID: 661fc4ca69a6
Revises: c7daf77d6b22
Create Date: 2021-08-05 10:31:57.105014

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '661fc4ca69a6'
down_revision = 'c7daf77d6b22'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('admin', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'admin')
    # ### end Alembic commands ###
