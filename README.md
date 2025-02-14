<h1 align="center" style="font-weight: bold;">CRUD using VueJS and Flask 💻</h1>
<h2 align="center" style="font-weight: bold;">and a Python Script to import data to MongoDB from data.json</h2>

<p align="center">
 <a href="#technologies">Technologies</a> • 
 <a href="#backend">Back-end</a> • 
 <a href="#routes">API Endpoints</a> • 
 <a href="#frontend">Front-end</a> 
</p>

<h2 id="technologies">💻 Technologies</h2>

- Python
- Flask
- MongoDB
- Vue
- Vuetify

<h2 id="backend">🚀 Back-end</h2>

<1. Clone the repository (if you haven't already):
```bash
git clone https://github.com/tiagomaciels/crud-python-vue.git
cd crud-python-vue
```

2. Create and activate a virtual environment:
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

4. Make sure MongoDB is running locally on port 27017 (default port)

5. Start the Flask application:
```bash
# From the backend directory
python run.py
```

<h2 id="routes">📍 API Endpoints</h2>

The backend server will start running at `http://localhost:5000`

You can test the API endpoints using tools like Postman or curl:

```bash
# Test the GET users endpoint
curl http://localhost:5000/api/users

# Test the GET user by id endpoint
curl http://localhost:5000/api/users/$id

# Test the POST user endpoint
curl http://localhost:5000/api/users

# Test the PUT user by id endpoint
curl http://localhost:5000/api/users/$id

# Test the DEL user by id endpoint
curl http://localhost:5000/api/users/$id
```


### Environment Configuration

Create a `.env` file in the backend directory with the following variables:
```env
FLASK_APP=run.py
FLASK_ENV=development
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DB=crud_db
```

<h2 id="frontend">🚀 Front-end</h2>
1. Navigate to the frontend directory:

```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run serve
```

The application will be available at `http://localhost:8080`

### Dependencies

- Vue.js 3.2.13
- Vuetify 3.7.12 - UI component framework
- Vue Router 4.5.0 - Routing
- Axios 1.7.9 - HTTP client
- Material Design Icons 7.4.47
