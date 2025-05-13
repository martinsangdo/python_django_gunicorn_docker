# An application under the web framework Django + Gunicorn + Docker
1. Build and run the project:<br/>
    ``$python manage.py makemigrations `` <br/>
   ``$python manage.py migrate `` <br/>
   ``$python manage.py runserver `` <br/>
   Then the project will run at the default address: `` http://127.0.0.1:8000 ``<br/><br/>

   Call other APIs as per requirements.<br/><br/>
    1a) Import CSV file (The file "sales.csv" is in the folder "/my_app"):<br/>
        ``
        curl --location 'http://127.0.0.1:8000/api/import-sales'
       ``
       <br/>
       **Response:**
       
        {
            "imported_rows": 1662    #we skipped duplicated rows in the file
        }
   
    1b) Get overall metric:<br/>
        ``curl --location 'http://127.0.0.1:8000/api/metrics/revenue/daily?start=2025-3-5&end=2025-03-9' ``
       <br/>
        **Response:**

        {
            "total_revenue_sgd": 2206.2680000000005,
            "average_order_value_sgd": 31.518114285714294
        }
       
    1c) Get daily metric: <br/>
        ``curl --location 'http://127.0.0.1:8000/api/metrics/revenue/daily?start=2025-3-5&end=2025-03-9'``
        <br/>
        **Response:**
           
        [
            {
                "date": "2025-03-05",
                "revenue_sgd": 408.096
            },
            {
                "date": "2025-03-06",
                "revenue_sgd": 985.7960000000003
            }
       ]
   
    1d) Check service status:
        ``curl --location 'http://127.0.0.1:8000/health'``
       <br/>
       **Response:**
   
       {
            "status": "ok",
            "database": "reachable"
       }
2. Run test:<br/>
    ``python manage.py test``
   
3. Docker build:<br/>
    ``docker build --no-cache -t python_django_gunicorn_docker .``<br/>
    ``docker run -p 8000:8000 python_django_gunicorn_docker``<br/>
    

    
# Documentation
1. High-Level Architecture Diagram<br/>
     * .github/workflows/ci.yml (Contain list of commands once we have new 
     * my_app/
       * controller/
         * main_controller.py (API interface like /health)
         * sale_controller.py (API interface to store CSV data, get metrics)
       * models/
         * product.py (Define database scheme for the table Product to save basic product info)
         * sale.py (Define database scheme for the table Sale to save basic sale info)
       * services/
         * product_service.py (Contains functions like: Store product details into database)
         * sale_service.py (Contains functions like: Import CSV data to database, query metrics)
       * test/
         * tests.py (Unit tests)
       * middleware.py (Define logger format)
       * settings.py (constants, common function, database connector, ...)
       * urls.py  (URL path routers)
       * sales.csv (original file)
     * Dockerfile (Docker settings of the project)
     * requirements.txt (Package names for docker building)
     * .env (NOT in github)
   
2. API & Data Model Sketch
   Product: name, price, created_at, updated_at (we can store extra info like color, price, etc.)
   Sale: date (Sale Date), order_id (Sale ID), product_id (refer to the table Product), amount_sgd (Total Paid w/ Payment Method)
3. Infrastructure Choices
   * For this first assigment, we use SQLite3. Once we have another database service, we can use another engine instead.
   * We store minimum info into tables as requirements
   * We use Pandas for data preprocessing
4. Scaling & Resilience Strategy
   * This relates to DevOps tasks, let's discuss in next meeting
5. CI/CD & Rollback Plan
    * I use default Github workflows to auto build the code once we have new change in the branch "main".
    * Note that I disable building docker in workflow. Let discuss it next meeting
6. Observability & SRE
    * What is this part?
7. Trade-Off Discussion & TODO
   * Store daily revenue into another table for faster query. We don't need to calculate revenue every time becaues: (1) revenue is not likely to change, (2) reduce latency in API.
   * Employ cloud database. At this time, even we build Docker image successfully, the functions won't work because SQLite3 is not connected.
   * Store sale info info multiple tables like Location, Payment method.
    
