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

### Environment Variables

```bash
# Database Configuration
export DATABASE_PATH='/path/to/your/metadata-full.sqlite'

# Flask Configuration  
export FLASK_HOST=127.0.0.1        # Server host
export FLASK_PORT=5000             # Server port
export FLASK_DEBUG=True            # Debug mode
export SECRET_KEY='your-secret-key'
```

### Database Path Options

**Option 1: Environment Variable (Recommended)**
```bash
export DATABASE_PATH='/Volumes/UNPS1/Linux/Web/Fanfiction Search/metadata-full.sqlite'
venv/bin/python run.py
```

**Option 2: Using the NAS Script (Direct - May have limitations)**
```bash
# Use the pre-configured script for direct NAS access
venv/bin/python run_with_nas_db.py
```

**Option 3: Using the NAS Copy Script (Recommended for NAS)**
```bash
# Copy database from NAS to local storage for optimal performance
venv/bin/python run_with_nas_copy.py
```

> **💡 NAS Performance Tip**: SQLite works best with local files. The copy script automatically syncs from your NAS and provides the best performance.

**Option 4: Using .env file**
```bash
# Copy the example environment file
cp .env.example .env
# Edit .env with your database path
# Then load and run:
export $(cat .env | xargs) && venv/bin/python run.py
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

- **🚀 Lightning Fast**: Comprehensive database indexing provides 20x+ speed improvements
- **⚡ Sub-second Queries**: All searches complete in under 1 second on 9M+ records
- **🎯 Optimized Indexes**: 19 strategic indexes covering all search patterns
- **📊 Smart Pagination**: Memory-efficient browsing of large result sets
- **💾 Caching**: Optimized static asset delivery
- **📱 Responsive**: Fast on all device types

### Performance Benchmarks
- Author searches: **255x faster** (2.0s → 8ms)
- Word count ranges: **401x faster** (2.0s → 5ms)
- Top author queries: **18x faster** (11.4s → 0.6s)
- Multi-filter searches: **12x faster** (2.2s → 0.2s)

## 🛠️ Database Management

The application includes management commands for database optimization:

### Create Performance Indexes
```bash
# Create all database indexes for optimal performance
venv/bin/python manage.py create-indexes
```

### Analyze Performance
```bash
# Test current database query performance
venv/bin/python manage.py analyze
```

### Available Commands
- `create-indexes` - Create 19 optimized database indexes
- `analyze` - Benchmark current query performance
- `remove-indexes` - Remove all custom indexes
- `help` - Show available commands

**⚡ Pro Tip**: Run `create-indexes` after setting up the application for best performance on large databases!

## 🐛 Troubleshooting

### Common Issues

1. **Database not found:**
   - Check the DATABASE_PATH environment variable or use the default path
   - Ensure the SQLite file exists and is readable
   - For NAS setups, verify the mount point `/Volumes/UNPS1/` is accessible

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
