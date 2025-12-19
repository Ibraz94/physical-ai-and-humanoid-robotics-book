"""
Safe migration script that handles existing tables.
This script checks for existing tables and only creates what's missing.
"""

import asyncio
import asyncpg
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

async def check_table_exists(conn, table_name):
    """Check if a table exists."""
    query = """
    SELECT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name = $1
    );
    """
    result = await conn.fetchval(query, table_name)
    return result

async def check_column_exists(conn, table_name, column_name):
    """Check if a column exists in a table."""
    query = """
    SELECT EXISTS (
        SELECT FROM information_schema.columns 
        WHERE table_schema = 'public' 
        AND table_name = $1 
        AND column_name = $2
    );
    """
    result = await conn.fetchval(query, table_name, column_name)
    return result

async def safe_migrate():
    """Run migrations safely, checking for existing tables."""
    
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        print("Starting safe database migrations...")
        print("=" * 60)
        
        # Check and create users table
        print("\n1. Checking users table...")
        if not await check_table_exists(conn, 'users'):
            print("   Creating users table...")
            await conn.execute("""
                CREATE TABLE users (
                    id TEXT PRIMARY KEY,
                    email TEXT UNIQUE NOT NULL,
                    email_verified BOOLEAN DEFAULT false,
                    name TEXT,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
            """)
            print("   ✓ users table created")
        else:
            print("   ✓ users table already exists")
        
        # Check and create sessions table
        print("\n2. Checking sessions table...")
        if not await check_table_exists(conn, 'sessions'):
            print("   Creating sessions table...")
            await conn.execute("""
                CREATE TABLE sessions (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
                    ip_address TEXT,
                    user_agent TEXT,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
                CREATE INDEX idx_sessions_user_id ON sessions(user_id);
            """)
            print("   ✓ sessions table created")
        else:
            print("   ✓ sessions table already exists")
            # Check if we need to add missing columns
            if not await check_column_exists(conn, 'sessions', 'ip_address'):
                print("   Adding ip_address column...")
                await conn.execute("ALTER TABLE sessions ADD COLUMN IF NOT EXISTS ip_address TEXT;")
            if not await check_column_exists(conn, 'sessions', 'user_agent'):
                print("   Adding user_agent column...")
                await conn.execute("ALTER TABLE sessions ADD COLUMN IF NOT EXISTS user_agent TEXT;")
        
        # Check and create accounts table
        print("\n3. Checking accounts table...")
        if not await check_table_exists(conn, 'accounts'):
            print("   Creating accounts table...")
            await conn.execute("""
                CREATE TABLE accounts (
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
                CREATE INDEX idx_accounts_user_id ON accounts(user_id);
            """)
            print("   ✓ accounts table created")
        else:
            print("   ✓ accounts table already exists")
        
        # Check and create verification table
        print("\n4. Checking verification table...")
        if not await check_table_exists(conn, 'verification'):
            print("   Creating verification table...")
            await conn.execute("""
                CREATE TABLE verification (
                    id TEXT PRIMARY KEY,
                    identifier TEXT NOT NULL,
                    value TEXT NOT NULL,
                    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
                CREATE INDEX idx_verification_identifier ON verification(identifier);
            """)
            print("   ✓ verification table created")
        else:
            print("   ✓ verification table already exists")
        
        # Check and create user_profiles table
        print("\n5. Checking user_profiles table...")
        if not await check_table_exists(conn, 'user_profiles'):
            print("   Creating user_profiles table...")
            await conn.execute("""
                CREATE TABLE user_profiles (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
                    software_background TEXT,
                    hardware_background TEXT,
                    consent_given BOOLEAN NOT NULL DEFAULT false,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
                CREATE INDEX idx_user_profiles_user_id ON user_profiles(user_id);
            """)
            print("   ✓ user_profiles table created")
        else:
            print("   ✓ user_profiles table already exists")
        
        # Create or replace trigger function
        print("\n6. Setting up triggers...")
        await conn.execute("""
            CREATE OR REPLACE FUNCTION update_updated_at_column()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.updated_at = CURRENT_TIMESTAMP;
                RETURN NEW;
            END;
            $$ language 'plpgsql';
        """)
        
        # Apply triggers to all tables
        tables = ['users', 'sessions', 'accounts', 'verification', 'user_profiles']
        for table in tables:
            if await check_table_exists(conn, table):
                await conn.execute(f"""
                    DROP TRIGGER IF EXISTS update_{table}_updated_at ON {table};
                    CREATE TRIGGER update_{table}_updated_at
                        BEFORE UPDATE ON {table}
                        FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
                """)
        print("   ✓ Triggers created successfully")
        
        print("\n" + "=" * 60)
        print("✅ All migrations completed successfully!")
        print("\nDatabase is ready for Better Auth integration.")
        
    except Exception as e:
        print(f"\n❌ Error running migrations: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        await conn.close()


async def show_schema():
    """Show the current database schema."""
    
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        print("\n" + "=" * 60)
        print("DATABASE SCHEMA")
        print("=" * 60)
        
        # Get all tables
        tables_query = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        ORDER BY table_name;
        """
        tables = await conn.fetch(tables_query)
        
        if not tables:
            print("\nNo tables found in database.")
            return
        
        for table in tables:
            table_name = table['table_name']
            print(f"\n📋 Table: {table_name}")
            print("-" * 60)
            
            # Get columns for this table
            columns_query = """
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = $1
            ORDER BY ordinal_position;
            """
            columns = await conn.fetch(columns_query, table_name)
            
            for col in columns:
                nullable = "NULL" if col['is_nullable'] == 'YES' else "NOT NULL"
                default = f" DEFAULT {col['column_default']}" if col['column_default'] else ""
                print(f"  • {col['column_name']:<30} {col['data_type']:<20} {nullable}{default}")
        
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"Error showing schema: {e}")
    finally:
        await conn.close()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "schema":
        print("Showing database schema...")
        asyncio.run(show_schema())
    else:
        print("Running safe migrations...")
        asyncio.run(safe_migrate())
        print("\nTo view the schema, run: python safe_migrate.py schema")
