import os, shutil

base_test_db_fp = "DBManager/tests/data/base_app_test.db"
test_db_fp = "DBManager/tests/data/app_test.db"

# Post Session object creation, Pre Test Collection
def pytest_sessionstart(session):
    # Check if test db was not cleaned up
    if os.path.exists(test_db_fp):
        os.remove(test_db_fp)
    shutil.copy2(base_test_db_fp, test_db_fp)

# Post test run finish, pre exit status
def pytest_sessionfinish(session):
    # Cleanup test DB
    if os.path.exists(test_db_fp):
        os.remove(test_db_fp)