# 🔒 Privacy Protection Suite

A comprehensive privacy vulnerability assessment platform that analyzes browser security, system configurations, and potential privacy risks. Automatically sends detailed security reports to Discord for analysis and monitoring.

## ⚠️ Important Legal Notice

This platform is designed for educational and research purposes. Please ensure you comply with:
- GDPR and other privacy regulations
- Website Terms of Service
- Local data protection laws
- Obtain proper consent from users before collecting data

## 🚀 Features

### Data Collection
- **IP Address Tracking**: Captures both original and hashed IP addresses
- **Hardware Fingerprinting**: Generates unique hardware IDs based on system information
- **Browser Fingerprinting**: Canvas, WebGL, and system fingerprints
- **System Information**: OS, browser, screen resolution, timezone
- **Performance Metrics**: Page load times, navigation data
- **User Interaction**: Mouse position, scroll position, viewport data
- **Network Information**: Connection type, speed, RTT when available

### Analytics Dashboard
- **Real-time Statistics**: Total visitors, unique IPs, daily visits
- **Interactive Charts**: Browser distribution, OS breakdown, daily trends
- **Detailed Logs**: Comprehensive visitor data table
- **Export Functionality**: Download data as JSON
- **Auto-refresh**: Real-time updates every 30 seconds

### Multiple Collection Methods
1. **Web Interface**: Automatic collection when users visit the site
2. **Embeddable Script**: JavaScript snippet for external websites
3. **Python Client**: Standalone script for programmatic data collection

## 📋 Installation

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Setup

1. **Clone or download the project files**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
python app.py
```

4. **Access the platform:**
- Main page: http://localhost:5000
- Dashboard: http://localhost:5000/dashboard
- API: http://localhost:5000/api/stats

## 🖥️ Usage

### 1. Web Interface

Simply visit `http://localhost:5000` and the system will automatically collect data from your browser.

### 2. Embeddable Script

Include this in any website to collect analytics:

```html
<!-- Include the analytics script -->
<script src="http://localhost:5000/static/embed.js"></script>

<!-- Initialize with your configuration -->
<script>
AnalyticsCollector.init({
    server: 'http://localhost:5000',
    auto: true,           // Automatically collect data
    interval: 30000,      // Collect data every 30 seconds
    debug: true          // Enable console logging
});
</script>
```

### 3. Python Data Collector

Use the standalone Python script:

```bash
# Single data collection
python data_collector.py --server http://localhost:5000

# Continuous collection every 60 seconds
python data_collector.py --server http://localhost:5000 --interval 60

# Include additional custom data
python data_collector.py --data '{"custom_field": "value", "user_id": 123}'
```

## 📊 Data Structure

The platform collects the following data points:

### Browser Information
- User agent string
- Browser name and version
- Platform information
- Language settings
- Cookie support status

### System Information
- Operating system
- Screen resolution and color depth
- Timezone and locale
- Hardware concurrency
- Available memory

### Network Data
- IP address (original and hashed)
- Connection type and speed
- Round-trip time (RTT)
- Referrer information

### Fingerprinting
- Canvas fingerprint
- WebGL fingerprint
- Combined browser fingerprint
- Hardware ID (HWID)

### Performance Metrics
- Page load times
- DOM ready time
- Navigation type
- Mouse and scroll positions

## 🔧 API Endpoints

### Data Collection
- **POST /collect**: Submit analytics data
- **GET /api/stats**: Retrieve aggregated statistics
- **GET /export**: Export all data as JSON

### Web Interface
- **GET /**: Main landing page with auto-collection
- **GET /dashboard**: Analytics dashboard with charts and tables

## 🛡️ Privacy Considerations

### Data Protection Features
- IP address hashing for anonymization
- Session-based tracking (not persistent)
- No storage of personally identifiable information
- Configurable data retention policies

### Compliance Recommendations
1. **Add Privacy Policy**: Clearly state what data you collect
2. **Obtain Consent**: Use cookie banners or consent forms
3. **Data Minimization**: Only collect necessary data
4. **Secure Storage**: Implement proper database security
5. **Right to Deletion**: Provide data deletion mechanisms

## 🔧 Configuration

### Environment Variables
```bash
export FLASK_ENV=production
export SECRET_KEY=your-secret-key-here
export DATABASE_URL=sqlite:///data_logs.db
```

### Custom Configuration
Edit `app.py` to modify:
- Database connection settings
- Data retention policies
- Rate limiting
- CORS settings

## 📁 File Structure

```
analytics-platform/
├── app.py                 # Main Flask application
├── data_collector.py      # Standalone Python collector
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   ├── index.html        # Main landing page
│   └── dashboard.html    # Analytics dashboard
├── static/
│   └── embed.js         # Embeddable JavaScript
└── data_logs.db         # SQLite database (created automatically)
```

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
```bash
# Using Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Using Docker (create Dockerfile)
docker build -t analytics-platform .
docker run -p 5000:5000 analytics-platform
```

## 📈 Analytics Dashboard Features

### Statistics Cards
- Total visitors count
- Unique IP addresses
- Today's visits
- Average daily visits

### Interactive Charts
- Browser distribution (doughnut chart)
- Operating system breakdown (doughnut chart)
- Daily visits trend (line chart)

### Data Table
- Recent visitor logs
- Filterable and sortable columns
- Real-time updates
- Export functionality

## 🔒 Security Features

- Input validation and sanitization
- SQL injection prevention
- Rate limiting capabilities
- CORS configuration
- Secure session handling

## 🤝 Contributing

This is an educational project. Feel free to:
- Report bugs or issues
- Suggest new features
- Submit improvements
- Add documentation

## ⚖️ Legal Disclaimer

This software is provided for educational purposes only. Users are responsible for:
- Complying with applicable laws and regulations
- Obtaining proper consent before collecting personal data
- Implementing appropriate security measures
- Respecting user privacy and data protection rights

## 📝 License

This project is for educational use. Please ensure compliance with local laws and regulations when implementing data collection systems.

---

**Remember**: Always prioritize user privacy and comply with data protection regulations in your jurisdiction.