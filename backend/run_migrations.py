"""
Complete database migration script for Better Auth integration.
This script creates all necessary tables for Better Auth and user profiles.
"""

import asyncio
import asyncpg
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

async def run_migrations():
    """Run all database migrations."""
    
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        print("Starting database migrations...")
        
        # Create Better Auth tables
        print("\n1. Creating Better Auth tables...")
        better_auth_tables = """
        -- Users table (managed by Better Auth)
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            email_verified BOOLEAN DEFAULT false,
            name TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );

        -- Sessions table (managed by Better Auth)
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
            ip_address TEXT,
            user_agent TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );

        -- Accounts table (for OAuth providers, managed by Better Auth)
        CREATE TABLE IF NOT EXISTS accounts (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            account_id TEXT NOT NULL,
            provider_id TEXT NOT NULL,
            access_token TEXT,
            refresh_token TEXT,
            id_token TEXT,
            access_token_expires_at TIMESTAMP WITH TIME ZONE,
            refresh_token_expires_at TIMESTAMP WITH TIME ZONE,
            scope TEXT,
            password TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(provider_id, account_id)
        );

        -- Verification tokens table (managed by Better Auth)
        CREATE TABLE IF NOT EXISTS verification (
            id TEXT PRIMARY KEY,
            identifier TEXT NOT NULL,
            value TEXT NOT NULL,
            expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        await conn.execute(better_auth_tables)
        print("✓ Better Auth tables created successfully")
        
        # Create indexes for Better Auth tables
        print("\n2. Creating indexes...")
        indexes = """
        CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);
        CREATE INDEX IF NOT EXISTS idx_accounts_user_id ON accounts(user_id);
        CREATE INDEX IF NOT EXISTS idx_verification_identifier ON verification(identifier);
        """
        
        await conn.execute(indexes)
        print("✓ Indexes created successfully")
        
        # Create user_profiles table
        print("\n3. Creating user_profiles table...")
        user_profiles_table = """
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
        """
        
        await conn.execute(user_profiles_table)
        print("✓ user_profiles table created successfully")
        
        # Create trigger for updated_at
        print("\n4. Creating triggers...")
        triggers = """
        -- Create trigger function to update the updated_at column
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ language 'plpgsql';

        -- Apply trigger to users table
        DROP TRIGGER IF EXISTS update_users_updated_at ON users;
        CREATE TRIGGER update_users_updated_at
            BEFORE UPDATE ON users
            FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

        -- Apply trigger to sessions table
        DROP TRIGGER IF EXISTS update_sessions_updated_at ON sessions;
        CREATE TRIGGER update_sessions_updated_at
            BEFORE UPDATE ON sessions
            FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

        -- Apply trigger to accounts table
        DROP TRIGGER IF EXISTS update_accounts_updated_at ON accounts;
        CREATE TRIGGER update_accounts_updated_at
            BEFORE UPDATE ON accounts
            FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

        -- Apply trigger to verification table
        DROP TRIGGER IF EXISTS update_verification_updated_at ON verification;
        CREATE TRIGGER update_verification_updated_at
            BEFORE UPDATE ON verification
            FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

        -- Apply trigger to user_profiles table
        DROP TRIGGER IF EXISTS update_user_profiles_updated_at ON user_profiles;
        CREATE TRIGGER update_user_profiles_updated_at
            BEFORE UPDATE ON user_profiles
            FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
        """
        
        await conn.execute(triggers)
        print("✓ Triggers created successfully")
        
        print("\n✅ All migrations completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error running migrations: {e}")
        raise
    finally:
        await conn.close()


async def check_tables():
    """Check which tables exist in the database."""
    
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        query = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        ORDER BY table_name;
        """
        
        tables = await conn.fetch(query)
        
        print("\nExisting tables in database:")
        if tables:
            for table in tables:
                print(f"  - {table['table_name']}")
        else:
            print("  No tables found")
            
    except Exception as e:
        print(f"Error checking tables: {e}")
    finally:
        await conn.close()


async def drop_all_tables():
    """Drop all tables (use with caution!)."""
    
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        print("⚠️  WARNING: Dropping all tables...")
        
        drop_query = """
        DROP TABLE IF EXISTS user_profiles CASCADE;
        DROP TABLE IF EXISTS verification CASCADE;
        DROP TABLE IF EXISTS accounts CASCADE;
        DROP TABLE IF EXISTS sessions CASCADE;
        DROP TABLE IF EXISTS users CASCADE;
        DROP FUNCTION IF EXISTS update_updated_at_column CASCADE;
        """
        
        await conn.execute(drop_query)
        print("✓ All tables dropped successfully")
        
    except Exception as e:
        print(f"Error dropping tables: {e}")
        raise
    finally:
        await conn.close()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "migrate":
            print("Running migrations...")
            asyncio.run(run_migrations())
        elif command == "check":
            print("Checking database tables...")
            asyncio.run(check_tables())
        elif command == "drop":
            response = input("Are you sure you want to drop all tables? (yes/no): ")
            if response.lower() == "yes":
                asyncio.run(drop_all_tables())
            else:
                print("Operation cancelled")
        else:
            print("Usage: python run_migrations.py [migrate|check|drop]")
            print("  migrate - Run all migrations")
            print("  check   - Check existing tables")
            print("  drop    - Drop all tables (requires confirmation)")
    else:
        print("Running migrations by default...")
        asyncio.run(run_migrations())
