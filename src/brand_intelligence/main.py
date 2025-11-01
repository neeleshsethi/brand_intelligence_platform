"""
Main entry point for the Brand Intelligence Platform.
"""

from brand_intelligence.config import Config


def main() -> None:
    """Main application entry point."""
    print("Brand Intelligence Platform v0.1.0")
    print(f"Environment: {Config.ENV}")
    print(f"Data directory: {Config.DATA_DIR}")

    # Initialize your application here
    print("\nPlatform initialized successfully!")


if __name__ == "__main__":
    main()
