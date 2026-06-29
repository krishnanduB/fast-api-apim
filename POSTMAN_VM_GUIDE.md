# Accessing the FastAPI App on a Cloud VM using Postman

When your FastAPI application is hosted on a Cloud VM, you can test the endpoints from your local machine using Postman by replacing `localhost` or `127.0.0.1` with the public IP address of your VM.

**VM Public IP:** `52.188.106.168`
**Default Port:** `8000`

## Important Prerequisites

Before you can access the application from the outside, you need to ensure two things:

1.  **Application Binding**: When starting the FastAPI server on the VM, you must bind it to all network interfaces (`0.0.0.0`) rather than just localhost. 
    You can do this by running:
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```
    *(If you are using the `start.bat` script, you may want to modify it to include `--host 0.0.0.0`)*

2.  **Firewall/Network Security Group**: Ensure that port `8000` is open for inbound TCP traffic in your cloud provider's firewall settings (e.g., Azure NSG, AWS Security Groups).
    Additionally, you must open the port in the Windows Firewall on the VM itself. Run the following command in **Windows PowerShell (as Administrator)**:
    ```powershell
    New-NetFirewallRule `
      -DisplayName "Allow FastAPI Port 8000" `
      -Direction Inbound `
      -Protocol TCP `
      -LocalPort 8000 `
      -Action Allow
    ```

    **Understanding the Network Flow (Why this is needed):**
    ```text
    Postman/Laptop
       ↓
    Azure Public IP
       ↓
    Azure NSG allowed port 8000
       ↓
    Windows VM reached
       ↓
    Windows Firewall blocked port 8000
    ```

---

## Postman Testing Instructions

To test your application remotely, configure your Postman requests with the following URLs:

### 1. Root Endpoint (GET)
- **Method:** `GET`
- **URL:** `http://52.188.106.168:8000/`
- **Description:** Verifies the app is running and reachable.

### 2. Read Item (GET)
- **Method:** `GET`
- **URL:** `http://52.188.106.168:8000/items/1?q=test`
- **Description:** Retrieves an item by its ID.

### 3. Create Item (POST)
- **Method:** `POST`
- **URL:** `http://52.188.106.168:8000/items/`
- **Body:** Under the Body tab, select **raw** and choose **JSON** format.
  ```json
  {
      "name": "Laptop",
      "description": "A high performance laptop",
      "price": 1500.00,
      "tax": 150.00
  }
  ```

### 4. Partially Update Item (PATCH)
- **Method:** `PATCH`
- **URL:** `http://52.188.106.168:8000/items/1`
- **Body:** Under the Body tab, select **raw** and choose **JSON** format.
  ```json
  {
      "price": 1800.00
  }
  ```

### 5. Update Item (PUT)
- **Method:** `PUT`
- **URL:** `http://52.188.106.168:8000/items/1`
- **Body:** Under the Body tab, select **raw** and choose **JSON** format.
  ```json
  {
      "name": "Gaming Laptop",
      "description": "Updated description",
      "price": 2000.00,
      "tax": 200.00
  }
  ```

### 6. Delete Item (DELETE)
- **Method:** `DELETE`
- **URL:** `http://52.188.106.168:8000/items/1`
- **Description:** Deletes an item by its ID.

### 7. Create User (POST)
- **Method:** `POST`
- **URL:** `http://52.188.106.168:8000/users/`
- **Body:** Under the Body tab, select **raw** and choose **JSON** format.
  ```json
  {
      "username": "johndoe",
      "email": "john@example.com",
      "full_name": "John Doe",
      "disabled": false
  }
  ```

### 8. Read User (GET)
- **Method:** `GET`
- **URL:** `http://52.188.106.168:8000/users/1`
- **Description:** Retrieves a user by their ID.

### 9. Update User (PUT)
- **Method:** `PUT`
- **URL:** `http://52.188.106.168:8000/users/1`
- **Body:** Under the Body tab, select **raw** and choose **JSON** format.
  ```json
  {
      "username": "johndoe_updated",
      "email": "john.updated@example.com",
      "full_name": "John Doe Updated",
      "disabled": true
  }
  ```

### 10. Delete User (DELETE)
- **Method:** `DELETE`
- **URL:** `http://52.188.106.168:8000/users/1`
- **Description:** Deletes a user by their ID.

> **Tip:** You can also access the live Swagger UI documentation by navigating to `http://52.188.106.168:8000/docs` in your web browser.
