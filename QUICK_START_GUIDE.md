# TravelGo 2.0 - Quick Start & Deployment Guide

## 🚀 Quick Start (Development)

### Prerequisites
- Python 3.8+
- Git
- pip/virtualenv

### 1. Clone & Setup
```bash
# Clone repository
git clone <repo-url>
cd TravelGo

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 2. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
# Set FLASK_ENV=development for local testing
```

### 4. Run Application
```bash
python app.py
```

Application will be available at: `http://localhost:5000`

## 🌐 Application URLs

| Page | URL |
|------|-----|
| 🏠 Home | http://localhost:5000/ |
| 🔑 Login | http://localhost:5000/login |
| 📝 Register | http://localhost:5000/register |
| 🔍 Search | http://localhost:5000/search |
| 📊 Dashboard | http://localhost:5000/dashboard |
| 🛡️ Admin | http://localhost:5000/admin/dashboard |

## 📋 Test Credentials

### Regular User
- Email: user@example.com
- Password: Password123

### Admin User
- Email: admin@travelgo.com
- Password: Admin@123

## 🏗️ Project Architecture

### Backend Structure
```
backend/
├── app.py                    # Flask entry point
├── config.py                 # Configuration
├── requirements.txt          # Dependencies
├── services/                 # Business logic
│   └── booking_service.py   # Unified booking service
├── validators/              # Input validation
├── decorators/              # Auth decorators
├── routes/                  # API endpoints
│   ├── auth.py
│   ├── bookings.py
│   ├── search.py
│   └── admin.py
├── models/                  # Data models
├── aws/                     # AWS integration
└── utils/                   # Utilities
```

### Frontend Structure
```
frontend/
├── static/
│   ├── css/
│   │   ├── style.css        # Main styles (Premium Red & White)
│   │   └── responsive.css
│   └── js/
│       ├── main.js
│       └── api.js
└── templates/
    ├── base.html
    ├── index.html
    ├── login.html
    ├── register.html
    ├── search.html
    ├── dashboard.html
    ├── admin_dashboard.html
    └── booking_confirmation.html
```

## 🔐 Key Features

### 1. Authentication & Security
- Bcrypt password hashing
- Secure session management
- CSRF protection
- Input validation
- Rate limiting

### 2. Booking Management
- Unified booking service for Bus, Train, Flight, Hotel
- Real-time booking status updates
- Cancellation with refund calculation
- Booking history and statistics

### 3. Admin Dashboard
- View all bookings and users
- Manage booking status
- System statistics and analytics
- User administration

### 4. Professional UI
- Premium red & white theme
- Responsive design (mobile-first)
- Smooth animations and transitions
- Accessibility features

## 🛠️ API Reference

### Search Endpoint
```bash
GET /api/search?mode=Flight&from=NYC&to=LAX&date=2024-03-15

Response:
{
  "success": true,
  "count": 3,
  "results": [
    {
      "id": "FL001",
      "name": "Express Air",
      "from": "NYC",
      "to": "LAX",
      "duration": "5h",
      "price": 250,
      "rating": 4.8,
      "departure_time": "10:00 AM"
    }
  ]
}
```

### Create Booking
```bash
POST /api/bookings
Content-Type: application/json

{
  "booking_type": "Flight",
  "from_city": "NYC",
  "to_city": "LAX",
  "travel_date": "2024-03-15",
  "total_price": 250,
  "seats_selected": ["12A", "12B"],
  "passengers": [
    {
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "+1234567890"
    }
  ]
}

Response:
{
  "success": true,
  "booking_id": "BK20240315XXXXX",
  "confirmation_number": "CONF-XXXXX",
  "booking_details": {...}
}
```

### Get User Bookings
```bash
GET /api/bookings

Response:
{
  "success": true,
  "bookings": [
    {
      "booking_id": "BK20240315XXXXX",
      "booking_type": "Flight",
      "status": "Confirmed",
      "from_city": "NYC",
      "to_city": "LAX",
      "travel_date": "2024-03-15",
      "total_price": 250
    }
  ]
}
```

### Cancel Booking
```bash
DELETE /api/bookings/<booking_id>
?reason=personal

Response:
{
  "success": true,
  "message": "Booking cancelled",
  "refund_amount": 250
}
```

## 🚢 Production Deployment

### AWS EC2 Deployment

#### 1. Setup EC2 Instance
```bash
# Connect to EC2 instance
ssh -i your-key.pem ec2-user@your-instance-ip

# Update system
sudo yum update -y
sudo yum install python3 python3-pip git -y
```

#### 2. Setup Application
```bash
# Clone repository
git clone <repo-url>
cd TravelGo/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 3. Configure for Production
```bash
# Copy and edit .env
cp .env.example .env
nano .env

# Set:
FLASK_ENV=production
SECRET_KEY=<strong-random-key>
SESSION_COOKIE_SECURE=True
AWS_ACCESS_KEY_ID=<your-aws-key>
AWS_SECRET_ACCESS_KEY=<your-aws-secret>
```

#### 4. Setup Gunicorn
```bash
# Install Gunicorn
pip install gunicorn

# Create systemd service
sudo nano /etc/systemd/system/travelgo.service
```

```ini
[Unit]
Description=TravelGo Flask Application
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/TravelGo/backend
ExecStart=/home/ec2-user/TravelGo/backend/venv/bin/gunicorn \
    --workers 4 \
    --bind 0.0.0.0:5000 \
    app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable travelgo
sudo systemctl start travelgo
```

#### 5. Setup Nginx Reverse Proxy
```bash
# Install Nginx
sudo yum install nginx -y

# Create Nginx config
sudo nano /etc/nginx/conf.d/travelgo.conf
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /home/ec2-user/TravelGo/frontend/static/;
    }
}
```

```bash
# Start Nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

#### 6. Setup SSL/TLS
```bash
# Install Certbot
sudo yum install certbot python3-certbot-nginx -y

# Obtain certificate
sudo certbot --nginx -d your-domain.com
```

## 🔗 AWS Integration

### DynamoDB Setup
```bash
# Create tables using AWS CLI
aws dynamodb create-table \
  --table-name TravelGo_Users \
  --attribute-definitions AttributeName=email,AttributeType=S \
  --key-schema AttributeName=email,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region us-east-1

aws dynamodb create-table \
  --table-name TravelGo_Bookings \
  --attribute-definitions AttributeName=booking_id,AttributeType=S \
  --key-schema AttributeName=booking_id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region us-east-1
```

### SNS Setup
```bash
# Create SNS topic
aws sns create-topic --name TravelGo_Notifications

# Subscribe email to topic
aws sns subscribe \
  --topic-arn arn:aws:sns:us-east-1:ACCOUNT_ID:TravelGo_Notifications \
  --protocol email \
  --notification-endpoint your-email@example.com
```

## 📊 Monitoring & Logging

### CloudWatch Logs
```bash
# View application logs
aws logs tail /aws/ec2/travelgo --follow
```

### Setup CloudWatch Alarms
```bash
# High error rate alarm
aws cloudwatch put-metric-alarm \
  --alarm-name travelgo-errors \
  --alarm-description "Alert on high error rate" \
  --metric-name Errors \
  --namespace TravelGo \
  --statistic Sum \
  --period 300 \
  --threshold 10 \
  --comparison-operator GreaterThanThreshold
```

## 🐛 Troubleshooting

### Common Issues

**1. Database Connection Error**
```
Error: "Unable to connect to DynamoDB"
Solution: Verify AWS credentials in .env and IAM permissions
```

**2. Session Not Persisting**
```
Error: "User session lost after page refresh"
Solution: Check Flask-Session configuration and disk space
```

**3. Emails Not Sending**
```
Error: "SNS topic not found"
Solution: Verify SNS_TOPIC_ARN in .env and IAM permissions
```

**4. Admin Dashboard 403 Error**
```
Error: "Access Forbidden"
Solution: Check is_admin flag in user session
```

## 📈 Performance Optimization

### Caching
```python
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'redis'})
```

### Database Optimization
- Index frequently queried fields
- Use GSI for email lookups
- Archive old bookings

### Frontend Optimization
- Minify CSS/JS
- Enable gzip compression
- Use CDN for static assets

## 🔄 CI/CD Pipeline

### GitHub Actions Example
```yaml
name: Deploy to AWS

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy
        run: |
          # Deploy script here
          ./scripts/deploy.sh
```

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [AWS Documentation](https://docs.aws.amazon.com/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
- [DynamoDB Best Practices](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html)

## 💼 Support

For production support or custom requirements:
- Email: support@travelgo.com
- Issues: https://github.com/travelgo/issues
- Documentation: https://docs.travelgo.com

---

**TravelGo 2.0 - Production-Ready Travel Booking Platform**
*Built with Flask, AWS, and Modern Best Practices*
