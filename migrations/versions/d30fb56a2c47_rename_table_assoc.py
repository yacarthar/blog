"""rename table assoc

Revision ID: d30fb56a2c47
Revises: c6a48f1bea8d
Create Date: 2023-11-28 09:17:29.838358

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd30fb56a2c47'
down_revision = 'c6a48f1bea8d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post_x_tag',
    sa.Column('post_id', sa.String(length=10), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ),
    sa.PrimaryKeyConstraint('post_id', 'tag_id')
    )
    op.drop_table('associations')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('associations',
    sa.Column('post_id', sa.VARCHAR(length=10), autoincrement=False, nullable=False),
    sa.Column('tag_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], name='associations_post_id_fkey'),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], name='associations_tag_id_fkey'),
    sa.PrimaryKeyConstraint('post_id', 'tag_id', name='associations_pkey')
    )
    op.drop_table('post_x_tag')
    # ### end Alembic commands ###
