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
