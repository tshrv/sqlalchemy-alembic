# sqlalchemy-alembic: sqal
This project is a simple demonstration of SQLAlchemy (for ORM) and Alembic (for database migrations)

## SQLAlchemy
1. Establish connection
2. Transactions and DBAPI
3. Database Metadata

---

## Overview
1. **SQL Database** has a `users` table.
2. **SQLAlchemy** configuration for `UserModel` that connects to the `users` table in the database.
3. **Alembic** configuration to carry out database migrations
4. `UserService` defines a set of functionalities based on the `User` entity.

## Part 1: SQL Database
1. Setting up a **PostgreSQL** instance along with **PGAdmin**
2. A `.sql` file for the initial setup

## Part 2: SQL Alchemy
1. Defining the `UserModel`
2. Utilizing the `UserModel` to carry out operations on the `users` table in tha database

## Part 3: Alembic
1. Define configurations to carry out database migrations