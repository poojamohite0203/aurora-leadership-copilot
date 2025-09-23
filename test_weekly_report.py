#!/usr/bin/env python3

import sys
import os
sys.path.append('/Users/pmohite3/Library/CloudStorage/OneDrive-azureford/Documents/AI-PROJECTS/aurora-leadership-copilot/src')

from datetime import datetime
from db.database import get_db
from api.services.process_service import generate_weekly_report

def test_weekly_report():
    db = next(get_db())
    
    # Test with current date
    today = datetime.now()
    print(f"Generating weekly report for {today.strftime('%Y-%m-%d')}")
    
    try:
        report = generate_weekly_report(today, db, force_regen=True)
        print(f"Report generated: {report}")
        print(f"Summary type: {type(report.summary)}")
        print(f"Summary content (first 200 chars): {repr(report.summary[:200])}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_weekly_report()
