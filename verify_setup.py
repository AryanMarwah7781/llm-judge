"""
Simple test script to verify installation and basic functionality.
Run this after installation to ensure everything is set up correctly.
"""
import sys


def check_imports():
    """Check if all required packages are installed."""
    print("Checking package imports...")
    packages = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("openai", "OpenAI"),
        ("anthropic", "Anthropic"),
        ("pydantic", "Pydantic"),
        ("pymupdf4llm", "PyMuPDF4LLM"),
        ("tenacity", "Tenacity"),
    ]
    
    failed = []
    for module, name in packages:
        try:
            __import__(module)
            print(f"  ✅ {name}")
        except ImportError as e:
            print(f"  ❌ {name}: {e}")
            failed.append(name)
    
    return len(failed) == 0


def check_env():
    """Check environment configuration."""
    print("\nChecking environment configuration...")
    try:
        from app.config import settings
        
        print(f"  Environment: {settings.environment}")
        print(f"  Log Level: {settings.log_level}")
        print(f"  OpenAI Key Configured: {settings.has_openai_key()}")
        print(f"  Anthropic Key Configured: {settings.has_anthropic_key()}")
        
        if not settings.has_openai_key() and not settings.has_anthropic_key():
            print("\n  ⚠️  Warning: No API keys configured!")
            print("     Set at least one API key in .env file")
            return False
        
        print("  ✅ Configuration valid")
        return True
        
    except Exception as e:
        print(f"  ❌ Configuration error: {e}")
        return False


def check_app():
    """Check if FastAPI app can be imported."""
    print("\nChecking FastAPI application...")
    try:
        from app.main import app
        print(f"  App Title: {app.title}")
        print(f"  Version: {app.version}")
        print(f"  Routes: {len(app.routes)}")
        print("  ✅ Application loads successfully")
        return True
    except Exception as e:
        print(f"  ❌ Application error: {e}")
        return False


def main():
    """Run all checks."""
    print("="*60)
    print("LLM as Judge - Installation Verification")
    print("="*60 + "\n")
    
    results = [
        check_imports(),
        check_env(),
        check_app()
    ]
    
    print("\n" + "="*60)
    if all(results):
        print("✅ All checks passed! System is ready.")
        print("\nNext steps:")
        print("1. Configure API keys in .env file (if not done)")
        print("2. Run the server: uvicorn app.main:app --reload")
        print("3. Visit http://localhost:8000/docs for API documentation")
        return 0
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("- Install missing packages: pip install -r requirements.txt")
        print("- Copy .env.example to .env and configure API keys")
        print("- Check for Python version compatibility (3.10+)")
        return 1


if __name__ == "__main__":
    sys.exit(main())
