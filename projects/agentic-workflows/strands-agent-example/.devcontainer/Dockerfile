# Use a lightweight base image
FROM python:3.12-slim

# Set environment to avoid prompts
ENV DEBIAN_FRONTEND=noninteractive

# Root: install OS deps (curl)
# Do this while still root, then clean cache
RUN apt-get update \
 && apt-get install -y --no-install-recommends curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Create a non-root user 'mluser' with UID 1001
RUN groupadd -g 1001 mluser && \
    useradd -m -u 1001 -g mluser -s /bin/bash mluser

# Create working directory and set ownership to mluser
RUN mkdir -p /app && chown -R mluser:mluser /app

# Switch to non-root for app work
USER mluser

# Switch to the working directory
WORKDIR /app

# Switch to the non-root user
USER mluser

# Copy requirements.txt and install dependencies as mluser
COPY --chown=mluser:mluser requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expose any necessary ports (e.g., Ray default)
EXPOSE 6379

# Set default shell
ENTRYPOINT ["/bin/bash"]