FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to the PATH for future steps
ENV PATH="/root/.local/bin:$PATH"

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock ./

# Install the dependencies using Poetry
RUN poetry install --no-root

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Run migrations and start the server
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
