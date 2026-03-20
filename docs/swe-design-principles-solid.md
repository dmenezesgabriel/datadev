# Design Principles - SOLID

S.O.L.I.D is an acronym for five design principles that help software developers create maintainable, flexible, and scalable software. These principles are widely used in object-oriented programming.

## Single Responsibility Principle (SRP)

A class should have only one reason to change, meaning it should have only one responsibility. This principle helps to keep classes focused and easier to maintain.

**Bad**:

```python
class User:
    def create_user(self, user_data): ...
    def validate_user(self, user_data): ...
    def send_email(self, email_data): ...
    def save_to_database(self, user_data): ...
```

This class handles:

- business logic
- persistence
- email sending

Too many responsibilities, making it tightly coupled and hard to test.

**Good**:

```python
class UserValidator: ...
class UserRepository: ...
class EmailService: ...
class UserService: ...
```

Each class has only one reason to change:

- `UserRepository`: change if we change the database
- `EmailService`: change if we change the email provider
- `UserValidator`: change if we change validation rules
- `UserService`: change if we change business logic

## Open/Closed Principle (OCP)

Software entities (classes, modules, functions) should be open for extension but closed for modification. This means you should be able to add new behavior without changing existing code.

**Bad**:

```python
class PaymentProcessor:
    def process(self, payment_type):
        if payment_type == 'credit_card':
            ...
        elif payment_type == 'paypal':
            ...
```

To add a new payment type, we need to modify the `process` method, which can introduce bugs.

**Good**:

```python
from typing import Protocol


class Payment(Protocol):
    def process(self) -> None:
        ...


class CreditCardPayment:
    def process(self) -> None:
        print("Processing credit card")


class PayPalPayment:
    def process(self) -> None:
        print("Processing PayPal")


class PaymentProcessor:
    def process(self, payment: Payment) -> None:
        payment.process()
```

Now the behavior can be extended by creating new payment classes without modifying existing code. In the example above we use polymorphism that is the same interface but with a different behavior. The `PaymentProcessor` can process any payment type that implements the `Payment` interface.

Other patterns also present are strategy where `Payment` is the strategy interface and `CreditCardPayment` and `PayPalPayment` are concrete strategies. The `PaymentProcessor` is the context that uses the strategy to process payments.

Also `Dependency Injection` is used to inject the `Payment` dependency into the `PaymentProcessor`, allowing for loose coupling and adherence to the OCP. So it receives the dependency from the outside rather than creating it internally, making it easier to extend and maintain.

`Dependency Inversion Principle` is also present as the `PaymentProcessor` depends on the abstraction (`Payment`) rather than concrete implementations, as high-level modules should not depend on low-level modules, but both should depend on abstractions. This allows for flexibility and extensibility in the design.

Using `Protocol`instead of Inheritance is more _pythonic_ because enforces static type checking (with mypy), has no forced inheritance, better decoupling and follows the duck typing philosophy of Python "If it quacks like a duck, it is a duck".

## Liskov Substitution Principle (LSP)

Subtypes must be substitutable for their base types without altering the correctness of the program. This means that derived classes should be able to replace their base classes without affecting the functionality.

**Bad**:

```python
class NotificationService:
    def send(self, user: str, message: str) -> None:
        print(f"Sending '{message}' to {user}")

class SMSNotificationService(NotificationService):
    def send(self, user: str, message: str) -> None:
        if len(message) > 160:
            raise ValueError("SMS cannot exceed 160 characters")
        print(f"Sending SMS '{message}' to {user}")

# Client code
def notify(service: NotificationService):
    service.send("gabriel", "A" * 500)
```

Here subclass changes the behavior of the base class, only works for short messages, violating LSP. Now client code must check that means substitution is broken.

```python
if isinstance(service, SMSNotificationService): ...
```

**Good**:

```python
from typing import Protocol


class NotificationService(Protocol):
    def send(self, user: str, message: str) -> None:
        ...

class EmailNotificationService:
    def send(self, user: str, message: str) -> None:
        print(f"Sending email '{message}' to {user}")

class SMSNotificationService:
    def send(self, user: str, message: str) -> None:
        if len(message) > 160:
            message = message[:160]  # adapt internally
        print(f"Sending SMS '{message}' to {user}")
```

- The contract stays the same
- No unexpected errors
- Each implementation handles its own constraints internally, so client code can use any notification service without worrying about specific limitations.

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

class PayPalProcessor:          # PayPal supports everything
    def charge(self, amount: float) -> Receipt: ...
    def refund(self, receipt: Receipt) -> None: ...
    def save_card(self, card: CardDetails) -> Token: ...
    def get_installments(self, amount: float) -> list[Installment]: ...

# ---

class BoletoProcessor:          # Boleto has no card vault or installments natively
    def charge(self, amount: float) -> Receipt: ...
    def refund(self, receipt: Receipt) -> None: raise NotImplementedError
    def save_card(self, card: CardDetails) -> Token: raise NotImplementedError
    def get_installments(self, amount: float) -> list[Installment]: raise NotImplementedError

# ---

class PixProcessor:             # Pix is instant payment only
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

class BoletoProcessor(Chargeable):         # Boleto is charge-only, no refund or vault
    def charge(self, amount: float) -> Receipt: ...

# ---

class PixProcessor(Chargeable, Refundable):  # Pix supports refund, but no cards or installments
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
