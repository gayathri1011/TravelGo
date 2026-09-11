"""
Search routes for finding travel options
"""

from flask import Blueprint, request, jsonify
import json
import os
import logging
import random


logger = logging.getLogger(__name__)

search_bp = Blueprint(
    "search",
    __name__,
    url_prefix="/api"
)


# ============================================================
# MOCK TRAVEL DATA
# ============================================================

MOCK_LISTINGS = {}


def load_mock_data():
    """
    Load mock travel data from listings.json if available.

    If listings.json does not exist, the application will
    use dynamically generated travel results instead.
    """

    global MOCK_LISTINGS

    json_file = os.path.join(
        os.path.dirname(__file__),
        "listings.json"
    )

    try:

        if os.path.exists(json_file):

            with open(
                json_file,
                "r",
                encoding="utf-8"
            ) as f:

                MOCK_LISTINGS = json.load(f)

            logger.info(
                "Mock data loaded successfully"
            )

        else:

            logger.info(
                "listings.json not found. "
                "Using dynamic travel results."
            )

            MOCK_LISTINGS = {
                "Bus": [],
                "Train": [],
                "Flight": [],
                "Hotel": []
            }

    except Exception as e:

        logger.error(
            f"Error loading mock data: {e}"
        )

        MOCK_LISTINGS = {
            "Bus": [],
            "Train": [],
            "Flight": [],
            "Hotel": []
        }


# ============================================================
# SEARCH ROUTE
# ============================================================

@search_bp.route(
    "/search",
    methods=["GET"]
)
def search():
    """
    Search for travel options.

    Query parameters:
        mode: Bus | Train | Flight | Hotel
        from: Departure/location city
        to: Arrival/destination city
        date: Travel date
    """

    try:

        mode = request.args.get(
            "mode",
            ""
        ).strip()

        from_city = request.args.get(
            "from",
            ""
        ).strip()

        to_city = request.args.get(
            "to",
            ""
        ).strip()

        date = request.args.get(
            "date",
            ""
        ).strip()

        # ----------------------------------------------------
        # Validate required parameters
        # ----------------------------------------------------

        if (
            not mode
            or not from_city
            or not to_city
            or not date
        ):

            return jsonify({
                "success": False,
                "message": (
                    "Missing required parameters: "
                    "mode, from, to, date"
                )
            }), 400

        # ----------------------------------------------------
        # Validate travel mode
        # ----------------------------------------------------

        valid_modes = [
            "Bus",
            "Train",
            "Flight",
            "Hotel"
        ]

        if mode not in valid_modes:

            return jsonify({
                "success": False,
                "message": (
                    "Invalid mode. Valid options: "
                    + ", ".join(valid_modes)
                )
            }), 400

        # ----------------------------------------------------
        # Load mock data
        # ----------------------------------------------------

        if not MOCK_LISTINGS:

            load_mock_data()

        results = []

        # ----------------------------------------------------
        # Search exact matches
        # ----------------------------------------------------

        if mode in MOCK_LISTINGS:

            for item in MOCK_LISTINGS[mode]:

                item_from = str(
                    item.get("from", "")
                ).lower()

                item_to = str(
                    item.get("to", "")
                ).lower()

                if (
                    item_from == from_city.lower()
                    and
                    item_to == to_city.lower()
                ):

                    results.append(item)

        # ----------------------------------------------------
        # Generate dynamic results if no match
        # ----------------------------------------------------

        if not results:

            results = generate_dynamic_results(
                mode,
                from_city,
                to_city
            )

        logger.info(
            f"Search: mode={mode}, "
            f"from={from_city}, "
            f"to={to_city}, "
            f"found={len(results)}"
        )

        return jsonify({

            "success": True,

            "mode": mode,

            "from": from_city,

            "to": to_city,

            "date": date,

            "count": len(results),

            "results": results

        }), 200

    except Exception as e:

        logger.error(
            f"Search error: {e}"
        )

        return jsonify({
            "success": False,
            "message": "Internal server error"
        }), 500


# ============================================================
# DYNAMIC TRAVEL RESULTS
# ============================================================

def generate_dynamic_results(
    mode,
    from_city,
    to_city
):
    """
    Generate dynamic travel options for any
    city combination.
    """

    # --------------------------------------------------------
    # Price ranges
    # --------------------------------------------------------

    price_ranges = {

        "Bus": (
            25,
            60
        ),

        "Train": (
            35,
            80
        ),

        "Flight": (
            80,
            150
        ),

        "Hotel": (
            60,
            200
        )

    }

    # --------------------------------------------------------
    # Duration ranges
    # --------------------------------------------------------

    duration_ranges = {

        "Bus": (
            3,
            12
        ),

        "Train": (
            4,
            16
        ),

        "Flight": (
            1,
            8
        ),

        "Hotel": (
            1,
            1
        )

    }

    # --------------------------------------------------------
    # Providers
    # --------------------------------------------------------

    providers = {

        "Bus": [
            "Express Bus",
            "Rapid Transit",
            "Quick Travels",
            "Speed Coach",
            "Premium Travels"
        ],

        "Train": [
            "Express Train",
            "Fast Track",
            "Rail Express",
            "High Speed Train",
            "Premium Express"
        ],

        "Flight": [
            "Air India",
            "IndiGo",
            "SpiceJet",
            "Vistara",
            "Go Air"
        ],

        "Hotel": [
            "Hotel Grand",
            "The Plaza",
            "Luxury Inn",
            "City Hotel",
            "Premium Stay"
        ]

    }

    results = []

    min_price, max_price = price_ranges.get(
        mode,
        (25, 100)
    )

    min_duration, max_duration = duration_ranges.get(
        mode,
        (1, 10)
    )

    # --------------------------------------------------------
    # Generate 2–4 travel options
    # --------------------------------------------------------

    num_options = random.randint(
        2,
        4
    )

    for i in range(num_options):

        price = random.randint(
            min_price,
            max_price
        )

        # ----------------------------------------------------
        # Hotel
        # ----------------------------------------------------

        if mode == "Hotel":

            duration = "1 night"

            seats = random.randint(
                5,
                20
            )

        # ----------------------------------------------------
        # Bus / Train / Flight
        # ----------------------------------------------------

        else:

            duration_hours = random.randint(
                min_duration,
                max_duration
            )

            minutes = random.randint(
                0,
                59
            )

            if minutes > 0:

                duration = (
                    f"{duration_hours}h "
                    f"{minutes}m"
                )

            else:

                duration = (
                    f"{duration_hours}h"
                )

            seats = random.randint(
                20,
                100
            )

        provider_list = providers.get(
            mode,
            ["Transport Co"]
        )

        provider = provider_list[
            i % len(provider_list)
        ]

        # ----------------------------------------------------
        # Create result
        # ----------------------------------------------------

        result = {

            "id": (
                f"{mode[0]}"
                f"{i + 1}_"
                f"{from_city[:2]}_"
                f"{to_city[:2]}"
            ),

            "name": provider,

            "from": from_city,

            "to": to_city,

            "price": price,

            "duration": duration,

            "seats": seats,

            "rating": round(
                random.uniform(
                    3.8,
                    5.0
                ),
                1
            )

        }

        results.append(
            result
        )

    return results


# ============================================================
# DESTINATIONS
# ============================================================

@search_bp.route(
    "/destinations",
    methods=["GET"]
)
def get_destinations():
    """Get all available destinations."""

    try:

        if not MOCK_LISTINGS:

            load_mock_data()

        destinations = set()

        for mode, items in MOCK_LISTINGS.items():

            for item in items:

                from_city = item.get(
                    "from"
                )

                to_city = item.get(
                    "to"
                )

                if from_city:

                    destinations.add(
                        from_city
                    )

                if to_city:

                    destinations.add(
                        to_city
                    )

        return jsonify({

            "success": True,

            "count": len(destinations),

            "destinations": sorted(
                list(destinations)
            )

        }), 200

    except Exception as e:

        logger.error(
            f"Get destinations error: {e}"
        )

        return jsonify({
            "success": False,
            "message": "Internal server error"
        }), 500


# ============================================================
# LISTINGS BY MODE
# ============================================================

@search_bp.route(
    "/listings/<mode>",
    methods=["GET"]
)
def get_listings_by_mode(mode):
    """Get all listings for a specific travel mode."""

    try:

        if not MOCK_LISTINGS:

            load_mock_data()

        valid_modes = [
            "Bus",
            "Train",
            "Flight",
            "Hotel"
        ]

        if mode not in valid_modes:

            return jsonify({

                "success": False,

                "message": (
                    "Invalid mode. Valid options: "
                    + ", ".join(valid_modes)
                )

            }), 400

        listings = MOCK_LISTINGS.get(
            mode,
            []
        )

        return jsonify({

            "success": True,

            "mode": mode,

            "count": len(listings),

            "listings": listings

        }), 200

    except Exception as e:

        logger.error(
            f"Get listings error: {e}"
        )

        return jsonify({
            "success": False,
            "message": "Internal server error"
        }), 500


# ============================================================
# INITIALIZE MOCK DATA
# ============================================================

load_mock_data()