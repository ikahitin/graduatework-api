"""Update type field to location_type

Revision ID: 224cca44340c
Revises: aef7dfe68774
Create Date: 2022-04-19 14:54:49.177106

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '224cca44340c'
down_revision = 'aef7dfe68774'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('location', sa.Column('location_type', sa.String(), nullable=True))
    op.drop_column('location', 'type')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('location', sa.Column('type', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('location', 'location_type')
    # ### end Alembic commands ###
