"""empty message

Revision ID: 7f920bc95796
Revises: 
Create Date: 2019-05-22 18:49:22.029331

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f920bc95796'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('web_leave',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('LeavingName', sa.String(length=30), nullable=True),
    sa.Column('LeavingWord', sa.String(length=500), nullable=True),
    sa.Column('LeavingTime', sa.DateTime(), nullable=True),
    sa.Column('LeavingContact', sa.String(length=64), nullable=True),
    sa.Column('LeavingReply', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_web_leave_id'), 'web_leave', ['id'], unique=False)
    op.create_table('work_direction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=120), nullable=True),
    sa.Column('content', sa.TEXT(length=0), nullable=True),
    sa.Column('content_time', sa.DateTime(), nullable=True),
    sa.Column('content_look', sa.Integer(), nullable=True),
    sa.Column('content_type', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_work_direction_id'), 'work_direction', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_work_direction_id'), table_name='work_direction')
    op.drop_table('work_direction')
    op.drop_index(op.f('ix_web_leave_id'), table_name='web_leave')
    op.drop_table('web_leave')
    # ### end Alembic commands ###
