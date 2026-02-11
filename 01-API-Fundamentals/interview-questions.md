
# Interview Questions - API Fundamentals

## Basic Questions

### 1. What is an API?
**Answer:** An API (Application Programming Interface) is a set of rules and protocols that allows different software applications to communicate with each other. It defines the methods and data formats that applications can use to request and exchange information.

**Follow-up:** Can you give a real-world example?
**Answer:** When you use a weather app on your phone, the app uses a weather service API to fetch forecast data. The app sends a request to the weather service's API, and the API returns weather data in a structured format (usually JSON).

---

### 2. What does REST stand for?
**Answer:** REST stands for Representational State Transfer. It's an architectural style for designing networked applications that rely on stateless, client-server communication using standard HTTP methods.

---

### 3. What are the main HTTP methods used in RESTful APIs?
**Answer:** The main HTTP methods are:
- **GET**: Retrieve data from the server (Read)
- **POST**: Send data to create a new resource (Create)
- **PUT**: Update an existing resource entirely (Update/Replace)
- **PATCH**: Partially update a resource (Partial Update)
- **DELETE**: Remove a resource from the server (Delete)

---

### 4. What is the difference between PUT and PATCH?
**Answer:** 
- **PUT**: Replaces the entire resource with the new data provided. You must send the complete representation of the resource.
- **PATCH**: Only updates the specified fields, leaving other fields unchanged. You send only the fields you want to modify.

**Example:**
```
Original: {"name": "John", "age": 30, "email": "john@example.com"}

PUT /users/1: {"name": "John Doe", "age": 31, "email": "john@example.com"}
Result: Entire object replaced

PATCH /users/1: {"age": 31}
Result: Only age field updated, name and email remain unchanged
```

---

### 5. What is a REST endpoint?
**Answer:** A REST endpoint is a specific URL where an API can be accessed by a client application. It represents a resource or a collection of resources that can be interacted with using HTTP methods.

**Example:**
- `GET /api/users` - Endpoint to retrieve all users
- `POST /api/users` - Endpoint to create a new user
- `GET /api/users/123` - Endpoint to retrieve user with ID 123

---

## Intermediate Questions

### 6. What are the key principles of REST?
**Answer:** The six key principles of REST are:
1. **Client-Server Architecture**: Separation of concerns between UI and data storage
2. **Statelessness**: Each request contains all necessary information
3. **Cacheability**: Responses define themselves as cacheable or not
4. **Uniform Interface**: Consistent way of interacting with resources
5. **Layered System**: Client doesn't know if connected directly to end server
6. **Code on Demand** (optional): Server can send executable code to client

### 7. What does "stateless" mean in REST?
**Answer:** Statelessness means that each request from a client to the server must contain all the information needed to understand and process the request. The server doesn't store any client context or session information between requests.

**Benefits:** Better scalability, improved reliability, easier load balancing
**Trade-off:** Larger request payloads

### 8. What are common HTTP status codes?
**Answer:**
- **2xx Success**: 200 OK, 201 Created, 204 No Content
- **3xx Redirection**: 301 Moved Permanently, 304 Not Modified  
- **4xx Client Error**: 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found
- **5xx Server Error**: 500 Internal Server Error, 503 Service Unavailable

### 9. Difference between 401 and 403?
**Answer:**
- **401 Unauthorized**: User hasn't authenticated. Solution: Log in
- **403 Forbidden**: User is authenticated but lacks permission. Solution: Request access

### 10. What is idempotency?
**Answer:** An operation that produces the same result no matter how many times it's executed.
**Idempotent**: GET, PUT, DELETE, HEAD, OPTIONS
**Non-idempotent**: POST

---

## Advanced Questions

### 11. Why is POST not idempotent?
**Answer:** POST creates a new resource each time. Multiple identical POST requests create multiple distinct resources with different IDs.

### 12. What is HATEOAS?
**Answer:** Hypermedia As The Engine Of Application State - API responses include hypermedia links allowing clients to navigate the API dynamically.

### 13. REST vs SOAP?
**Answer:**
- REST: Lightweight, uses HTTP methods, supports multiple formats (JSON/XML)
- SOAP: Heavy, uses only POST and XML, has built-in security standards

### 14. What is content negotiation?
**Answer:** Process where client and server agree on data format using Accept headers (e.g., application/json, application/xml).

### 15. How to version a REST API?
**Answer:**
- URL versioning: /api/v1/users (most common)
- Header versioning: Accept: application/vnd.api.v1+json  
- Query parameter: /api/users?version=1

---

## Scenario Questions

### 16. When to use PUT vs POST?
**POST**: Creating resources (server assigns ID), non-idempotent
**PUT**: Updating entire resource, idempotent

### 17. Design endpoint for searching users?
**Answer:** `GET /api/users?name=John&age=25&role=admin&sort=created_at:desc&page=1&limit=20`

### 18. Status code for successful creation?
**Answer:** 201 Created with Location header pointing to new resource

### 19. How to handle pagination?
**Answer:** 
- Offset-based: ?page=2&limit=10
- Cursor-based: ?cursor=abc123&limit=10

### 20. Best way to handle errors?
**Answer:** Return appropriate HTTP status codes with consistent error response structure including error code, message, timestamp, and details.
