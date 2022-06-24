"""Add exchange apartment reservation table

Revision ID: 5fde930fc9d1
Revises: ee2e04567c5b
Create Date: 2022-06-06 12:24:04.306378

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5fde930fc9d1'
down_revision = 'ee2e04567c5b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('exchange_apartment_reservation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('from_date', sa.Date(), nullable=True),
    sa.Column('to_date', sa.Date(), nullable=True),
    sa.Column('guest_name', sa.String(), nullable=True),
    sa.Column('guest_phone', sa.String(), nullable=True),
    sa.Column('user_email', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('apartment_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['apartment_id'], ['exchange_apartment.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_exchange_apartment_reservation_id'), 'exchange_apartment_reservation', ['id'], unique=False)
    op.add_column('exchange_apartment', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'exchange_apartment', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'exchange_apartment', type_='foreignkey')
    op.drop_column('exchange_apartment', 'user_id')
    op.drop_index(op.f('ix_exchange_apartment_reservation_id'), table_name='exchange_apartment_reservation')
    op.drop_table('exchange_apartment_reservation')
    # ### end Alembic commands ###
