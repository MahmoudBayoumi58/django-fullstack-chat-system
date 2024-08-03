
# Django Full-Stack Chat System

This project is a full-stack chat application that supports real-time messaging, audio and video calling, and user authentication. It is built using Django for both the backend and frontend, leveraging Django templates for rendering the user interface.

## Features

- **Real-Time Chat:** Users can send and receive messages in real-time.
- **Audio and Video Calls:** The app supports both audio and video calling features.
- **User Authentication:** Secure user authentication with registration and login functionality.
- **Responsive Design:** The user interface is designed to be responsive and user-friendly.

## Installation

Follow these steps to set up the project locally.

### Prerequisites

- Python 3.x

### Setup

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/MahmoudBayoumi58/django-fullstack-chat-system.git
    cd django-fullstack-chat-system
    ```

2. **Create a Virtual Environment:**

    ```bash
    python -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts activate`
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Apply Migrations:**

    ```bash
    python manage.py migrate
    ``

5. **Create a Superuser:**

    ```bash
    python manage.py createsuperuser
    ```

6. **Run the Development Server:**

    ```bash
    python manage.py runserver
    ```

## Usage

1. Open your web browser and navigate to \`http://localhost:8000\`.
2. Register a new user or log in with an existing account.
3. Start chatting with other users, and initiate audio or video calls.

## Project Structure

- **chat/**: Contains the Django application files.
- **templates/**: HTML templates for rendering frontend views.
- **static/**: Static files (CSS, JavaScript, images).

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (\`git checkout -b feature/your-feature-name\`).
3. Make your changes.
4. Commit your changes (\`git commit -m 'Add some feature'\`).
5. Push to the branch (\`git push origin feature/your-feature-name\`).
6. Create a pull request.

## Acknowledgements

- Django
- WebRTC
