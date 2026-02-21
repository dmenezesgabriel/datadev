# Design Principles: SOLID

S.O.L.I.D is an acronym for five design principles that help software developers create maintainable, flexible, and scalable software. These principles are widely used in object-oriented programming.

# Single Responsibility Principle (SRP)

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

Now the behavior can be extended by creating new payment classes without modifying existing code. In the example above we use polymorphism to achieve this. The `PaymentProcessor` can process any payment type that implements the `Payment` interface, adhering to the OCP.

Other patterns also present are strategy where `Payment` is the strategy interface and `CreditCardPayment` and `PayPalPayment` are concrete strategies. The `PaymentProcessor` is the context that uses the strategy to process payments.

Also `Dependency Injection` is used to inject the `Payment` dependency into the `PaymentProcessor`, allowing for loose coupling and adherence to the OCP. So it receives the dependency from the outside rather than creating it internally, making it easier to extend and maintain.

`Dependency Inversion Principle` is also present as the `PaymentProcessor` depends on the abstraction (`Payment`) rather than concrete implementations, as high-level modules should not depend on low-level modules, but both should depend on abstractions. This allows for flexibility and extensibility in the design.

Using `Protocol`instead of Inheritance is more _pythonic_ because enforces static type checking (with mypy), has no forced inheritance, better decoupling and follows the duck typing philosophy of Python "If it quacks like a duck, it is a duck".
