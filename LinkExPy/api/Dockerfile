FROM       python:3
LABEL      maintainer="Sawood Alam <@ibnesayeed>"

ENV        REDIS_URL="redis://localhost:6379"

WORKDIR    /app
COPY       requirements.txt /app/
RUN        pip install -r requirements.txt

COPY       *.py /app/
## Normalize line endings to LF to avoid CRLF/shebang issues when files are
## copied from a Windows host. This uses sed to strip trailing CR (\r) bytes.
RUN        sed -i 's/\r$//' /app/*.py || true

RUN        chmod a+x *.py

# Run the script with the Python interpreter directly to avoid relying on the
# script shebang (this prevents failures if the file has Windows CRLF line
# endings which make the shebang appear as 'python\r' inside the container).
CMD        ["python", "main.py"]
