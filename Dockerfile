# syntax=docker/dockerfile:1
# Pull base image
FROM python:3.10
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Set work directory
WORKDIR /test_api_gallery
# Install dependencies
COPY poetry.lock pyproject.toml /test_api_gallery/
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root
# Copy project
COPY . /test_api_gallery