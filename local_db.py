"""
Local file-based database for development/testing
Stores data in JSON files instead of AWS DynamoDB
"""

import json
import os
import uuid
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class LocalDatabase:
    """Local file-based database for TravelGo"""

    def __init__(self):
        """Initialize local database"""
        try:
            # Vercel provides /tmp as a writable temporary directory.
            # For local development, continue using the project's data folder.
            if os.getenv('VERCEL') == '1':
                self.data_dir = '/tmp/travelgo_data'
            else:
                self.data_dir = os.path.join(
                    os.path.dirname(__file__),
                    'data'
                )

            # Create the database directory
            Path(self.data_dir).mkdir(
                parents=True,
                exist_ok=True
            )

            self.users_file = os.path.join(
                self.data_dir,
                'users.json'
            )

            self.bookings_file = os.path.join(
                self.data_dir,
                'bookings.json'
            )

            # Initialize files if they don't exist
            self._ensure_files_exist()

            logger.info("Local database initialized successfully")

        except Exception as e:
            logger.error(f"Error initializing local database: {e}")
            raise

    def _ensure_files_exist(self):
        """Ensure database files exist"""

        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({}, f)

        if not os.path.exists(self.bookings_file):
            with open(self.bookings_file, 'w') as f:
                json.dump({}, f)

    def _read_file(self, filepath):
        """Read JSON file"""

        try:
            with open(filepath, 'r') as f:
                return json.load(f)

        except Exception as e:
            logger.error(
                f"Error reading file {filepath}: {e}"
            )
            return {}

    def _write_file(self, filepath, data):
        """Write JSON file"""

        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)

            return True

        except Exception as e:
            logger.error(
                f"Error writing file {filepath}: {e}"
            )
            return False

    # =========================================================
    # USER OPERATIONS
    # =========================================================

    def create_user(
        self,
        email,
        name,
        phone,
        password_hash
    ):
        """Create a new user"""

        try:
            users = self._read_file(self.users_file)

            if email in users:
                logger.warning(
                    f"User already exists: {email}"
                )
                return False

            user_id = str(uuid.uuid4())

            users[email] = {
                'email': email,
                'user_id': user_id,
                'name': name,
                'phone': phone,
                'password_hash': password_hash,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }

            self._write_file(
                self.users_file,
                users
            )

            logger.info(
                f"User created successfully: {email}"
            )

            return True

        except Exception as e:
            logger.error(
                f"Error creating user: {e}"
            )
            return False

    def get_user(self, email):
        """Retrieve user by email"""

        try:
            users = self._read_file(
                self.users_file
            )

            user = users.get(email)

            if user:
                logger.info(
                    f"User retrieved: {email}"
                )

            return user

        except Exception as e:
            logger.error(
                f"Error retrieving user: {e}"
            )
            return None

    def user_exists(self, email):
        """Check if user exists"""

        return self.get_user(email) is not None

    def update_user(self, email, **kwargs):
        """Update user information"""

        try:
            users = self._read_file(
                self.users_file
            )

            if email not in users:
                logger.warning(
                    f"User not found: {email}"
                )
                return False

            user = users[email]

            for key, value in kwargs.items():
                if key in user:
                    user[key] = value

            user['updated_at'] = datetime.now().isoformat()

            users[email] = user

            self._write_file(
                self.users_file,
                users
            )

            logger.info(
                f"User updated successfully: {email}"
            )

            return True

        except Exception as e:
            logger.error(
                f"Error updating user: {e}"
            )
            return False

    # =========================================================
    # BOOKING OPERATIONS
    # =========================================================

    def create_booking(self, booking_data):
        """Create a new booking"""

        try:
            bookings = self._read_file(
                self.bookings_file
            )

            booking_id = str(uuid.uuid4())

            booking_data['booking_id'] = booking_id
            booking_data['created_at'] = (
                datetime.now().isoformat()
            )
            booking_data['updated_at'] = (
                datetime.now().isoformat()
            )

            bookings[booking_id] = booking_data

            self._write_file(
                self.bookings_file,
                bookings
            )

            logger.info(
                f"Booking created successfully: {booking_id}"
            )

            return booking_data

        except Exception as e:
            logger.error(
                f"Error creating booking: {e}"
            )
            return None

    def get_booking(self, booking_id):
        """Get booking by ID"""

        try:
            bookings = self._read_file(
                self.bookings_file
            )

            booking = bookings.get(booking_id)

            if booking:
                logger.info(
                    f"Booking retrieved: {booking_id}"
                )

            return booking

        except Exception as e:
            logger.error(
                f"Error retrieving booking: {e}"
            )
            return None

    def get_user_bookings(self, email):
        """Get all bookings for a user"""

        try:
            bookings = self._read_file(
                self.bookings_file
            )

            user_bookings = [
                booking
                for booking in bookings.values()
                if booking.get('email') == email
            ]

            logger.info(
                f"Retrieved {len(user_bookings)} "
                f"bookings for user: {email}"
            )

            return user_bookings

        except Exception as e:
            logger.error(
                f"Error retrieving user bookings: {e}"
            )
            return []

    def update_booking(self, booking_id, **kwargs):
        """Update booking"""

        try:
            bookings = self._read_file(
                self.bookings_file
            )

            if booking_id not in bookings:
                logger.warning(
                    f"Booking not found: {booking_id}"
                )
                return False

            booking = bookings[booking_id]

            for key, value in kwargs.items():
                if key in booking:
                    booking[key] = value

            booking['updated_at'] = (
                datetime.now().isoformat()
            )

            bookings[booking_id] = booking

            self._write_file(
                self.bookings_file,
                bookings
            )

            logger.info(
                f"Booking updated successfully: {booking_id}"
            )

            return True

        except Exception as e:
            logger.error(
                f"Error updating booking: {e}"
            )
            return False

    def cancel_booking(self, booking_id, email):
        """Cancel a booking"""

        try:
            bookings = self._read_file(
                self.bookings_file
            )

            if booking_id not in bookings:
                logger.warning(
                    f"Booking not found: {booking_id}"
                )
                return False

            booking = bookings[booking_id]

            if booking.get('email') != email:
                logger.warning(
                    "Unauthorized booking cancellation "
                    f"attempt: {booking_id}"
                )
                return False

            booking['status'] = 'Cancelled'

            booking['updated_at'] = (
                datetime.now().isoformat()
            )

            bookings[booking_id] = booking

            self._write_file(
                self.bookings_file,
                bookings
            )

            logger.info(
                f"Booking cancelled successfully: {booking_id}"
            )

            return True

        except Exception as e:
            logger.error(
                f"Error cancelling booking: {e}"
            )
            return False