"""Add car reservation table

Revision ID: f210ca418825
Revises: 65cb583a7fc3
Create Date: 2022-05-26 19:26:22.097647

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f210ca418825'
down_revision = '65cb583a7fc3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('car_reservation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('from_date', sa.DateTime(), nullable=True),
    sa.Column('to_date', sa.DateTime(), nullable=True),
    sa.Column('user_name', sa.String(), nullable=True),
    sa.Column('user_phone', sa.String(), nullable=True),
    sa.Column('user_email', sa.String(), nullable=True),
    sa.Column('additions', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('car_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['car_id'], ['car.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_car_reservation_id'), 'car_reservation', ['id'], unique=False)
    op.add_column('car', sa.Column('available', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('car', 'available')
    op.drop_index(op.f('ix_car_reservation_id'), table_name='car_reservation')
    op.drop_table('car_reservation')
    # ### end Alembic commands ###
