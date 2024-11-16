DebManager - Debian Package Installer

DebManager is a desktop application that allows users to easily install .deb package files. Built using PyQt5, this application is designed to run on Debian-based Linux distributions. Users can select and install Debian packages via a graphical interface. It includes a progress bar to display installation progress and provides feedback to the user in case of errors during installation.
Features

    User-Friendly Interface: A simple and intuitive interface that allows users to easily install packages.
    Package Installation Progress: Visual tracking of the installation process via a progress bar.
    Error Feedback: Informative message boxes that notify users of any errors during the installation.
    Root Permission Check: Ensures the application runs with necessary root permissions.
    Fusion Style: A sleek and modern look using the "Fusion" style.

Requirements

    Python 3.x
    PyQt5: Required for the graphical user interface.
    A Debian-based Linux distribution (Ubuntu, Linux Mint, etc.) or any system that supports .deb packages.

Installation

    Clone the repository:

git clone https://github.com/tohan-tr/DebManager

Install the necessary dependencies:

pip install -r requirements.txt

Run the application:

    python start.py

Usage

When the application starts, the user will be presented with an interface to select a .deb file. After selecting a file, the user can initiate the installation process, which will be displayed in the progress bar.
Contributing

This project is open-source and contributions are welcome. Feel free to submit pull requests. If you find any issues, please open a new issue in the repository.
License

This project is licensed under the MIT License.
