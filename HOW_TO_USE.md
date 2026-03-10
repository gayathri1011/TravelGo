📱 TRAVELGO - HOW TO USE THE SEARCH & BOOKING SYSTEM
====================================================

✨ **NEW FEATURE: Book ANY Route!**
You can now book travel from ANY city to ANY other city - we'll find options for you!

🎯 QUICK START
--------------
1. Register: http://localhost:5000/register
2. Login: http://localhost:5000/login
3. Search: http://localhost:5000/search
4. Dashboard: http://localhost:5000/dashboard

🚀 UNIVERSAL BOOKING - WORKS WITH ANY CITIES!
----------------------------------------------
✅ You can now search for routes between ANY two cities
✅ No predefined city list required
✅ Works with Indian cities, international cities, or any place name
✅ Dynamic pricing based on travel mode and distance

📍 EXAMPLE SEARCHES (Try Any of These!)
--------------------------------------

**Domestic Routes:**
- From: Dindigul → To: Trichy (Bus/Train)
- From: Delhi → To: Mumbai (Flight/Train/Bus)
- From: Bangalore → To: Pune (Flight/Bus)
- From: Chennai → To: Hyderabad (Bus/Train/Flight)
- From: Kolkata → To: Delhi (Flight/Train/Bus)

**International (Any City Name Works!):**
- From: New York → To: Los Angeles
- From: London → To: Paris
- From: Tokyo → To: Bangkok
- From: Sydney → To: Melbourne

**Any Combination Works:**
- From: Dindigul → To: Trichy ✅
- From: Small Town A → To: Big City B ✅
- From: Custom Place → To: Another Place ✅

🛎️ HOW TO BOOK SUCCESSFULLY
----------------------------

### Step 1: Register (If New User)
- Email: any valid email
- Name: your full name
- Phone: any phone number
- Password: min 6 characters

### Step 2: Login with Your Credentials
- Email: the registered email
- Password: the password you set

### Step 3: Go to Search Page
- URL: http://localhost:5000/search

### Step 4: Enter Search Details
- **Mode**: Select Bus, Train, Flight, or Hotel
- **From**: Enter departure city (ANY city name works!)
  - Example: Dindigul, Delhi, Bangalore, New York, etc.
- **To**: Enter arrival city (ANY city name works!)
  - Example: Trichy, Mumbai, Chennai, London, etc.
- **Date**: Select today or any future date
- **Click**: Search button

### Step 5: View Results
- You will see 2-4 available options
- Each option shows:
  - Provider name
  - Route details
  - Price
  - Duration
  - Rating
  - Book button

### Step 6: Book Your Ticket
- Click the "Book" button on any option
- You'll see confirmation with booking reference
- Auto-redirect to Dashboard (2 seconds)

### Step 7: View in Dashboard
- Check your booking on Dashboard
- See booking reference, details, price, date
- Cancel if needed

✅ WHAT WORKS NOW
-----------------
✓ Search ANY city to ANY city
✓ Book ANY route combination
✓ Instant booking confirmation
✓ Unique booking reference generated
✓ View all bookings in dashboard
✓ Cancel bookings
✓ Dynamic pricing per mode
✓ All modes: Bus, Train, Flight, Hotel

💰 PRICING BY MODE
------------------
🚌 **Bus**: $25-$60 (3-12 hours)
🚂 **Train**: $35-$80 (4-16 hours)
✈️ **Flight**: $80-$150 (1-8 hours)
🏨 **Hotel**: $60-$200 (1 night)

📊 BOOKING REFERENCE FORMAT
---------------------------
Example: `TG-20260309-A1B2C3D4`
- TG = TravelGo
- 20260309 = Date (YYYYMMDD)
- A1B2C3D4 = Unique code

🔄 COMPLETE TEST FLOW
---------------------
1. Register at http://localhost:5000/register
2. Login at http://localhost:5000/login
3. Search at http://localhost:5000/search
   - Mode: Bus
   - From: Dindigul
   - To: Trichy
   - Date: Today or future
4. Click Search
5. See 2-4 results appear
6. Click Book on any result
7. Get confirmation with reference
8. View booking in Dashboard at http://localhost:5000/dashboard

⚠️ TROUBLESHOOTING
------------------

❌ "Please login to book"
   → You're not logged in
   → Solution: Go to /login and login first

❌ "No results found"
   → This shouldn't happen now!
   → But if it does: check your city names are spelled correctly

❌ "Booking failed"
   → Database error
   → Solution: Refresh and try again

❌ "Can't see dashboard"
   → Not logged in
   → Solution: Login first

✅ SUCCESSFUL BOOKING SIGNS
----------------------------
1. ✓ Search returns 2-4 results
2. ✓ Book button is clickable
3. ✓ Get success message with reference
4. ✓ Booking appears in dashboard
5. ✓ Can see all booking details

💡 TIPS & TRICKS
----------------
• Any city name works - be creative!
• Mix domestic and international cities
• Test with different dates
• Try all 4 travel modes
• Booking reference is unique per booking
• Dashboard shows all your bookings

� SAMPLE TEST ACCOUNT
----------------------
Email: test@example.com
Password: password123

(Or create your own account - works too!)

� TEST SCENARIOS
-----------------

**Scenario 1: Domestic Bus**
- Mode: Bus
- From: Dindigul
- To: Trichy
- Expected: 2-4 bus options with prices $25-$60

**Scenario 2: International Flight**
- Mode: Flight
- From: New York
- To: London
- Expected: 2-4 flight options with prices $80-$150

**Scenario 3: Train Booking**
- Mode: Train
- From: Delhi
- To: Mumbai
- Expected: 2-4 train options with prices $35-$80

**Scenario 4: Hotel Search**
- Mode: Hotel
- From: Bangalore
- To: Chennai
- Expected: 2-4 hotel options with prices $60-$200

🌐 URLs REFERENCE
-----------------
Homepage:           http://localhost:5000/
Register:           http://localhost:5000/register
Login:              http://localhost:5000/login
Search:             http://localhost:5000/search
Dashboard:          http://localhost:5000/dashboard
API Endpoints:      http://localhost:5000/api/*

� DATABASE
-----------
User data: backend/aws/data/users.json
Booking data: backend/aws/data/bookings.json
Both created automatically on first use

🎊 ENJOY BOOKING!
-----------------
Now you can book ANY route from ANY place to ANY destination!
Try searching between different cities and see the magic happen! ✨

Happy Travels! 🚀

