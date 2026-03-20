# Design Principles - SOLID

S.O.L.I.D is an acronym for five design principles that help software developers create maintainable, flexible, and scalable software. These principles are widely used in object-oriented programming.

## Single Responsibility Principle (SRP)

A class should have only one reason to change, meaning it should have only one responsibility. This principle helps to keep classes focused and easier to maintain.

**Bad**:

```python
class OrderService:
    def place_order(self, order: Order) -> None:
        # validates the order
        if not order.items:
            raise ValueError("Order has no items")
        if order.total <= 0:
            raise ValueError("Order total must be positive")

        # applies discount
        if order.customer_type == "premium":
            order.total *= 0.85

        # persists to database
        db.execute("INSERT INTO orders ...", order)

        # notifies the customer
        smtp.send(order.customer.email, f"Order {order.id} confirmed")
```

One method, four reasons to change: validation rules tighten, discount logic evolves, the database migrates, the email provider switches. Any of those changes forces you back into the same class.

**Good**:

```python
class OrderValidator:
    def validate(self, order: Order) -> None:
        if not order.items:
            raise ValueError("Order has no items")
        if order.total <= 0:
            raise ValueError("Order total must be positive")

# ---

class DiscountService:
    def apply(self, order: Order) -> None:
        if order.customer_type == "premium":
            order.total *= 0.85

# ---

class OrderRepository:
    def save(self, order: Order) -> None:
        db.execute("INSERT INTO orders ...", order)

# ---

class NotificationService:
    def notify(self, order: Order) -> None:
        smtp.send(order.customer.email, f"Order {order.id} confirmed")

# ---

class OrderService:
    def __init__(
        self,
        validator: OrderValidator,
        discount: DiscountService,
        repository: OrderRepository,
        notifier: NotificationService,
    ):
        self.validator = validator
        self.discount = discount
        self.repository = repository
        self.notifier = notifier

    def place_order(self, order: Order) -> None:
        self.validator.validate(order)
        self.discount.apply(order)
        self.repository.save(order)
        self.notifier.notify(order)
```

Each class now has exactly one reason to change. `OrderService` is reduced to an orchestrator — it owns the sequence, not the logic. Notice also that this naturally sets up **DIP**: each dependency could be swapped for a different implementation without touching OrderService at all.

## Open/Closed Principle (OCP)

Software entities (classes, modules, functions) should be open for extension but closed for modification. This means you should be able to add new behavior without changing existing code.

**Bad**:

```python
class OrderService:
    def calculate_discount(self, order: Order) -> float:
        if order.customer_type == "regular":
            return order.total * 0.05
        elif order.customer_type == "premium":
            return order.total * 0.15
        elif order.customer_type == "employee":
            return order.total * 0.30
        # adding "partner" means touching this method again and again
```

Business rules buried in conditionals. Every new customer type is a modification, not an extension.

**Good**:

```python
from typing import Protocol

class DiscountPolicy(Protocol):
    def calculate(self, order: Order) -> float: ...

# ---

class RegularDiscountStrategy:
    def calculate(self, order: Order) -> float:
        return order.total * 0.05

# ---

class PremiumDiscountStrategy:
    def calculate(self, order: Order) -> float:
        return order.total * 0.15

# ---

class EmployeeDiscountStrategy:
    def calculate(self, order: Order) -> float:
        return order.total * 0.30

# ---

# new behavior: zero existing code touched
class PartnerDiscountStrategy:
    def calculate(self, order: Order) -> float:
        return order.total * 0.40

# ---

class OrderService:
    def __init__(self, discount_policy: DiscountPolicy):
        self.discount_policy = discount_policy

    def calculate_discount(self, order: Order) -> float:
        return self.discount_policy.calculate(order) # Polymorphism
```

Adding `PartnerDiscount` required writing a new class and nothing else `OrderService` never changed. That's the open/closed principle: _extend by adding, never by editing_.

## Liskov Substitution Principle (LSP)

Subtypes must be substitutable for their base types without altering the correctness of the program. This means that derived classes should be able to replace their base classes without affecting the functionality.

- A subclass cannot demand more than the base class
- The subclass cannot reduce the garantes provided by the base class after the method execution
- The subclass cannot alter intern conditions maintained as constants by the base class

**Bad**:

```python
class BankAccount:
    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.balance += amount

# ---

class SavingsAccount(BankAccount):
    def deposit(self, amount: float) -> None:
        if amount < 50: # strengthens the precondition — LSP violation
            raise ValueError("Minimum deposit is $50")
        self.balance += amount
```

`BankAccount` promises that any positive amount is valid. `SavingsAccount` silently tightens that rule to $50, so any code that holds a `BankAccount` and deposits $10 will crash unexpectedly if it receives a `SavingsAccount`. The subclass broke the parent's contract.

**Good**:

```python
from abc import ABC, abstractmethod

class Account(ABC):
    def __init__(self):
        self.balance: float = 0.0

    @abstractmethod
    def deposit(self, amount: float) -> None: ...

    @abstractmethod
    def withdraw(self, amount: float) -> None: ...

# ---

# no minimum deposit restriction
class CurrentAccount(Account):
    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount

# ---

# honest about its own rules
class SavingsAccount(Account):
    MINIMUM_DEPOSIT = 50.0

    def deposit(self, amount: float) -> None:
        if amount < self.MINIMUM_DEPOSIT:
            raise ValueError(f"Minimum deposit is ${self.MINIMUM_DEPOSIT}")
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount

# ---


def process_deposit(account: Account, amount: float) -> None:
    account.deposit(amount) # Polymorphism
```

- The contract stays the same
- No unexpected errors
- Each implementation handles its own constraints internally, so client code can use any notification service without worrying about specific limitations.

`process_deposit` doesn't know — and doesn't care whether it received a `CurrentAccount` or a `SavingsAccount`. It calls `.deposit()` and each object responds according to its own rules. That's **polymorphism**: one interface, multiple behaviors.

## Interface Segregation Principle (ISP)

- Classes should not be forced to depend on methods they do not use. This means that it's better to have many specific interfaces rather than a single general-purpose interface.

### Why

- Improve class cohesion
- Reduce coupling
- Improves code reusability
- Improves software maintenance

**Bad**:

```python
class PaymentProcessor(Protocol):
    def charge(self, amount: float) -> Receipt: ...
    def refund(self, receipt: Receipt) -> None: ...
    def save_card(self, card: CardDetails) -> Token: ...
    def get_installments(self, amount: float) -> list[Installment]: ...

# ---

# PayPal supports everything
class PayPalProcessor:
    def charge(self, amount: float) -> Receipt: ...
    def refund(self, receipt: Receipt) -> None: ...
    def save_card(self, card: CardDetails) -> Token: ...
    def get_installments(self, amount: float) -> list[Installment]: ...

# ---

# Boleto has no card vault or installments natively
class BoletoProcessor:
    def charge(self, amount: float) -> Receipt: ...
    def refund(self, receipt: Receipt) -> None: raise NotImplementedError
    def save_card(self, card: CardDetails) -> Token: raise NotImplementedError
    def get_installments(self, amount: float) -> list[Installment]: raise NotImplementedError

# ---

# Pix is instant payment only
class PixProcessor:
    def charge(self, amount: float) -> Receipt: ...
    def refund(self, receipt: Receipt) -> None: ...
    def save_card(self, card: CardDetails) -> Token: raise NotImplementedError
    def get_installments(self, amount: float) -> list[Installment]: raise NotImplementedError
```

All three processors are forced to acknowledge methods they'll never support, turning the interface into a contract nobody fully honors.

**Good**:

```python
from typing import Protocol

class Chargeable(Protocol):
    def charge(self, amount: float) -> Receipt: ...

# ---

class Refundable(Protocol):
    def refund(self, receipt: Receipt) -> None: ...

# ---

class CardVaultable(Protocol):
    def save_card(self, card: CardDetails) -> Token: ...

# ---

class Installable(Protocol):
    def get_installments(self, amount: float) -> list[Installment]: ...

# ---

class PayPalProcessor(Chargeable, Refundable, CardVaultable, Installable):
    def charge(self, amount: float) -> Receipt: ...
    def refund(self, receipt: Receipt) -> None: ...
    def save_card(self, card: CardDetails) -> Token: ...
    def get_installments(self, amount: float) -> list[Installment]: ...

# ---

# Boleto is charge-only, no refund or vault
class BoletoProcessor(Chargeable):
    def charge(self, amount: float) -> Receipt: ...

# ---

# Pix supports refund, but no cards or installments
class PixProcessor(Chargeable, Refundable):
    def charge(self, amount: float) -> Receipt: ...
    def refund(self, receipt: Receipt) -> None: ...
```

Each processor implements exactly what its payment method supports by design. `save_card_for_later(p: CardVaultable)` statically rejects `BoletoProcessor` and `PixProcessor` no runtime surprises, no dead stubs, and adding a new processor like a crypto gateway never touches existing code.

Also instead of protocols _multiple inheritance_ could be used

## Dependency Inversion Principle (DIP)

Is the base principle for layered software architectures like _Ports and Adapters_.

- High-level modules should not depend on low-level modules. Both should depend on abstractions.
- Abstractions should not depend on details, details should depend on abstractions.
- Modules should not depend on external dependencies.
- We should depend on interfaces or abstract classes rather than concrete implementations.

### Why

- Improve flexibility: The software should grow healthy in a simple way, changing components without breaking what already exists.
- Improve maintenance: Follow the Open-Closed Principle.
- Improve testability: Be able to mock dependencies easily

**Bad**:

```python
class MySQLDatabase:
    def connect(self): ...

# ---

class UserRepository:
    def __init__(self):
        self.db = MySQLDatabase()  # tight coupling
    def get_user(self, user_id): ...
```

Here `UserRepository` is tightly coupled to `MySQLDatabase`, making it hard to change the database implementation without modifying `UserRepository`.

**Good**:

```python
from typing import Protocol

class DatabasePort(Protocol):
    def query(self, sql: str) -> list[dict]: ...

# ---

class MySQLAdapter:
    def query(self, sql: str) -> list[dict]: ...

# ---

# For unit testing purposes
class InMemoryAdapter:
    def query(self, sql: str) -> list[dict]: ...

# ---

class UserRepository:
    def __init__(self, db: DatabasePort):
        self.db = db  # depends on abstraction
    def get_user(self, user_id): ...
```

- You can inject any database
- You can mock easily
- You can switch implementation
