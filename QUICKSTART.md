# TravelGo Quick Start Guide

## ⚡ 5-Minute Setup

### 1. Prerequisites Check
```bash
# Verify Python installation
python --version  # Should be 3.8+

# Verify pip installation
pip --version
```

### 2. AWS Setup (5 minutes)
1. Go to AWS Console → IAM
2. Create user with:
   - `AmazonDynamoDBFullAccess`
   - `AmazonSNSFullAccess`
3. Create security credentials (Access Key & Secret Key)
4. Go to DynamoDB → Create Tables:
   - **Users**: Partition Key = `email`
   - **Bookings**: Partition Key = `booking_id`, Sort Key = `email`
5. Go to SNS → Create Topic `TravelGo_Notifications`
6. Subscribe your email to the topic

### 3. Environment Setup (2 minutes)
```bash
cd TravelGo/backend
cp .env.example .env
```

Edit `.env`:
```
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1
SNS_TOPIC_ARN=arn:aws:sns:us-east-1:account-id:TravelGo_Notifications
```

### 4. Install & Run (2 minutes)
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

Visit: **http://localhost:5000**

---

## 🧪 Test the Application

1. **Register**: Create a new account
2. **Search**: Find buses from Hyderabad to Bangalore
3. **Book**: Select and book a bus
4. **Check Email**: Confirm booking notification received
5. **Dashboard**: View your bookings
6. **Cancel**: Cancel a booking

---

## 📦 Docker Quick Start

```bash
# From project root
docker-compose up --build

# Access at http://localhost:5000
```

---

## 🆘 Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 5000 already in use | `lsof -i :5000` then `kill -9 <PID>` |
| DynamoDB connection error | Check AWS credentials in `.env` |
| SNS not sending emails | Confirm email subscription in SNS console |
| Module not found | Run `pip install -r requirements.txt` again |

---

## 📞 Need Help?

- Check README.md for detailed documentation
- Review AWS CloudFormation template for infrastructure
- Check Flask logs: `FLASK_ENV=development python app.py`

---

**Ready to go! Start booking travels with TravelGo!** 🚀
