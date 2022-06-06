"""Create exchange apartment table

Revision ID: ee2e04567c5b
Revises: c63b63df3cd8
Create Date: 2022-06-02 23:16:04.672573

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ee2e04567c5b'
down_revision = 'c63b63df3cd8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('exchange_apartment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('location', sa.String(), nullable=True),
    sa.Column('coordinates', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('city', sa.String(), nullable=True),
    sa.Column('images', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('amenities', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('nearby', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('rooms', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('details', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('exchange_duration', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('desired_city', sa.String(), nullable=True),
    sa.Column('people_quantity', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_exchange_apartment_id'), 'exchange_apartment', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_exchange_apartment_id'), table_name='exchange_apartment')
    op.drop_table('exchange_apartment')
    # ### end Alembic commands ###
