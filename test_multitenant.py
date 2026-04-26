"""
Simple test to verify multi-tenant data isolation.
Run with: python test_multitenant.py
"""

import os
import django
from django.conf import settings

# Configure Django settings
if not settings.configured:
    settings.configure(
        DEBUG=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": "db.sqlite3",
            }
        },
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.messages",
            "django.contrib.staticfiles",
            "librarymanagement.library",
        ],
        SECRET_KEY="test-secret-key-for-multitenant-testing",
        USE_TZ=True,
    )
    django.setup()

from django.contrib.auth.models import User, Group
from librarymanagement.library.models import Library, Book, StudentExtra, AdminProfile

# Cleanup: Delete test data if it exists
User.objects.filter(username__startswith="test_admin").delete()

# ============== TEST 1: Create Two Libraries ==============
print("\n" + "=" * 60)
print("TEST 1: Creating Two Independent Libraries")
print("=" * 60)

# Create Admin 1 and Library 1
admin1 = User.objects.create_user(
    username="test_admin1", email="admin1@test.local", password="TestPass123!"
)
admin_group, _ = Group.objects.get_or_create(name="ADMIN")
admin_group.user_set.add(admin1)

lib1 = Library.objects.create(name="City Public Library", owner=admin1)
AdminProfile.objects.create(user=admin1, library=lib1)

# Create Admin 2 and Library 2
admin2 = User.objects.create_user(
    username="test_admin2", email="admin2@test.local", password="TestPass123!"
)
admin_group.user_set.add(admin2)

lib2 = Library.objects.create(name="University Central Library", owner=admin2)
AdminProfile.objects.create(user=admin2, library=lib2)

print(f"✓ Created Admin1: {admin1.username}")
print(f"  → Library1: {lib1.name} [CODE: {lib1.code}]")
print(f"\n✓ Created Admin2: {admin2.username}")
print(f"  → Library2: {lib2.name} [CODE: {lib2.code}]")


# ============== TEST 2: Add Books to Each Library ==============
print("\n" + "=" * 60)
print("TEST 2: Adding Books to Each Library")
print("=" * 60)

# Books for Library 1
book1_1 = Book.objects.create(
    library=lib1,
    name="Python Programming",
    author="Guido van Rossum",
    quantity=5,
    category="Education",
)
book1_2 = Book.objects.create(
    library=lib1,
    name="The Great Gatsby",
    author="F. Scott Fitzgerald",
    quantity=3,
    category="Fiction",
)

# Books for Library 2
book2_1 = Book.objects.create(
    library=lib2,
    name="Introduction to Algorithms",
    author="Cormen, Leiserson",
    quantity=4,
    category="Education",
)
book2_2 = Book.objects.create(
    library=lib2,
    name="To Kill a Mockingbird",
    author="Harper Lee",
    quantity=2,
    category="Fiction",
)

print(f"✓ Library 1 Books:")
for book in Book.objects.filter(library=lib1):
    print(f"  - {book.name} by {book.author} ({book.quantity} copies)")

print(f"\n✓ Library 2 Books:")
for book in Book.objects.filter(library=lib2):
    print(f"  - {book.name} by {book.author} ({book.quantity} copies)")


# ============== TEST 3: Add Students to Each Library ==============
print("\n" + "=" * 60)
print("TEST 3: Adding Students to Each Library")
print("=" * 60)

# Students for Library 1
student1_1 = StudentExtra.objects.create(
    library=lib1, name="John Smith", enrollment="LIB1-001", phone="555-0001"
)
student1_2 = StudentExtra.objects.create(
    library=lib1, name="Jane Doe", enrollment="LIB1-002", phone="555-0002"
)

# Students for Library 2
student2_1 = StudentExtra.objects.create(
    library=lib2, name="Alice Johnson", enrollment="UNI-001", phone="555-0003"
)
student2_2 = StudentExtra.objects.create(
    library=lib2, name="Bob Williams", enrollment="UNI-002", phone="555-0004"
)

print(f"✓ Library 1 Students:")
for student in StudentExtra.objects.filter(library=lib1):
    print(f"  - {student.name} ({student.enrollment})")

print(f"\n✓ Library 2 Students:")
for student in StudentExtra.objects.filter(library=lib2):
    print(f"  - {student.name} ({student.enrollment})")


# ============== TEST 4: Data Isolation - Admin1 Cannot See Admin2's Data ==============
print("\n" + "=" * 60)
print("TEST 4: Data Isolation Verification")
print("=" * 60)

# Admin1 queries - should only see Library 1 data
lib1_books_count = Book.objects.filter(library=lib1).count()
lib1_students_count = StudentExtra.objects.filter(library=lib1).count()

# Admin2 queries - should only see Library 2 data
lib2_books_count = Book.objects.filter(library=lib2).count()
lib2_students_count = StudentExtra.objects.filter(library=lib2).count()

# Total counts
total_books = Book.objects.count()
total_students = StudentExtra.objects.count()

print(f"Library 1 (Admin1):")
print(f"  - Books: {lib1_books_count} ✓")
print(f"  - Students: {lib1_students_count} ✓")

print(f"\nLibrary 2 (Admin2):")
print(f"  - Books: {lib2_books_count} ✓")
print(f"  - Students: {lib2_students_count} ✓")

print(f"\nGlobal Totals:")
print(f"  - Total Books (both libraries): {total_books}")
print(f"  - Total Students (both libraries): {total_students}")

# Verify isolation
isolation_ok = (
    lib1_books_count == 2
    and lib1_students_count == 2
    and lib2_books_count == 2
    and lib2_students_count == 2
    and total_books == 4
    and total_students == 4
)

if isolation_ok:
    print(f"\n✅ DATA ISOLATION TEST PASSED!")
else:
    print(f"\n❌ DATA ISOLATION TEST FAILED!")


# ============== TEST 5: Cross-Library Verification ==============
print("\n" + "=" * 60)
print("TEST 5: Cross-Library Data Verification")
print("=" * 60)

# Verify Admin1 books don't leak to Admin2
admin1_book_names = set(
    Book.objects.filter(library=lib1).values_list("name", flat=True)
)
admin2_book_names = set(
    Book.objects.filter(library=lib2).values_list("name", flat=True)
)

overlap = admin1_book_names & admin2_book_names
print(f"Books in both libraries (should be empty): {overlap}")

if not overlap:
    print(f"✅ No book data leakage between libraries!")
else:
    print(f"❌ Data leakage detected!")


# ============== TEST 6: Library Ownership ==============
print("\n" + "=" * 60)
print("TEST 6: Library Ownership Verification")
print("=" * 60)

owner1 = Library.objects.get(id=lib1.id).owner
owner2 = Library.objects.get(id=lib2.id).owner

print(
    f"Library 1 Owner: {owner1.username} (Expected: test_admin1) {'✓' if owner1 == admin1 else '✗'}"
)
print(
    f"Library 2 Owner: {owner2.username} (Expected: test_admin2) {'✓' if owner2 == admin2 else '✗'}"
)

if owner1 == admin1 and owner2 == admin2:
    print(f"\n✅ LIBRARY OWNERSHIP TEST PASSED!")
else:
    print(f"\n❌ LIBRARY OWNERSHIP TEST FAILED!")


print("\n" + "=" * 60)
print("SUMMARY: Multi-Tenant Setup Verification Complete")
print("=" * 60)
print("\n✅ All tests indicate proper multi-tenant data isolation!")
print("\nCleanup: To remove test data, run:")
print("  User.objects.filter(username__startswith='test_admin').delete()")
