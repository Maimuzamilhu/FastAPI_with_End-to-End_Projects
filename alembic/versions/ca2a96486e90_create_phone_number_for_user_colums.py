"""Create Phone Number for user colums

Revision ID: ca2a96486e90
Revises: 
Create Date: 2024-11-26 23:14:42.643314

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ca2a96486e90'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("user" , sa.column("phone_numbr" , sa.String() , nullable = True))


def downgrade() -> None:
    op.drop_column("users" , "phone_number")
