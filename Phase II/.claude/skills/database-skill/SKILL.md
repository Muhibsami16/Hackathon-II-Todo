---
name: database-skill
description: Design, create, and manage databases with proper schema design, tables, and migrations.
---

# Database Design & Management Skill

## Instructions

1. **Schema design**
   - Identify entities and relationships
   - Apply normalization (1NF, 2NF, 3NF)
   - Define primary and foreign keys

2. **Table creation**
   - Use appropriate data types
   - Apply constraints (NOT NULL, UNIQUE, CHECK)
   - Set indexes for performance

3. **Migrations**
   - Version-controlled schema changes
   - Forward and rollback migrations
   - Safe changes for production databases

4. **Relationships**
   - One-to-One
   - One-to-Many
   - Many-to-Many (junction tables)

## Best Practices
- Use clear and consistent naming conventions
- Avoid redundant data
- Always use migrations instead of manual changes
- Backup database before structural updates
- Optimize queries with indexes
- Document schema changes

## Example Structure
```sql
-- Create users table
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(150) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create posts table with relationship
CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(id),
  title VARCHAR(200) NOT NULL,
  content TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
