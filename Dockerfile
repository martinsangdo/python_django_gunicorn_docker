# --- Base Stage: Install build dependencies ---
    FROM python:3.11-slim-buster AS builder

    WORKDIR /app
    
    # Install system-level dependencies for psycopg2 (PostgreSQL) or other database adapters
    RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
        python3-dev \
        libpq-dev \
        # Add other necessary build dependencies here
        && rm -rf /var/lib/apt/lists/*
    
    # Install Python dependencies
    COPY requirements.txt .

    RUN pip install --upgrade pip
    RUN pip install --no-cache-dir -r requirements.txt
    
    # --- Migrate Stage: Run database migrations ---
    FROM builder AS migrator
    
    # Copy application code
    COPY . .
    COPY ./my_app/sales.csv ./app/my_app
    RUN chmod -R a+r ./my_app/sales.csv

    # Run database migrations
    RUN python manage.py migrate --no-input
    
    # Collect static files
    RUN python manage.py collectstatic --no-input
    
    # --- Final Stage: Gunicorn server ---
    FROM python:3.11-slim-buster AS final
    
    WORKDIR /app
    
    # Create a non-root user
    RUN groupadd --system nonroot && useradd --system --gid nonroot --create-home --home /home/nonroot nonroot
    RUN chown -R nonroot:nonroot /home/nonroot
    USER nonroot

    # Copy only the necessary artifacts from the previous stages
    COPY --from=migrator /app/static /app/static --chown=nonroot:nonroot

    COPY --from=migrator /app/my_app/sales.csv /app/my_app/sales.csv --chown=nonroot:nonroot

    COPY --from=migrator /app/manage.py /app/manage.py
    COPY --from=migrator /app/my_app /app/my_app
    COPY --from=migrator /app/requirements.txt /app/requirements.txt

    # Set PYTHONUSERBASE to store gunicorn
    ENV PYTHONUSERBASE=/home/nonroot
    ENV PATH="$PYTHONUSERBASE/bin:${PATH}"

    # Install only runtime dependencies (without build tools)
    RUN pip install --upgrade pip
    RUN pip install --no-cache-dir -r requirements.txt --user   
    
    # Set environment variables (adjust as needed)
    ENV DJANGO_SETTINGS_MODULE=my_app.settings
    ENV PYTHONUNBUFFERED=1
    ENV PORT=8000
    
    # Expose the application port
    EXPOSE $PORT
    
    # Command to run the Gunicorn server
    #RUN ls -l /usr/local/bin/gunicorn
    RUN ls -l /home/nonroot/bin/gunicorn
    CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--threads", "4", "my_app.wsgi"]