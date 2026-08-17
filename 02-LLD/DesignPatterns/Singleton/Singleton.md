# Singleton Using Connection Pool

## 1. First understand the requirement

Suppose our application uses a database.

Opening a database connection is relatively expensive.

So instead of creating a new connection for every request, we create a **Connection Pool**.

The pool manages multiple reusable database connections:

```text
              Connection Pool
           ┌──────┬──────┬──────┐
           │ Conn1│ Conn2│ Conn3│
           └──────┴──────┴──────┘
```

Different services use this pool.

```text
                Connection Pool
                       │
          ┌────────────┼────────────┐
          ↓            ↓            ↓
     UserService  OrderService  PaymentService
```

---

## 2. Why might we want one Connection Pool?

Imagine every service creates its own pool:

```python
user_pool = ConnectionPool()
order_pool = ConnectionPool()
payment_pool = ConnectionPool()
```

Now we have:

```text
UserService
     ↓
 Connection Pool A
     ├── Connection 1
     ├── Connection 2
     └── Connection 3

OrderService
     ↓
 Connection Pool B
     ├── Connection 4
     ├── Connection 5
     └── Connection 6
```

This could create unnecessary connections and resource usage.

Instead, we may want:

> **One Connection Pool shared by the application process.**

---

## 3. This is where Singleton comes in

The Singleton idea is:

```text
First request for ConnectionPool
             ↓
        Create pool
             ↓
       Store the pool
             ↓
Next request for ConnectionPool
             ↓
       Return same pool
```

So:

```python
pool1 = ConnectionPool.get_instance()
pool2 = ConnectionPool.get_instance()

print(pool1 is pool2)
```

Output:

```text
True
```

Both services get the same pool.

---

## 4. Simple Singleton Implementation

```python
class ConnectionPool:

    _instance = None

    def __new__(cls):

        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):
        if not hasattr(self, "connections"):
            self.connections = [
                "Connection 1",
                "Connection 2",
                "Connection 3"
            ]
```

Now:

```python
pool1 = ConnectionPool()
pool2 = ConnectionPool()

print(pool1 is pool2)
# True
```

There is one `ConnectionPool` object.

But that pool manages **multiple connections**:

```text
              ONE ConnectionPool
                     │
          ┌──────────┼──────────┐
          ↓          ↓          ↓
       Conn 1     Conn 2     Conn 3
```

This is the important distinction.

> **Singleton controls the number of pool objects. The pool controls the number of database connections.**

---

## 5. How Services Use It

Suppose we have:

```python
class UserService:

    def __init__(self, pool):
        self.pool = pool

    def get_user(self):
        connection = self.pool.get_connection()
        # execute query
        self.pool.release(connection)
```

And:

```python
class OrderService:

    def __init__(self, pool):
        self.pool = pool
```

At application startup:

```python
pool = ConnectionPool()

user_service = UserService(pool)
order_service = OrderService(pool)
```

Now:

```text
                    Connection Pool
                    /     |      \
                   /      |       \
              Conn 1    Conn 2    Conn 3
                 ↑         ↑
                 │         │
          UserService  OrderService
```

Both services share the **same pool**.

---

## 6. But Do We Actually Need Singleton?

This is the important part for your interview.

We can achieve the same thing without a Singleton:

```python
pool = ConnectionPool()

user_service = UserService(pool)
order_service = OrderService(pool)
payment_service = PaymentService(pool)
```

There is still only **one pool**.

The difference is that **the application controls the lifecycle** instead of the `ConnectionPool` class controlling it.

This is generally cleaner:

```text
Application
     │
     └── creates ONE pool
              │
       ┌──────┼──────┐
       ↓      ↓      ↓
     User   Order  Payment
```

---

## 7. So Why Does Singleton Exist?

Singleton is useful when you want the class itself to enforce:

> **"There can only be one instance of this class."**

But if your application can simply do:

```python
pool = ConnectionPool()
```

once at startup and pass it around, then **Dependency Injection is usually preferable**.

---

## The Interview-Level Understanding

Remember these two layers:

```text
                Application
                     │
                     ↓
             Connection Pool
              /      |      \
             ↓       ↓       ↓
          Conn 1   Conn 2   Conn 3
```

**Connection Pool:**

> Manages multiple reusable database connections.

**Singleton:**

> Ensures there is only one Connection Pool object within the defined scope.

**Dependency Injection:**

> Creates that pool once and passes it to the services that need it.

### Best interview answer

> **A connection pool is a good example where Singleton might be considered because we typically want one shared pool per application process. The pool itself manages multiple database connections. However, in Python I would usually create the pool once at application startup and inject it into my services rather than making the pool a global Singleton. This gives me the same shared-instance behavior while keeping dependencies explicit and making testing easier.**
