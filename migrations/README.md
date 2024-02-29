## Useful commands

In this section, I’ll describe some useful [Alembic commands](https://alembic.sqlalchemy.org/en/latest/api/commands.html), but I recommend exploring the Alembic commands page to learn more.

> Check if revision command with autogenerate has pending upgrade ops:
>
> ```Bash
> alembic check
> ```

> Autogenerate the initial migrations:
>
> ```Bash
> alembic revision --autogenerate -m "Init"
> ```

> Generate an empty migration:
>
> ```Bash
> alembic revision -m "message"
> ```

> Display the current revision for a database:
>
> ```Bash
> alembic current
> ```

> View migrations history:
>
> ```Bash
> alembic history --verbose
> ```

> Revert all migrations:
>
> ```Bash
> alembic downgrade base
> ```

> Revert migrations one by one:
>
> ```Bash
> alembic downgrade -1
> ```

> Apply all migrations:
>
> ```Bash
> alembic upgrade head
> ```

> Apply migrations one by one:
>
> ```Bash
> alembic upgrade +1
> ```

> Display all raw SQL:
>
> ```Bash
> alembic upgrade head --sql
> ```

> Reset the database:
>
> ```Bash
> alembic downgrade base && alembic upgrade head
> ```
