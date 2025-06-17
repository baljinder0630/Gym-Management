from typing import Any, Optional
import httpx
from mcp.server.fastmcp import FastMCP
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("gym")

# Constants
BASE_URL = "https://ai-workout-planner-exercise-fitness-nutrition-guide.p.rapidapi.com"
RAPID_APIKEY = os.getenv("RAPID_APIKEY")

if not RAPID_APIKEY:
    logger.warning("RAPID_APIKEY environment variable not set")


async def make_api_request(endpoint: str, payload: dict) -> dict:
    """Make API request to the gym management service"""
    if not RAPID_APIKEY:
        raise Exception(
            "API key not configured. Please set RAPID_APIKEY environment variable.")

    url = f"{BASE_URL}{endpoint}"

    headers = {
        'x-rapidapi-key': RAPID_APIKEY,
        'x-rapidapi-host': "ai-workout-planner-exercise-fitness-nutrition-guide.p.rapidapi.com",
        'Content-Type': "application/json"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()
    except httpx.TimeoutException:
        raise Exception("API request timed out. Please try again.")
    except httpx.HTTPStatusError as e:
        raise Exception(
            f"API request failed with status {e.response.status_code}: {e.response.text}")
    except Exception as e:
        raise Exception(f"API request failed: {str(e)}")


def validate_required_params(**kwargs) -> dict:
    """Validate and set default values for parameters"""
    errors = []
    validated_params = {}

    for key, value in kwargs.items():
        if value is None or (isinstance(value, str) and value.strip() == ""):
            errors.append(f"Missing required parameter: {key}")
        else:
            validated_params[key] = value

    if errors:
        raise ValueError(f"Validation errors: {'; '.join(errors)}")

    return validated_params


@mcp.tool()
async def generateWorkoutPlan(
    goal: Optional[str] = None,
    fitness_level: Optional[str] = None,
    preferences: Optional[list[str]] = None,
    health_conditions: Optional[list[str]] = None,
    days_per_week: Optional[int] = None,
    session_duration: Optional[int] = None,
    plan_duration_weeks: Optional[int] = None,
    lang: str = "en"
) -> dict:
    """
    Generate a workout plan based on user input.

    Args:
        goal: Fitness goal (e.g., "weight_loss", "muscle_gain", "endurance")
        fitness_level: Current fitness level (e.g., "beginner", "intermediate", "advanced")
        preferences: List of exercise preferences (e.g., ["cardio", "strength_training"])
        health_conditions: List of health conditions to consider (e.g., ["knee_injury"])
        days_per_week: Number of workout days per week (1-7)
        session_duration: Duration of each session in minutes
        plan_duration_weeks: Duration of the plan in weeks
        lang: Language code (default: "en")
    """
    try:
        # Set defaults for missing values
        goal = goal or "general_fitness"
        fitness_level = fitness_level or "beginner"
        preferences = preferences or ["mixed"]
        health_conditions = health_conditions or []
        days_per_week = days_per_week or 3
        session_duration = session_duration or 45
        plan_duration_weeks = plan_duration_weeks or 4

        # Validate numeric parameters
        if not (1 <= days_per_week <= 7):
            raise ValueError("days_per_week must be between 1 and 7")
        if not (15 <= session_duration <= 180):
            raise ValueError(
                "session_duration must be between 15 and 180 minutes")
        if not (1 <= plan_duration_weeks <= 52):
            raise ValueError(
                "plan_duration_weeks must be between 1 and 52 weeks")

        payload = {
            "goal": goal,
            "fitness_level": fitness_level,
            "preferences": preferences,
            "health_conditions": health_conditions,
            "schedule": {
                "days_per_week": days_per_week,
                "session_duration": session_duration
            },
            "plan_duration_weeks": plan_duration_weeks,
            "lang": lang
        }

        logger.info(f"Generating workout plan with payload: {payload}")
        return await make_api_request("/generateWorkoutPlan?noqueue=1", payload)

    except ValueError as e:
        return {"error": str(e), "status": "validation_error"}
    except Exception as e:
        logger.error(f"Error generating workout plan: {str(e)}")
        return {"error": str(e), "status": "api_error"}


@mcp.tool()
async def nutritionAdvice(
    goal: Optional[str] = None,
    dietary_restrictions: Optional[list[str]] = None,
    current_weight: Optional[float] = None,
    target_weight: Optional[float] = None,
    daily_activity_level: Optional[str] = None,
    lang: str = "en"
) -> dict:
    """
    Generate nutrition advice based on user input.

    Args:
        goal: Nutrition goal (e.g., "weight_loss", "weight_gain", "maintain_weight")
        dietary_restrictions: List of dietary restrictions (e.g., ["vegetarian", "gluten_free"])
        current_weight: Current weight in kg
        target_weight: Target weight in kg
        daily_activity_level: Activity level (e.g., "sedentary", "moderate", "active", "very_active")
        lang: Language code (default: "en")
    """
    try:
        # Set defaults for missing values
        goal = goal or "maintain_weight"
        dietary_restrictions = dietary_restrictions or []
        current_weight = current_weight or 70.0
        target_weight = target_weight or current_weight
        daily_activity_level = daily_activity_level or "moderate"

        # Validate weight parameters
        if not (30 <= current_weight <= 300):
            raise ValueError("current_weight must be between 30 and 300 kg")
        if not (30 <= target_weight <= 300):
            raise ValueError("target_weight must be between 30 and 300 kg")

        # Validate activity level
        valid_activity_levels = ["sedentary", "light",
                                 "moderate", "active", "very_active"]
        if daily_activity_level not in valid_activity_levels:
            daily_activity_level = "moderate"

        payload = {
            "goal": goal,
            "dietary_restrictions": dietary_restrictions,
            "current_weight": current_weight,
            "target_weight": target_weight,
            "daily_activity_level": daily_activity_level,
            "lang": lang
        }

        logger.info(f"Getting nutrition advice with payload: {payload}")
        return await make_api_request("/nutritionAdvice?noqueue=1", payload)

    except ValueError as e:
        return {"error": str(e), "status": "validation_error"}
    except Exception as e:
        logger.error(f"Error getting nutrition advice: {str(e)}")
        return {"error": str(e), "status": "api_error"}


@mcp.tool()
async def exerciseDetail(
    exercise_name: Optional[str] = None,
    lang: str = "en"
) -> dict:
    """
    Get details about a specific exercise.

    Args:
        exercise_name: Name of the exercise to get details for
        lang: Language code (default: "en")
    """
    try:
        if not exercise_name or exercise_name.strip() == "":
            return {
                "error": "Exercise name is required",
                "status": "validation_error",
                "suggestion": "Please provide an exercise name (e.g., 'push-ups', 'squats', 'bench press')"
            }

        payload = {
            "exercise_name": exercise_name.strip(),
            "lang": lang
        }

        logger.info(f"Getting exercise details with payload: {payload}")
        return await make_api_request("/exerciseDetails?noqueue=1", payload)

    except Exception as e:
        logger.error(f"Error getting exercise details: {str(e)}")
        return {"error": str(e), "status": "api_error"}


@mcp.tool()
async def customWorkoutPlan(
    goal: Optional[str] = None,
    fitness_level: Optional[str] = None,
    preferences: Optional[list[str]] = None,
    health_conditions: Optional[list[str]] = None,
    days_per_week: Optional[int] = None,
    session_duration: Optional[int] = None,
    plan_duration_weeks: Optional[int] = None,
    custom_goals: Optional[list[str]] = None,
    lang: str = "en"
) -> dict:
    """
    Generate a custom workout plan with additional goals.

    Args:
        goal: Primary fitness goal
        fitness_level: Current fitness level
        preferences: Exercise preferences
        health_conditions: Health conditions to consider
        days_per_week: Number of workout days per week
        session_duration: Duration of each session in minutes
        plan_duration_weeks: Duration of the plan in weeks
        custom_goals: Additional custom goals
        lang: Language code (default: "en")
    """
    try:
        # Set defaults for missing values
        goal = goal or "general_fitness"
        fitness_level = fitness_level or "beginner"
        preferences = preferences or ["mixed"]
        health_conditions = health_conditions or []
        days_per_week = days_per_week or 3
        session_duration = session_duration or 45
        plan_duration_weeks = plan_duration_weeks or 4
        custom_goals = custom_goals or []

        # Validate numeric parameters
        if not (1 <= days_per_week <= 7):
            raise ValueError("days_per_week must be between 1 and 7")
        if not (15 <= session_duration <= 180):
            raise ValueError(
                "session_duration must be between 15 and 180 minutes")
        if not (1 <= plan_duration_weeks <= 52):
            raise ValueError(
                "plan_duration_weeks must be between 1 and 52 weeks")

        payload = {
            "goal": goal,
            "fitness_level": fitness_level,
            "preferences": preferences,
            "health_conditions": health_conditions,
            "schedule": {
                "days_per_week": days_per_week,
                "session_duration": session_duration
            },
            "plan_duration_weeks": plan_duration_weeks,
            "custom_goals": custom_goals,
            "lang": lang
        }

        logger.info(f"Generating custom workout plan with payload: {payload}")
        return await make_api_request("/customWorkoutPlan?noqueue=1", payload)

    except ValueError as e:
        return {"error": str(e), "status": "validation_error"}
    except Exception as e:
        logger.error(f"Error generating custom workout plan: {str(e)}")
        return {"error": str(e), "status": "api_error"}


@mcp.resource("echo://{message}")
def echo_resource(message: str) -> str:
    """Echo a message as a resource"""
    return f"Resource echo: {message}"


if __name__ == "__main__":
    mcp.run()
