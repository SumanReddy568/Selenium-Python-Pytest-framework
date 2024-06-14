# Use the official Python 3.9 slim image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install necessary dependencies
RUN apt-get update \
    && apt-get install -y \
        wget \
        bzip2 \
        unzip \
        xvfb \
        libasound2 \
        libgtk-3-0 \
        vim \
        nano \
        curl \
        fonts-liberation \
        libgbm1 \
        libnspr4 \
        libnss3 \
        libu2f-udev \
        libvulkan1 \
        xdg-utils \
        apt-transport-https \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Download Google Chrome Stable
RUN wget -O chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i chrome.deb \
    && apt-get install -f \
    && rm chrome.deb

# Check Chrome version and store it in a variable
RUN chrome_version=$(google-chrome --version | awk '{print $3}' | cut -d '.' -f 1-3) \
    && echo "Chrome version: $chrome_version"

# Download Chromedriver corresponding to the Chrome version
RUN wget -O chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/126.0.6478.55/linux64/chromedriver-linux64.zip \
    && unzip chromedriver.zip -d /opt/ \
    && rm chromedriver.zip
    
# Set Chromedriver path
ENV PATH="/usr/local/bin:${PATH}"

# Set the DISPLAY environment variable
ENV DISPLAY=:99

# Copy all the files from the current directory into the container
COPY . .

# Install Python dependencies from requirements.txt in the current directory
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt



