# TravelGo: Cloud-Powered Real-Time Travel Booking Platform

## 📋 Project Overview

**TravelGo** is a comprehensive full-stack travel booking platform that enables users to seamlessly search and book buses, trains, flights, and hotels through a unified web interface. Built with Flask and deployed on AWS, it demonstrates modern cloud architecture with real-time notifications and secure session management.

### Core Features
- 🚌 Multi-mode travel booking (Buses, Trains, Flights, Hotels)
- 👤 Secure user authentication and profile management
- 🔔 Real-time email notifications via AWS SNS
- 📊 Dynamic dashboard with booking history
- 💾 NoSQL database using AWS DynamoDB
- ☁️ Cloud deployment on AWS EC2
- 🎨 Responsive Bootstrap UI

---

## 🏗️ Architecture

### Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend** | HTML5, CSS3, Bootstrap, JavaScript | Responsive web UI |
| **Backend** | Flask (Python) | REST API & business logic |
| **Database** | AWS DynamoDB | NoSQL data persistence |
| **Notifications** | AWS SNS | Email alerts |
| **Hosting** | AWS EC2 | Cloud deployment |
| **Authentication** | Flask Sessions | User session management |
| **Infrastructure** | CloudFormation | IaC automation |

### Database Schema

#### Users Table
```
Partition Key: email
Attributes:
  - user_id: UUID
  - name: String
  - phone: String
  - password_hash: String
  - created_at: Timestamp
  - updated_at: Timestamp
```

#### Bookings Table
```
Partition Key: booking_id
Sort Key: email
Attributes:
  - booking_type: String (Bus/Train/Flight/Hotel)
  - departure_city: String
  - arrival_city: String
  - travel_date: String (ISO-8601)
  - booking_date: Timestamp
  - status: String (Confirmed/Cancelled/Pending)
  - total_price: Float
  - seats_selected: List
  - booking_reference: String
  - created_at: Timestamp
  - updated_at: Timestamp
```

---

## 📁 Project Structure

```
TravelGo/
├── backend/
│   ├── app.py                    # Main Flask application
│   ├── config.py                 # Configuration settings
│   ├── requirements.txt           # Python dependencies
│   ├── .env.example              # Environment template
│   ├── aws/
│   │   ├── __init__.py
│   │   ├── dynamodb.py           # DynamoDB operations
│   │   └── sns.py                # SNS notifications
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py               # Authentication endpoints
│   │   ├── bookings.py           # Booking endpoints
│   │   └── search.py             # Search endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py               # User model
│   │   └── booking.py            # Booking model
│   ├── utils/
│   │   ├── __init__.py
│   │   └── helpers.py            # Utility functions
│   └── templates/                # HTML templates
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   ├── style.css         # Custom styles
│   │   │   └── responsive.css    # Responsive design
│   │   └── js/
│   │       ├── main.js           # Core JavaScript
│   │       └── api.js            # API client
│   ├── templates/                # Flask templates
│   └── listings.json             # Mock travel data
├── infra/
│   ├── cloudformation.yml        # AWS infrastructure
│   └── iam_policy.json           # IAM policy
├── scripts/
│   ├── deploy.sh                 # AWS deployment script
│   └── setup_ec2.sh              # EC2 setup script
├── Dockerfile                     # Docker configuration
├── docker-compose.yml            # Docker Compose setup
└── README.md                     # Documentation
```

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- AWS Account with credentials
- Git (for version control)

### Step 1: Clone Repository

```bash
git clone https://your-repo-url.git
cd TravelGo
```

### Step 2: Set Up Environment

#### Local Development
```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### AWS Configuration
1. Create AWS IAM user with:
   - `AmazonDynamoDBFullAccess`
   - `AmazonSNSFullAccess`

2. Copy `.env.example` to `.env` and fill in your credentials:
```bash
cp .env.example .env
```

3. Update `.env` with your AWS credentials:
```
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1
FLASK_ENV=development
SECRET_KEY=your_secret_key
SNS_TOPIC_ARN=arn:aws:sns:us-east-1:your-account-id:TravelGo_Notifications
```

### Step 3: AWS Infrastructure Setup

#### Using CloudFormation (Recommended)
```bash
# From project root
./scripts/deploy.sh \
  --stack-name travelgo-stack \
  --admin-email your-email@example.com
```

#### Manual Setup
1. Create DynamoDB tables:
   - Users table with email as primary key
   - Bookings table with booking_id as partition key and email as sort key

2. Create SNS Topic:
   - Topic name: `TravelGo_Notifications`
   - Subscribe your email address

3. Create IAM Policy:
   - Attach `iam_policy.json` to your IAM user

### Step 4: Run Application

#### Local Development
```bash
cd backend
python app.py
```

The application will be available at `http://localhost:5000`

#### Using Docker
```bash
# Build and run with Docker Compose
docker-compose up --build
```

---

## 📡 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout
- `GET /auth/profile` - Get user profile
- `PUT /auth/update-profile` - Update profile

### Search
- `GET /api/search?mode=Bus&from=Hyderabad&to=Bangalore&date=2026-03-15` - Search travel options
- `GET /api/destinations` - Get all available destinations
- `GET /api/listings/<mode>` - Get listings by mode

### Bookings
- `POST /api/bookings` - Create booking
- `GET /api/bookings/<booking_id>` - Get booking details
- `GET /api/bookings/my-bookings` - Get user's bookings
- `DELETE /api/bookings/<booking_id>` - Cancel booking
- `PUT /api/bookings/<booking_id>` - Update booking

---

## 🖥️ Pages & Routes

### Frontend Pages
- **Home** (`/`) - Landing page with features overview
- **Register** (`/register`) - User registration form
- **Login** (`/login`) - User login form
- **Search** (`/search`) - Search and book travel options
- **Dashboard** (`/dashboard`) - View all bookings
- **Booking Details** (`/booking/<booking_id>`) - View specific booking

---

## 🔐 Security Features

- **Password Hashing**: Uses Werkzeug security for password hashing
- **Session Management**: Flask session with automatic timeout
- **HTTPS Ready**: Can be deployed with SSL certificates
- **Input Validation**: All inputs validated on backend
- **CSRF Protection**: Ready for implementation
- **IAM Security**: Fine-grained AWS IAM policies

---

## ⚙️ Configuration

### Development vs Production

**Development** (`.env`)
```
FLASK_ENV=development
DEBUG=True
```

**Production** (`.env`)
```
FLASK_ENV=production
DEBUG=False
```

### Environment Variables
- `AWS_ACCESS_KEY_ID` - AWS access key
- `AWS_SECRET_ACCESS_KEY` - AWS secret key
- `AWS_REGION` - AWS region (default: us-east-1)
- `FLASK_ENV` - Flask environment (development/production)
- `SECRET_KEY` - Flask session secret
- `SNS_TOPIC_ARN` - SNS topic ARN
- `USERS_TABLE` - DynamoDB users table name
- `BOOKINGS_TABLE` - DynamoDB bookings table name

---

## 🚢 Deployment

### AWS EC2 Deployment

1. **Launch EC2 Instance**
   - AMI: Ubuntu 20.04 LTS
   - Instance Type: t2.micro (free tier eligible)
   - Security Group: Allow ports 80, 443, 5000

2. **Run Setup Script**
   ```bash
   chmod +x scripts/setup_ec2.sh
   ./scripts/setup_ec2.sh
   ```

3. **Configure Environment**
   ```bash
   nano .env
   # Fill in AWS credentials
   ```

4. **Run Application**
   ```bash
   # Using Gunicorn (recommended)
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

### Docker Deployment

```bash
# Build image
docker build -t travelgo:latest .

# Run container
docker run -p 5000:5000 \
  -e AWS_ACCESS_KEY_ID=your_key \
  -e AWS_SECRET_ACCESS_KEY=your_secret \
  -e AWS_REGION=us-east-1 \
  -e SNS_TOPIC_ARN=your_arn \
  travelgo:latest
```

### Production Considerations

1. **Load Balancer**: Use AWS ALB or NLB
2. **Auto Scaling**: Configure ASG for automatic scaling
3. **RDS**: Consider using RDS for relational data
4. **CloudFront**: Use for static file distribution
5. **WAF**: Implement AWS WAF for security
6. **Monitoring**: Set up CloudWatch monitoring

---

## 📊 Development Timeline

| Phase | Duration | Tasks |
|-------|----------|-------|
| **Phase 1: Infrastructure Setup** | 2 hours | AWS IAM, DynamoDB, SNS, CloudFormation |
| **Phase 2: Backend Development** | 4 hours | Flask, Routes, Models, AWS Integration |
| **Phase 3: Frontend Development** | 3 hours | Templates, CSS, JavaScript, API Client |
| **Phase 4: Testing & Deployment** | 3 hours | Unit tests, EC2 setup, Production config |
| **Total** | **12 hours** | Full production-ready deployment |

---

## 🧪 Testing

### Manual Testing Checklist

#### Authentication
- [ ] User registration with valid data
- [ ] Registration with duplicate email
- [ ] User login with correct credentials
- [ ] Login with incorrect credentials
- [ ] Session timeout on inactivity
- [ ] Profile update functionality

#### Search & Booking
- [ ] Search with all modes (Bus, Train, Flight, Hotel)
- [ ] Search with invalid parameters
- [ ] Book a travel option
- [ ] Booking confirmation received via email
- [ ] View all bookings in dashboard

#### Booking Management
- [ ] View booking details
- [ ] Cancel booking
- [ ] Cancellation email received
- [ ] Cannot cancel already cancelled bookings

---

## 📝 Mock Data

The application includes mock travel data in `frontend/listings.json`:

- **Buses**: Routes between major Indian cities (45-50 USD)
- **Trains**: Express trains with competitive pricing (35-60 USD)
- **Flights**: Domestic and international flights (95-150 USD)
- **Hotels**: Premium and budget accommodations (60-120 USD/night)

To use real data, replace the mock data with actual API integrations.

---

## 🔄 Workflow Example

### User Journey: Booking a Bus Ticket

1. User visits homepage
2. Clicks "Get Started" or "Sign In"
3. Registers/Logs in with email
4. Navigates to Search page
5. Selects "Bus" mode
6. Enters departure city (e.g., Hyderabad)
7. Enters destination city (e.g., Bangalore)
8. Selects travel date
9. Views available buses
10. Clicks "Book" on preferred option
11. Booking is confirmed and saved to DynamoDB
12. SNS sends confirmation email with booking reference
13. Booking appears in user's Dashboard
14. User can cancel booking anytime (if status is Confirmed)

---

## 🐛 Troubleshooting

### DynamoDB Connection Issues
```python
# Check DynamoDB connection
python -c "import boto3; print(boto3.resource('dynamodb').tables.all())"
```

### SNS Notification Not Sending
- Verify SNS Topic ARN in `.env`
- Check email subscription is confirmed in SNS console
- Review CloudWatch logs for errors

### Flask Not Starting
```bash
# Check Python version
python --version  # Should be 3.8+

# Check all dependencies installed
pip list | grep flask

# Run with debug
FLASK_ENV=development flask run --host=0.0.0.0 --port=5000
```

### Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>
```

---

## 📚 Learning Resources

- **Flask Documentation**: https://flask.palletsprojects.com/
- **AWS SDK for Python (Boto3)**: https://boto3.amazonaws.com/
- **DynamoDB Best Practices**: https://docs.aws.amazon.com/amazondynamodb/
- **Bootstrap Documentation**: https://getbootstrap.com/docs/5.0/

---

## 📞 Support & Contribution

### Reporting Issues
Create an issue with:
- Detailed description
- Steps to reproduce
- Error messages
- Environment details

### Contributing
1. Fork the repository
2. Create feature branch (`git checkout -b feature/feature-name`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature/feature-name`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License. See LICENSE file for details.

---

## 👥 Team

- **Project Manager**: Gaya
- **Development Team**: Full Stack Development
- **Cloud Architecture**: AWS Solutions

---

## 🎯 Future Enhancements

- [ ] Payment gateway integration (Stripe/PayPal)
- [ ] Real-time flight status updates
- [ ] Loyalty and rewards program
- [ ] Mobile app (React Native/Flutter)
- [ ] Advanced search filters and sorting
- [ ] Reviews and ratings system
- [ ] Group booking discounts
- [ ] Multi-language support
- [ ] Analytics dashboard
- [ ] Admin panel

---

## 📞 Contact

For questions or support, please contact:
- Email: support@travelgo.com
- Website: https://travelgo.com
- GitHub: https://github.com/travelgo/travelgo

---

**Version**: 1.0.0  
**Last Updated**: March 2026  
**Status**: Production Ready ✅
