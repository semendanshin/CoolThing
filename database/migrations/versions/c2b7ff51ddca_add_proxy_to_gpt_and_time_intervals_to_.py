"""add proxy to gpt and time intervals to campaign

Revision ID: c2b7ff51ddca
Revises: 74bed66211d6
Create Date: 2024-08-03 21:37:20.100405

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2b7ff51ddca'
down_revision: Union[str, None] = '74bed66211d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('campaigns', sa.Column('new_lead_wait_interval_seconds', sa.String(), server_default='180-300', nullable=False))
    op.add_column('campaigns', sa.Column('chat_answer_wait_interval_seconds', sa.String(), server_default='15-30', nullable=False))
    op.add_column('gpt_settings', sa.Column('proxy', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('gpt_settings', 'proxy')
    op.drop_column('campaigns', 'chat_answer_wait_interval_seconds')
    op.drop_column('campaigns', 'new_lead_wait_interval_seconds')
    # ### end Alembic commands ###
