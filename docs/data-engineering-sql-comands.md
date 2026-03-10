# SQL Commands

## DDL (Data Definition Language)

- Create:

```sql
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    hire_date DATE,
);
```

- Alter:

```sql
ALTER TABLE employees
ADD COLUMN email VARCHAR(100);
```

- Drop:

```sql
DROP TABLE employees;
```

## DCL (Data Control Language)

- Grant:

```sql
GRANT SELECT, INSERT ON employees TO user_name;
```

- Revoke"

```sql
REVOKE SELECT, INSERT ON employees FROM user_name;
```

- Deny:

```sql
DENY SELECT, INSERT ON employees TO user_name;
```

## DML (Data Manipulation Language)

- Select:

```sql
SELECT * FROM employees;
```

- Insert:

```sql
INSERT INTO employees (employee_id, first_name, last_name, hire_date)
VALUES (1, 'John', 'Doe', '2024-01-15');
```

- Update:

```sql
UPDATE employees
SET email = 'john.doe@example.com'
WHERE employee_id = 1;
```

- Delete:

```sql
DELETE FROM employees
WHERE employee_id = 1;
```
