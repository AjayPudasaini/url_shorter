# URL Shortener Using Django

## Setup Instructions

1. **Setup Virtual Environment:**
    - Create a virtual environment using `virtualenv` or `venv`.
    - Example using `venv`:
        ```
        python3 -m venv myenv
        ```

2. **Activate Environment:**
    - Activate the virtual environment.
    - Example:
        - On Windows:
            ```
            myenv\Scripts\activate
            ```
        - On macOS and Linux:
            ```
            source myenv/bin/activate
            ```

3. **Install Requirements:**
    - Install the required packages from the `requirements.txt` file.
    - Example:
        ```
        pip install -r requirements.txt
        ```

4. **Run Local Server:**
    - Start the local development server.
    - Example:
        ```
        python manage.py runserver
        ```

## Usage

- Once the server is running, visit the URL provided by the Django development server to access the URL shortener application.

- Follow the application's interface to shorten URLs, manage short URLs, and utilize any additional features implemented.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- [Django](https://www.djangoproject.com/) for the web framework.
- QR code generation implemented using [qrcode](https://pypi.org/project/qrcode/).
- Bootstrap used for frontend design.
