"""Alter ApartmentReservation field

Revision ID: 550b09341b76
Revises: ceaf574dd9c4
Create Date: 2022-05-19 21:06:46.272934

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '550b09341b76'
down_revision = 'ceaf574dd9c4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('apartment_reservation', sa.Column('arriving_hour', sa.Integer(), nullable=True))
    op.drop_column('apartment_reservation', 'arriving_time')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('apartment_reservation', sa.Column('arriving_time', postgresql.TIME(), autoincrement=False, nullable=True))
    op.drop_column('apartment_reservation', 'arriving_hour')
    # ### end Alembic commands ###
