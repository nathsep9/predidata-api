"""empty message

Revision ID: def519e2796a
Revises: 57b0d753b8cc
Create Date: 2022-02-14 11:41:31.638260

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'def519e2796a'
down_revision = '57b0d753b8cc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('properties', 'real_estate_registration',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger(),
               existing_nullable=False)
    op.create_unique_constraint(None, 'properties', ['real_estate_registration'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'properties', type_='unique')
    op.alter_column('properties', 'real_estate_registration',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER(),
               existing_nullable=False)
    # ### end Alembic commands ###