# An application under the web framework Django + Gunicorn + Docker
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
    
