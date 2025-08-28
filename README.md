# 📚 Fanfiction Explorer

A web application to explore and analyze your fanfiction database with interactive features and beautiful visualizations.

## ✨ Features

- **📊 Dashboard**: Overview statistics with interactive charts
- **🔍 Advanced Search**: Filter stories by title, author, fandom, genre, word count, and more
- **📖 Story Details**: Comprehensive story information with related recommendations
- **📈 Top Lists**: Browse top fandoms, authors, and longest stories
- **🎨 Responsive Design**: Mobile-friendly interface built with Bootstrap 5
- **⚡ Fast Performance**: Optimized database queries with pagination
- **🔄 RESTful API**: JSON endpoints for programmatic access

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ 
- SQLite database file (`metadata-full.sqlite`)

### Installation

1. **Clone/Navigate to the project directory:**
   ```bash
   cd /Users/Azrael/fanfiction-explorer
   ```

2. **Activate the virtual environment:**
   ```bash
   # On macOS/Linux with fish shell:
   source venv/bin/activate.fish
   # Or manually use the python interpreter:
   ./venv/bin/python
   ```

3. **Install dependencies (if not already installed):**
   ```bash
   venv/bin/pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   venv/bin/python run.py
   ```

5. **Open your browser:**
   Navigate to `http://127.0.0.1:5000`

## 📱 Usage

### Dashboard
- View total statistics: stories, authors, words
- Interactive charts showing top fandoms and language distribution
- Quick links to detailed views

### Search
- Use advanced filters to find specific stories
- Filter by title, author, fandom, genre, language, status, rating
- Set word count ranges for precise results
- Pagination for large result sets

### Browse
- Simple browsing of all stories with pagination
- Latest stories shown first
- Quick access to story details

### Story Details
- Complete story metadata and statistics
- Links to original story and author profile
- Related story recommendations

### Top Lists
- Most popular fandoms by story count
- Most prolific authors
- Longest stories by word count

## 🔧 Configuration

The application can be configured via environment variables:

```bash
export FLASK_HOST=127.0.0.1        # Server host
export FLASK_PORT=5000             # Server port
export FLASK_DEBUG=True            # Debug mode
```

### Database Path
Update the database path in `app/__init__.py`:
```python
DATABASE_PATH='/path/to/your/metadata-full.sqlite'
```

## 🛠️ API Endpoints

The application provides RESTful API endpoints:

### Statistics
- `GET /api/stats/basic` - Basic database statistics
- `GET /api/stats/fandoms` - Top fandoms
- `GET /api/stats/authors` - Top authors  
- `GET /api/stats/languages` - Language distribution
- `GET /api/stats/ratings` - Rating distribution

### Data
- `GET /api/search` - Search stories with filters
- `GET /api/story/<id>` - Story details
- `GET /api/top/longest` - Longest stories

### Example API Usage
```bash
# Get basic stats
curl http://localhost:5000/api/stats/basic

# Search for Harry Potter stories
curl "http://localhost:5000/api/search?category=Harry Potter&limit=10"
```

## 📊 Database Schema

The application expects an SQLite database with the following structure:

### metadata_full table
- `Title` - Story title
- `Author` - Author name
- `Category` - Fandom/category
- `Genre` - Story genre
- `Language` - Story language
- `Status` - Completion status
- `Rating` - Content rating
- `word_count` - Word count (integer)
- `chapter_count` - Chapter count (integer)
- `Updated` - Last update date
- `Summary` - Story summary
- `Story URL` - Link to original story
- `Author URL` - Link to author profile

## 🎨 Customization

### Styling
- Modify `app/static/css/style.css` for custom styles
- Uses Bootstrap 5 for responsive design
- Chart.js for interactive visualizations

### Templates
- Templates located in `app/templates/`
- Uses Jinja2 templating
- Responsive design with mobile support

## 📈 Performance

- Database queries are optimized with proper indexing
- Pagination limits memory usage
- Caching headers for static assets
- Responsive design for all device types

## 🐛 Troubleshooting

### Common Issues

1. **Database not found:**
   - Verify the database path in `app/__init__.py`
   - Ensure the SQLite file exists and is readable

2. **Import errors:**
   - Make sure virtual environment is activated
   - Install dependencies with `pip install -r requirements.txt`

3. **Performance issues:**
   - Consider adding database indexes for frequently searched columns
   - Adjust pagination size in search results

### Logging
- Application logs are written to `logs/fanfiction_explorer.log` in production
- Debug information available in development mode

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with Flask and Bootstrap
- Chart.js for data visualization
- SQLite for data storage
- Font Awesome for icons

---

**Enjoy exploring your fanfiction database!** 📚✨
