"""
Database migration script for user_profiles table to store user background information
and consent flags for Better Auth integration.
"""

import asyncio
import asyncpg
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

async def create_user_profiles_table():
    """Create the user_profiles table with proper foreign key relationship to Better Auth users."""

    conn = await asyncpg.connect(DATABASE_URL)

    try:
        # Create the user_profiles table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_profiles (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
            software_background TEXT,
            hardware_background TEXT,
            consent_given BOOLEAN NOT NULL DEFAULT false,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );

        -- Create index on user_id for faster lookups
        CREATE INDEX IF NOT EXISTS idx_user_profiles_user_id ON user_profiles(user_id);

        -- Create trigger to update the updated_at column
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ language 'plpgsql';

        DROP TRIGGER IF EXISTS update_user_profiles_updated_at ON user_profiles;
        CREATE TRIGGER update_user_profiles_updated_at
            BEFORE UPDATE ON user_profiles
            FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();
        """

        await conn.execute(create_table_query)
        print("✓ user_profiles table created successfully")

    except Exception as e:
        print(f"✗ Error creating user_profiles table: {e}")
        raise
    finally:
        await conn.close()


async def drop_user_profiles_table():
    """Drop the user_profiles table (for development/testing purposes)."""

    conn = await asyncpg.connect(DATABASE_URL)

    try:
        drop_table_query = "DROP TABLE IF EXISTS user_profiles;"
        await conn.execute(drop_table_query)
        print("✓ user_profiles table dropped successfully")

    except Exception as e:
        print(f"✗ Error dropping user_profiles table: {e}")
        raise
    finally:
        await conn.close()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "drop":
            print("Dropping user_profiles table...")
            asyncio.run(drop_user_profiles_table())
        elif sys.argv[1] == "create":
            print("Creating user_profiles table...")
            asyncio.run(create_user_profiles_table())
        else:
            print("Usage: python database_migrations.py [create|drop]")
    else:
        print("Creating user_profiles table...")
        asyncio.run(create_user_profiles_table())