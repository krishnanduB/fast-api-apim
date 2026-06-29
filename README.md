# FastAPI Backend

This is a simple FastAPI application demonstrating basic CRUD operations.

## Running the Application

To run the application locally, you can use Uvicorn. First, make sure you have installed the requirements:

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

By default, the application will run at `http://127.0.0.1:8000`.

## Testing with Postman

You can use Postman to test the API endpoints. Below are the instructions and sample requests for each endpoint.

### 1. Root Endpoint (GET)
- **Method:** `GET`
- **URL:** `http://127.0.0.1:8000/`
- **Description:** Returns a greeting message.
- **Expected Response:**
  ```json
  {
      "message": "Hello World"
  }
  ```

### 2. Read Item (GET)
- **Method:** `GET`
- **URL:** `http://127.0.0.1:8000/items/1?q=test`
- **Description:** Retrieves an item by its ID. You can also pass an optional query parameter `q`.
- **Expected Response:**
  ```json
  {
      "item_id": 1,
      "q": "test"
  }
  ```

### 3. Create Item (POST)
- **Method:** `POST`
- **URL:** `http://127.0.0.1:8000/items/`
- **Description:** Creates a new item.
- **Body:** Under the Body tab, select **raw** and choose **JSON** format.
  ```json
  {
      "name": "Laptop",
      "description": "A high performance laptop",
      "price": 1500.00,
      "tax": 150.00
  }
  ```
- **Expected Response:**
  ```json
  {
      "message": "Item Laptop created successfully",
      "item": {
          "name": "Laptop",
          "description": "A high performance laptop",
          "price": 1500.0,
          "tax": 150.0
      }
  }
  ```

### 4. Update Item (PUT)
- **Method:** `PUT`
- **URL:** `http://127.0.0.1:8000/items/1`
- **Description:** Updates an existing item.
- **Body:** Under the Body tab, select **raw** and choose **JSON** format.
  ```json
  {
      "name": "Gaming Laptop",
      "description": "Updated description",
      "price": 2000.00,
      "tax": 200.00
  }
  ```
- **Expected Response:**
  ```json
  {
      "message": "Item 1 updated successfully",
      "item_id": 1,
      "item": {
          "name": "Gaming Laptop",
          "description": "Updated description",
          "price": 2000.0,
          "tax": 200.0
      }
  }
  ```

### 5. Partially Update Item (PATCH)
- **Method:** `PATCH`
- **URL:** `http://127.0.0.1:8000/items/1`
- **Description:** Partially updates an existing item.
- **Body:** Under the Body tab, select **raw** and choose **JSON** format.
  ```json
  {
      "price": 1800.00
  }
  ```
- **Expected Response:**
  ```json
  {
      "message": "Item 1 partially updated successfully",
      "item_id": 1,
      "item": {
          "name": null,
          "description": null,
          "price": 1800.0,
          "tax": null
      }
  }
  ```

### 6. Delete Item (DELETE)
- **Method:** `DELETE`
- **URL:** `http://127.0.0.1:8000/items/1`
- **Description:** Deletes an item by its ID.
- **Expected Response:**
  ```json
  {
      "message": "Item 1 deleted successfully",
      "item_id": 1
  }
  ```

> **Tip:** You can also view the automatically generated Swagger UI documentation by navigating to `http://127.0.0.1:8000/docs` in your web browser while the application is running. This provides a great interactive interface for testing your API right in the browser!
