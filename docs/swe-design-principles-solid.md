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

Clients should not be forced to depend on interfaces they do not use. This means that it's better to have many specific interfaces rather than a single general-purpose interface.

**Bad**:

```python
class Vehicle:
    def drive(self): ...
    def fly(self): ...

class Car(Vehicle):
    def drive(self): ...
    def fly(self):

class Airplane(Vehicle):
    def drive(self):
    def fly(self): ...
```

Here `Car` is forced to implement `fly` which it cannot do, and `Airplane` is forced to implement `drive` which it cannot do. This creates a bloated interface and violates ISP.

**Good**:

```python
from typing import Protocol

class Drivable(Protocol):
    def drive(self) -> None:
        ...

class Flyable(Protocol):
    def fly(self) -> None:

class Car(Drivable):
    def drive(self) -> None: ...

class Airplane(Flyable):
    def fly(self) -> None: ...
```

Now we have two separate interfaces, `Drivable` and `Flyable`, and each class implements only the interface relevant to its behavior, adhering to the Interface Segregation Principle.

## Dependency Inversion Principle (DIP)

High-level modules should not depend on low-level modules. Both should depend on abstractions. This means that we should depend on interfaces or abstract classes rather than concrete implementations.

**Bad**:

```python
class MySQLDatabase:
    def connect(self): ...

class UserRepository:
    def __init__(self):
        self.db = MySQLDatabase()  # tight coupling
    def get_user(self, user_id): ...
```

Here `UserRepository` is tightly coupled to `MySQLDatabase`, making it hard to change the database implementation without modifying `UserRepository`.

**Good**:

```python
from typing import Protocol

class Database(Protocol):
    def connect(self) -> None:
        ...

class MySQLDatabase:
    def connect(self) -> None: ...

class UserRepository:
    def __init__(self, db: Database):
        self.db = db  # depends on abstraction
    def get_user(self, user_id): ...
```

- You can inject any database
- You can mock easily
- You can switch implementation
