# HomeLife

**HomeLife** is a task tracking app designed to streamline family life. It provides shared tools for managing calendars, meal plans, recipes, shopping lists, and tasks, all in one place.

Note: This app is an experiment in using output mainly from GenAI systems to write something non tribial.

---

## Features

- **Shared Calendar**: Plan and manage family events with ease.
- **Meal Planner**: Organize weekly meals and link them with recipes.
- **Recipe Manager**: Store and access your favorite recipes.
- **Shopping Lists**: Auto-generate shopping lists based on meal plans or add items manually.
- **Task Tracker**: Assign and manage household tasks for family members.

---

## Tech Stack

- **Frontend**: React
- **Backend**: Django (Django REST Framework)
- **Database**: PostgreSQL
- **Hosting**: To be determined (e.g., AWS, Heroku, DigitalOcean)

---

## Installation

### Prerequisites
- Python 3.x
- Node.js
- PostgreSQL
- Git
- Conda

### Backend Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/homelife.git
   cd homelife/backend
   ```
2. Create the conda environment:
   ```bash
   conda env create
   conda activate homelife
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create your database:
   ```bash
   ./bin/create-db.sh
   ```
4. Set up the database:
   ```bash
   python manage.py migrate
   ```
5. Run the development server:
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1.  Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm start
   ```

## Usage

1. Navigate to the frontend URL (usually http://localhost:3000).
2. Access API endpoints through the backend server (http://127.0.0.1:8000/api/).

## Contributing

Contributions are welcome! Follow these steps:

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your feature description"
   ```
4. Push to your forked repository:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a pull request.

## License
This project is licensed under the MIT License.

## Contact
For questions or suggestions, feel free to create an issue on the github tracker.

