#!/bin/bash
# prism_setup.sh
# Detect system architecture and extract the appropriate PRISM archive

# Exit on any error
set -e

# Define the folder and .deb file name
DEB_DIR="/packages"  # folder containing lark
DEB_FILE="python3-lark_1.1.9-1_all.deb"  # Replace with your actual .deb filename


# Detect architecture
ARCH=$(uname -m)

echo "Detected architecture: $ARCH"

# Determine which file to extract
if [[ "$ARCH" == "aarch64" ]]; then
    FILE="prism-4.9-linux64-arm.tar.gz"
    FOLDER="prism-4.9-linux64-arm"
elif [[ "$ARCH" == "x86_64" ]]; then
    FILE="prism-4.9-linux64-x86.tar.gz"
    FOLDER="prism-4.9-linux64-x86"
else
    echo "Unsupported architecture: $ARCH"
    echo "Please install Prism following the instructions in README.md"
    exit 1
fi

# Check if the file exists
if [[ ! -f "prism-bins/$FILE" ]]; then
    echo "Error: $FILE not found in the current directory."
    exit 1
fi

# check sudo mode
if [[ "$EUID" -ne 0 ]]; then
    echo "This script must be run as root (use: sudo $0)"
    exit 1
fi

# if the folder prism does exist then it delete the folder
if [ -d "prism" ]; then
    echo "Folder 'prism' exists. Deleting..."
    rm -rf "prism"
    echo "Folder 'prism' has been deleted."
fi

# Extract the corresponding file
echo "Extracting $FILE ..."
tar -xzf "prism-bins/$FILE"

#moving the file to prism folder
mv "$FOLDER" "prism"

#execute install for prism
cd prism
source install.sh
cd ..

# install lark
# Function to check if lark is installed
is_lark_installed() {
    dpkg -s lark &>/dev/null
}

echo "Checking if 'lark' is installed..."

if is_lark_installed; then
    echo "'lark' is already installed."
else
    echo "'lark' is not installed. Installing from .deb package..."

    if [[ ! -f "$DEB_DIR/$DEB_FILE" ]]; then
       echo "Error: $DEB_FILE not found in $DEB_DIR"
       exit 1
    fi

    # Install the .deb package
    dpkg -i "$DEB_DIR/$DEB_FILE"

    # Fix missing dependencies, if any
    apt-get install -f -y

    echo "'lark' has been installed successfully."
fi

echo "Installation complete!"

