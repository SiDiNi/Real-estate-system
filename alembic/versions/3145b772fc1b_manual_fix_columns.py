"""manual fix columns

Revision ID: 3145b772fc1b
Revises: 8ec85b800005
Create Date: 2026-05-22 12:00:10.370371

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "3145b772fc1b"
down_revision: Union[str, Sequence[str], None] = "8ec85b800005"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
