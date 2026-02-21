# ACID

Acid is an acronym that stands for Atomicity, Consistency, Isolation, and Durability. These are the key properties that ensure reliable processing of database transactions.

## Atomicity

Atomicity ensures that a transaction is treated as a single unit of work. It either completes entirely or does not happen at all. If any part of the transaction fails, the entire transaction is rolled back to maintain data integrity.

## Consistency

Consistency ensures that a transaction brings the database from one valid state to another valid state. It guarantees that any data written to the database must be valid according to all defined rules, including constraints, cascades, and triggers.

## Isolation

Isolation ensures that concurrent transactions do not interfere with each other. Each transaction should be executed in isolation, meaning that the intermediate state of a transaction is not visible to other transactions until it is completed.

## Durability

Durability ensures that once a transaction has been committed, it will remain so, even in the event of a system failure. This means that the changes made by the transaction are permanently stored in the database and will not be lost.
