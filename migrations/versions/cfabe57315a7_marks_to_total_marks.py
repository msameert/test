"""marks to total_marks

Revision ID: cfabe57315a7
Revises: 121710113bae
Create Date: 2026-08-18 16:45:28.846252

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cfabe57315a7'
down_revision: Union[str, Sequence[str], None] = '121710113bae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        "assessments",
        "marks",
        new_column_name="total_marks"
    )

def downgrade():
    op.alter_column(
        "assessments",
        "total_marks",
        new_column_name="marks"
    )
