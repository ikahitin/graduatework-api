"""Add location field to taxi reservation

Revision ID: 40b8c784835c
Revises: d8c7e4108d9e
Create Date: 2022-06-01 22:53:04.634184

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '40b8c784835c'
down_revision = 'd8c7e4108d9e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('taxi_reservation', sa.Column('reservation_datetime', sa.DateTime(), nullable=True))
    op.add_column('taxi_reservation', sa.Column('location', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.drop_column('taxi_reservation', 'reservation_date')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('taxi_reservation', sa.Column('reservation_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('taxi_reservation', 'location')
    op.drop_column('taxi_reservation', 'reservation_datetime')
    # ### end Alembic commands ###
