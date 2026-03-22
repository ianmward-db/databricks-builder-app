"""Grant PUBLIC access to builder_app schema and tables.

Revision ID: 20260323_grant_public_access
Revises: 20260115_warehouse_workspace
Create Date: 2026-03-23

Ensures any authenticated Databricks service principal can access the
builder_app schema without requiring manual GRANT statements. This prevents
the "relation does not exist" error when the app SP changes (e.g., app
is recreated or redeployed under a different service principal).
"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '20260323_grant_public_access'
down_revision: Union[str, None] = '20260115_warehouse_workspace'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  """Grant PUBLIC access to builder_app schema and tables."""
  # Allow any authenticated user to see and use objects in the schema
  op.execute('GRANT USAGE ON SCHEMA builder_app TO PUBLIC')
  op.execute('GRANT CREATE ON SCHEMA builder_app TO PUBLIC')

  # Grant DML on existing tables
  op.execute('GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA builder_app TO PUBLIC')

  # Ensure future tables also get PUBLIC access
  op.execute(
    'ALTER DEFAULT PRIVILEGES IN SCHEMA builder_app '
    'GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO PUBLIC'
  )


def downgrade() -> None:
  """Revoke PUBLIC access from builder_app schema and tables."""
  op.execute(
    'ALTER DEFAULT PRIVILEGES IN SCHEMA builder_app '
    'REVOKE SELECT, INSERT, UPDATE, DELETE ON TABLES FROM PUBLIC'
  )
  op.execute('REVOKE SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA builder_app FROM PUBLIC')
  op.execute('REVOKE CREATE ON SCHEMA builder_app FROM PUBLIC')
  op.execute('REVOKE USAGE ON SCHEMA builder_app FROM PUBLIC')
