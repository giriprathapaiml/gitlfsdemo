import csv
import os
import random
from datetime import date, timedelta

# ============================================================
# CONFIGURATION
# ============================================================

OUTPUT_DIR = "student_dataset"

# Minimum number of records for each file
STUDENT_COUNT = 50_000
MARKS_COUNT = 250_000
ATTENDANCE_COUNT = 500_000
FEES_COUNT = 100_000
COURSES_COUNT = 150_000

# Target minimum size in MB for each generated CSV.
# The script keeps adding records until the file reaches
# approximately this size.
TARGET_SIZE_MB = 5

TARGET_SIZE_BYTES = TARGET_SIZE_MB * 1024 * 1024

random.seed(42)


# ============================================================
# SAMPLE DATA
# ============================================================

FIRST_NAMES = [
    "Aarav", "Aditi", "Arjun", "Ananya", "Aditya",
    "Diya", "Ishaan", "Isha", "Kabir", "Kavya",
    "Rahul", "Riya", "Rohan", "Sneha", "Vikram",
    "Priya", "Karan", "Neha", "Varun", "Meera",
    "Nikhil", "Pooja", "Sanjay", "Shreya", "Akash",
    "Ravi", "Anjali", "Manish", "Divya", "Suresh",
    "Harsh", "Pallavi", "Abhishek", "Nandini", "Yash"
]

LAST_NAMES = [
    "Sharma", "Patel", "Reddy", "Rao", "Kumar",
    "Singh", "Gupta", "Verma", "Mehta", "Iyer",
    "Nair", "Joshi", "Desai", "Mishra", "Das",
    "Agarwal", "Bansal", "Kapoor", "Malhotra", "Shah"
]

COURSES = [
    "Computer Science",
    "Information Technology",
    "Artificial Intelligence",
    "Data Science",
    "Electronics",
    "Mechanical Engineering",
    "Civil Engineering",
    "Electrical Engineering",
    "Business Administration",
    "Commerce"
]

SUBJECTS = [
    "Mathematics",
    "Physics",
    "Chemistry",
    "Programming",
    "Data Structures",
    "Database Management",
    "Operating Systems",
    "Computer Networks",
    "Machine Learning",
    "English"
]

CITIES = [
    "Hyderabad",
    "Bangalore",
    "Chennai",
    "Mumbai",
    "Pune",
    "Delhi",
    "Kolkata",
    "Ahmedabad",
    "Jaipur",
    "Kochi"
]

COLLEGES = [
    "ABC Institute of Technology",
    "Global Engineering College",
    "National Institute of Science",
    "Sunrise University",
    "Tech Valley Institute",
    "City College of Engineering",
    "Modern College",
    "Bright Future University"
]

DEPARTMENTS = [
    "Computer Science",
    "Information Technology",
    "Artificial Intelligence",
    "Data Science",
    "Electronics",
    "Mechanical",
    "Civil",
    "Electrical"
]

PAYMENT_MODES = [
    "UPI",
    "Bank Transfer",
    "Credit Card",
    "Debit Card",
    "Cash"
]

FEE_TYPES = [
    "Tuition",
    "Hostel",
    "Library",
    "Examination",
    "Transport",
    "Laboratory"
]

GENDERS = ["Male", "Female"]

BLOOD_GROUPS = [
    "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"
]


# ============================================================
# HELPERS
# ============================================================

def random_date(start_year=2000, end_year=2007):
    start = date(start_year, 1, 1)
    end = date(end_year, 12, 31)

    days = (end - start).days

    return start + timedelta(
        days=random.randint(0, days)
    )


def random_phone():
    return f"+91-{random.randint(7000000000, 9999999999)}"


def random_email(student_id):
    return f"student{student_id}@example.com"


def random_amount(minimum, maximum):
    return round(random.uniform(minimum, maximum), 2)


def ensure_output_directory():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def write_csv_until_size(
    filename,
    fieldnames,
    row_generator,
    minimum_records
):
    """
    Write CSV records until both conditions are satisfied:

    1. At least minimum_records exist.
    2. File reaches TARGET_SIZE_MB.

    This is useful for creating large files for Git LFS demos.
    """

    path = os.path.join(OUTPUT_DIR, filename)

    count = 0

    with open(
        path,
        "w",
        newline="",
        encoding="utf-8"
    ) as csv_file:

        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        while True:
            row = row_generator(count + 1)

            writer.writerow(row)

            count += 1

            # Check file size every 1,000 records
            if count % 1000 == 0:

                csv_file.flush()

                current_size = os.path.getsize(path)

                if (
                    count >= minimum_records
                    and current_size >= TARGET_SIZE_BYTES
                ):
                    break

    size_mb = os.path.getsize(path) / (1024 * 1024)

    print(
        f"{filename:<30} "
        f"{count:>10,} records "
        f"{size_mb:>8.2f} MB"
    )


# ============================================================
# STUDENTS
# ============================================================

def generate_student(student_id):

    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)

    return {
        "student_id": f"STU{student_id:07d}",
        "first_name": first_name,
        "last_name": last_name,
        "full_name": f"{first_name} {last_name}",
        "gender": random.choice(GENDERS),
        "date_of_birth": random_date().isoformat(),
        "email": random_email(student_id),
        "phone": random_phone(),
        "course": random.choice(COURSES),
        "department": random.choice(DEPARTMENTS),
        "college": random.choice(COLLEGES),
        "city": random.choice(CITIES),
        "blood_group": random.choice(BLOOD_GROUPS),
        "year": random.randint(1, 4),
        "section": random.choice(["A", "B", "C", "D"]),
        "hostel": random.choice(["Yes", "No"]),
        "scholarship": random.choice(["Yes", "No"]),
    }


def generate_students():

    fields = [
        "student_id",
        "first_name",
        "last_name",
        "full_name",
        "gender",
        "date_of_birth",
        "email",
        "phone",
        "course",
        "department",
        "college",
        "city",
        "blood_group",
        "year",
        "section",
        "hostel",
        "scholarship"
    ]

    write_csv_until_size(
        "students.csv",
        fields,
        lambda i: generate_student(i),
        STUDENT_COUNT
    )


# ============================================================
# MARKS
# ============================================================

def generate_marks(record_id):

    student_id = random.randint(1, STUDENT_COUNT)

    marks = random.randint(35, 100)

    return {
        "mark_id": f"MARK{record_id:08d}",
        "student_id": f"STU{student_id:07d}",
        "subject": random.choice(SUBJECTS),
        "semester": random.randint(1, 8),
        "marks": marks,
        "max_marks": 100,
        "grade": (
            "A+" if marks >= 90 else
            "A" if marks >= 80 else
            "B" if marks >= 70 else
            "C" if marks >= 60 else
            "D" if marks >= 50 else
            "F"
        ),
        "exam_type": random.choice([
            "Midterm",
            "Final",
            "Assignment",
            "Practical"
        ])
    }


def generate_marks_file():

    fields = [
        "mark_id",
        "student_id",
        "subject",
        "semester",
        "marks",
        "max_marks",
        "grade",
        "exam_type"
    ]

    write_csv_until_size(
        "student_marks.csv",
        fields,
        lambda i: generate_marks(i),
        MARKS_COUNT
    )


# ============================================================
# ATTENDANCE
# ============================================================

def generate_attendance(record_id):

    student_id = random.randint(1, STUDENT_COUNT)

    total_classes = random.randint(60, 120)

    attended = random.randint(
        int(total_classes * 0.55),
        total_classes
    )

    percentage = round(
        (attended / total_classes) * 100,
        2
    )

    return {
        "attendance_id": f"ATT{record_id:09d}",
        "student_id": f"STU{student_id:07d}",
        "month": random.randint(1, 12),
        "year": random.choice([2024, 2025, 2026]),
        "total_classes": total_classes,
        "classes_attended": attended,
        "attendance_percentage": percentage,
        "status": (
            "Good"
            if percentage >= 75
            else "Shortage"
        )
    }


def generate_attendance_file():

    fields = [
        "attendance_id",
        "student_id",
        "month",
        "year",
        "total_classes",
        "classes_attended",
        "attendance_percentage",
        "status"
    ]

    write_csv_until_size(
        "student_attendance.csv",
        fields,
        lambda i: generate_attendance(i),
        ATTENDANCE_COUNT
    )


# ============================================================
# FEES
# ============================================================

def generate_fee(record_id):

    student_id = random.randint(1, STUDENT_COUNT)

    fee_amount = random_amount(5000, 150000)

    paid = random.choice([
        "Paid",
        "Paid",
        "Paid",
        "Pending",
        "Partial"
    ])

    if paid == "Paid":
        amount_paid = fee_amount
    elif paid == "Partial":
        amount_paid = round(
            fee_amount * random.uniform(0.3, 0.8),
            2
        )
    else:
        amount_paid = 0

    return {
        "fee_id": f"FEE{record_id:08d}",
        "student_id": f"STU{student_id:07d}",
        "fee_type": random.choice(FEE_TYPES),
        "semester": random.randint(1, 8),
        "fee_amount": fee_amount,
        "amount_paid": amount_paid,
        "balance": round(
            fee_amount - amount_paid,
            2
        ),
        "payment_status": paid,
        "payment_mode": random.choice(PAYMENT_MODES),
        "payment_date": random_date(
            2024,
            2026
        ).isoformat()
    }


def generate_fees_file():

    fields = [
        "fee_id",
        "student_id",
        "fee_type",
        "semester",
        "fee_amount",
        "amount_paid",
        "balance",
        "payment_status",
        "payment_mode",
        "payment_date"
    ]

    write_csv_until_size(
        "student_fees.csv",
        fields,
        lambda i: generate_fee(i),
        FEES_COUNT
    )


# ============================================================
# COURSE ENROLLMENTS
# ============================================================

def generate_course(record_id):

    student_id = random.randint(1, STUDENT_COUNT)

    course = random.choice(COURSES)

    return {
        "enrollment_id": f"ENR{record_id:08d}",
        "student_id": f"STU{student_id:07d}",
        "course_code": (
            f"{course[:3].upper()}"
            f"{random.randint(100, 999)}"
        ),
        "course_name": course,
        "semester": random.randint(1, 8),
        "credits": random.choice([2, 3, 4, 5]),
        "faculty": (
            random.choice(FIRST_NAMES)
            + " "
            + random.choice(LAST_NAMES)
        ),
        "academic_year": random.choice([
            "2024-25",
            "2025-26",
            "2026-27"
        ]),
        "result": random.choice([
            "Pass",
            "Pass",
            "Pass",
            "Pass",
            "Fail",
            "Pending"
        ])
    }


def generate_courses_file():

    fields = [
        "enrollment_id",
        "student_id",
        "course_code",
        "course_name",
        "semester",
        "credits",
        "faculty",
        "academic_year",
        "result"
    ]

    write_csv_until_size(
        "student_courses.csv",
        fields,
        lambda i: generate_course(i),
        COURSES_COUNT
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("Student Dataset Generator")
    print("=" * 70)

    print(f"Target minimum size : {TARGET_SIZE_MB} MB")
    print(f"Output directory    : {OUTPUT_DIR}")
    print()

    ensure_output_directory()

    generate_students()

    generate_marks_file()

    generate_attendance_file()

    generate_fees_file()

    generate_courses_file()

    print()
    print("=" * 70)
    print("Generation completed!")
    print("=" * 70)

    print()
    print("Generated files:")

    for filename in os.listdir(OUTPUT_DIR):

        path = os.path.join(
            OUTPUT_DIR,
            filename
        )

        size_mb = os.path.getsize(path) / (
            1024 * 1024
        )

        print(
            f"  {filename:<30}"
            f"{size_mb:>8.2f} MB"
        )


if __name__ == "__main__":
    main()
