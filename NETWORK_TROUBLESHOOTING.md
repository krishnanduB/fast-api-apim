# FastAPI Network Troubleshooting Guide

This guide explains how to troubleshoot networking and connectivity issues when deploying your FastAPI application to a remote server (like an Azure Virtual Machine).

If you are running your application on a remote server but getting a **"Request Timeout"** or **"Site cannot be reached"** error when trying to access it via its Public IP address, check the following two main causes:

## 1. The Uvicorn Host Binding (`0.0.0.0` vs `127.0.0.1`)

The most common reason a web server cannot be reached from the outside world is because it is only listening to itself. 

When you run Uvicorn, you tell it what IP address to "bind" (listen) to.

### The Default Behavior (Localhost Only)
If you run Uvicorn without specifying a host (which is what `start.bat` does by default):
```cmd
uvicorn main:app --port 8000
```
Uvicorn defaults to listening on `127.0.0.1` (also known as `localhost`). 
* **What this means:** The server will **only** accept network requests that originate from inside the server itself. 
* **Result:** You can test it from a browser inside the VM, but if you try to hit the public IP from your home computer, Uvicorn will completely ignore the request.

### The Public Behavior (`0.0.0.0`)
To make your application accessible from the internet, you must explicitly tell Uvicorn to listen on **all** available network interfaces using the `--host 0.0.0.0` flag:
```cmd
uvicorn main:app --host 0.0.0.0 --port 8000
```
* **What this means:** `0.0.0.0` is a special IP address that means "listen everywhere." Uvicorn will now accept traffic coming through your server's local network and its Public IP address.

> **Fix:** If you are using `start.bat`, edit the file and ensure the Uvicorn command includes `--host 0.0.0.0`.

---

## 2. Firewalls Blocking Port 8000

Even if Uvicorn is properly bound to `0.0.0.0`, your server's firewalls will block incoming web traffic by default. If you are using an Azure Windows VM, you have **two** firewalls to configure.

### A. Azure Network Security Group (NSG)
Azure places a cloud-level firewall in front of your Virtual Machine. By default, it blocks all inbound traffic except for management ports (like RDP/3389).

**How to allow Port 8000 in Azure:**
1. Log into the **Azure Portal**.
2. Navigate to your Virtual Machine.
3. Click on **Networking** (under the Settings menu).
4. Look at your **Inbound port rules**.
5. Click **Add inbound port rule** and fill it out:
   * **Source:** Any
   * **Source port ranges:** `*`
   * **Destination:** Any
   * **Destination port ranges:** `8000`
   * **Protocol:** TCP
   * **Action:** Allow
   * **Name:** Allow-FastAPI-8000
6. Click **Add** and wait for the rule to apply.

*(Note: If you use Terraform to manage Azure, you must add an `azurerm_network_security_rule` to your Terraform scripts so this port remains permanently open!)*

### B. Windows Defender Firewall
Even if traffic makes it past the Azure NSG, the Windows operating system inside the VM has its own firewall that will block port 8000.

**How to allow Port 8000 in Windows:**
1. Connect to your VM via RDP (Remote Desktop).
2. Open the Start Menu, search for and open **Windows Defender Firewall with Advanced Security**.
3. On the left panel, click on **Inbound Rules**.
4. On the right panel, click **New Rule...**
5. Select **Port** and click Next.
6. Select **TCP** and type `8000` into **Specific local ports**, then click Next.
7. Select **Allow the connection** and click Next.
8. Leave Domain, Private, and Public checked and click Next.
9. Name the rule (e.g., `FastAPI Port 8000`) and click Finish.

### Summary
For your FastAPI application to be reachable via the internet, you must have all three of these aligned:
1. Uvicorn must be running with `--host 0.0.0.0`.
2. The Azure NSG must allow inbound TCP traffic on your port.
3. The Windows Firewall must allow inbound TCP traffic on your port.
