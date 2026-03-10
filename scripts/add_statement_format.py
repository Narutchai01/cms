#!/usr/bin/env python3

import logging
from sqlalchemy import text
from cms.db import SessionGen

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate_statements_table():
    logger.info("Starting migration: adding 'format' column to 'statements' table.")
    with SessionGen() as session:
        try:
            # Check if column exists first
            result = session.execute(text(
                "SELECT column_name "
                "FROM information_schema.columns "
                "WHERE table_name='statements' and column_name='format';"
            ))
            if result.fetchone() is not None:
                logger.info("Column 'format' already exists in 'statements' table. Skipping migration.")
                return

            # Add the 'format' column
            session.execute(text("ALTER TABLE statements ADD COLUMN format VARCHAR NOT NULL DEFAULT 'pdf';"))
            session.commit()
            logger.info("Successfully added 'format' column to 'statements' table.")
        except Exception as e:
            session.rollback()
            logger.error("Failed to add 'format' column: %s", getattr(e, "message", repr(e)))
            raise

if __name__ == "__main__":
    migrate_statements_table()
