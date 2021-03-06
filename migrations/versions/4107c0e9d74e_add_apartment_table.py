"""Add apartment table

Revision ID: 4107c0e9d74e
Revises: 224cca44340c
Create Date: 2022-04-23 19:15:37.054934

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4107c0e9d74e'
down_revision = '224cca44340c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('apartment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('short_description', sa.String(), nullable=True),
    sa.Column('location', sa.String(), nullable=True),
    sa.Column('coordinates', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('city', sa.String(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('images', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('rating', sa.Float(), nullable=True),
    sa.Column('apartment_type', sa.String(), nullable=True),
    sa.Column('amenities', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('distance_from_center', sa.Float(), nullable=True),
    sa.Column('beds', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_apartment_id'), 'apartment', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_apartment_id'), table_name='apartment')
    op.drop_table('apartment')
    # ### end Alembic commands ###
