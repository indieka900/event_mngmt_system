### Django Management System

This is a Django-based management system for handling events, including features like pagination and custom utilities.

### Custom Pagination

The `CustomPagination` class extends Django's `PageNumberPagination` to provide a default page size of 3, allowing for easy navigation through paginated data. The class also supports a query parameter for dynamic page sizes and limits the maximum page size to 50.

# How to Use

clone the repository and install the required dependencies. You can then use the `CustomPagination` class in your views to paginate querysets effectively.

# Installation

1. Clone the repository:

   ```bash
   git clone    <repository-url>
   ```  

2. Navigate to the project directory:

   ```bash
    cd event_mngmt_system
    ```

3. Install the required packages:

   ```bash
    pip install -r requirements.txt
    ```

4. Apply migrations:

   ```bash
    python manage.py migrate
    ```

5. Run the server:

   ```bash
    python manage.py runserver
    ```
