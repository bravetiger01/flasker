"""Initial Migration

Revision ID: 37dbc0db0c82
Revises: 
Create Date: 2024-06-24 10:05:16.161958

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37dbc0db0c82'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('field', sa.String(length=120), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('field')

    # ### end Alembic commands ###