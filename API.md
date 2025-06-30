
# 📘 API Documentation

> 🔐 All endpoints marked with 🔐 require JWT Token in the `Authorization` header:  
`Authorization: Bearer <your_token_here>`

---

## 🧑‍💼 User API

### 🔹 `GET /api/users/me/`

- **Description**: Get currently authenticated user’s details.
- **Method**: `GET`
- **Auth**: 🔐 Yes
- **Response**:
```json
{
  "id": 1,
  "email": "johndoe@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "balance": "1000.00"
}
```

---

### 🔹 `PATCH /api/users/update-balance/`

- **Description**: Update the authenticated user’s balance.
- **Method**: `PATCH`
- **Auth**: 🔐 Yes
- **Request Body**:
```json
{
  "balance": 1500.00
}
```
- **Response**:
```json
{
  "balance": "1500.00"
}
```

---

### 🔹 `POST /api/users/`

- **Description**: Register a new user (internal use in ViewSet)
- **Method**: `POST`
- **Request Body**:
```json
{
  "email": "newuser@example.com",
  "password": "your_password",
  "register_flag": true
}
```
- **Response**:
```json
{
  "email": "newuser@example.com",
  "access_token": "xxx",
  "refresh_token": "xxx",
  "message": "User Registered"
}
```

---

### 🔹 `POST /api/login-register/`

- **Description**: Login or register a user using `register_flag`
- **Method**: `POST`
- **Request Body**:
```json
{
  "email": "johndoe@example.com",
  "password": "your_password",
  "register_flag": false
}
```

---

## 💸 Transactions API

### 🔹 `GET /api/transactions/`

- **Description**: Get all transactions of authenticated user
- **Auth**: 🔐 Yes
- **Query Parameters**:
  - `category=food`
  - `date=2025-06-28`
  - Searchable: `user__email`, `category`, `date`, `note`, `type`
  - Ordering: `category`, `date`
- **Response**:
```json
[
  {
    "id": 1,
    "type": "debit",
    "user": 1,
    "amount": "100.00",
    "category": "food",
    "date": "2025-06-28",
    "note": "Dinner",
    "created_at": "2025-06-28T10:00:00Z",
    "updated_at": "2025-06-28T10:00:00Z"
  }
]
```

---

### 🔹 `POST /api/transactions/`

- **Description**: Create a new transaction and update user’s balance.
- **Method**: `POST`
- **Auth**: 🔐 Yes
- **Request Body**:
```json
{
  "type": "debit",
  "amount": 500,
  "category": "food",
  "note": "Dinner with friends",
  "operation": "debited"
}
```
- **Response**:
```json
{
  "message": "New Transaction Added"
}
```
- **Error Response**:
```json
{
  "error": "error: No operation Found, Must Add the Operation To Do"
}
```

---

### 🔹 `PUT/PATCH /api/transactions/<id>/`

- **Description**: Update a transaction by ID
- **Method**: `PUT` / `PATCH`
- **Auth**: 🔐 Yes

---

### 🔹 `DELETE /api/transactions/<id>/`

- **Description**: Delete a transaction
- **Method**: `DELETE`
- **Auth**: 🔐 Yes

---

## ✅ Authorization Header Format (for protected routes)

```
Authorization: Bearer <your-access-token>
```

---

## 📍 Example cURL Request

```bash
curl -X PATCH http://localhost:8000/api/users/update-balance/ \
-H "Authorization: Bearer <token>" \
-H "Content-Type: application/json" \
-d '{"balance": 2000.00}'
```
