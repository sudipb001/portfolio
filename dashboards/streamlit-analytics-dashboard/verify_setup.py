#!/usr/bin/env python3
"""
Installation Verification Script
Tests that all dependencies are properly installed and configured.
"""

import sys

def check_python_version():
    """Check Python version"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (Need 3.8+)")
        return False

def check_dependencies():
    """Check if all required packages are installed"""
    print("\n📦 Checking dependencies...")
    
    required_packages = {
        'streamlit': 'streamlit',
        'pandas': 'pandas',
        'plotly': 'plotly',
        'supabase': 'supabase',
        'dotenv': 'python-dotenv',
        'openpyxl': 'openpyxl',
        'reportlab': 'reportlab',
        'numpy': 'numpy'
    }
    
    all_installed = True
    
    for module_name, package_name in required_packages.items():
        try:
            __import__(module_name.replace('-', '_'))
            # Get version if available
            try:
                module = __import__(module_name.replace('-', '_'))
                version = getattr(module, '__version__', 'unknown')
                print(f"   ✅ {package_name} ({version})")
            except:
                print(f"   ✅ {package_name}")
        except ImportError:
            print(f"   ❌ {package_name} - NOT INSTALLED")
            all_installed = False
    
    return all_installed

def check_environment():
    """Check environment variables"""
    print("\n🔐 Checking environment variables...")
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_KEY")
    
    if supabase_url and supabase_key:
        print(f"   ✅ SUPABASE_URL: {supabase_url[:30]}...")
        print(f"   ✅ SUPABASE_KEY: {'*' * 20}...")
        return True
    else:
        print("   ⚠️  Supabase credentials not found in .env")
        print("   ℹ️  The app will use sample data instead")
        return False

def check_supabase_connection():
    """Try to connect to Supabase"""
    print("\n🔌 Testing Supabase connection...")
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    try:
        from supabase import create_client
        
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        
        if not url or not key:
            print("   ⚠️  Skipping (credentials not configured)")
            return None
        
        supabase = create_client(url, key)
        
        # Try a simple query
        response = supabase.table('sales_data').select('*').limit(1).execute()
        
        print("   ✅ Successfully connected to Supabase")
        print(f"   ℹ️  Found {len(response.data)} records (showing 1 for test)")
        return True
        
    except Exception as e:
        print(f"   ⚠️  Connection failed: {str(e)}")
        print("   ℹ️  The app will use sample data instead")
        return False

def test_data_generation():
    """Test sample data generation"""
    print("\n📊 Testing sample data generation...")
    
    try:
        import pandas as pd
        import numpy as np
        from datetime import datetime, timedelta
        
        # Simple data generation test
        dates = pd.date_range(start='2024-01-01', end='2024-01-10', freq='D')
        data = [{
            'date': date,
            'revenue': np.random.uniform(1000, 5000),
            'units': np.random.randint(1, 10)
        } for date in dates]
        
        df = pd.DataFrame(data)
        
        print(f"   ✅ Generated {len(df)} sample records")
        print(f"   ℹ️  Date range: {df['date'].min()} to {df['date'].max()}")
        return True
        
    except Exception as e:
        print(f"   ❌ Failed: {str(e)}")
        return False

def print_next_steps(all_checks_passed):
    """Print next steps based on verification results"""
    print("\n" + "="*60)
    
    if all_checks_passed:
        print("🎉 All checks passed! You're ready to go!")
        print("="*60)
        print("\n📝 Next steps:")
        print("   1. Run the app: streamlit run app.py")
        print("   2. Open browser: http://localhost:8501")
        print("   3. Explore the dashboard features")
        print("\n💡 Optional:")
        print("   - Set up Supabase: See README.md for instructions")
        print("   - Customize the dashboard: Edit app.py")
        print("   - Deploy to cloud: See DEPLOYMENT.md")
    else:
        print("⚠️  Some checks failed")
        print("="*60)
        print("\n🔧 To fix issues:")
        print("   1. Install missing packages: pip install -r requirements.txt")
        print("   2. Check Python version (need 3.8+)")
        print("   3. Verify .env file configuration (optional)")
        print("\n📚 Need help? Check README.md")

def main():
    """Run all verification checks"""
    print("="*60)
    print("🔍 Sales Analytics Dashboard - Installation Verification")
    print("="*60)
    
    checks = []
    
    # Run all checks
    checks.append(check_python_version())
    checks.append(check_dependencies())
    
    # These are optional but we'll run them
    check_environment()
    check_supabase_connection()
    checks.append(test_data_generation())
    
    # All required checks must pass
    all_checks_passed = all(checks)
    
    # Print final status
    print_next_steps(all_checks_passed)
    
    return 0 if all_checks_passed else 1

if __name__ == "__main__":
    sys.exit(main())
