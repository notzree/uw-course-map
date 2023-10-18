import os
from dotenv import load_dotenv
import requests
from typing import List
from db import database
load_dotenv()


class CourseInfo:
    courseId: str
    courseOfferNumber: int
    termCode: str
    termName: str
    associatedAcademicCareer: str
    associatedAcademicGroupCode: str
    associatedAcademicOrgCode: str
    subjectCode: str
    catalogNumber: str
    title: str
    descriptionAbbreviated: str
    description: str
    gradingBasis: str
    courseComponentCode: str
    enrollConsentCode: str
    enrollConsentDescription: str
    dropConsentCode: str
    dropConsentDescription: str
    requirementsDescription: str


uw_api_key = os.environ.get('UW_API_KEY')
url = "https://openapi.data.uwaterloo.ca/v3"
termCode = 1239

db = database()
db.createTables()

# Get ALL courses in the term
response = requests.get(f"{url}/Courses/{termCode}", headers={
    'accept': 'application/json',
    'x-api-key': '71BE603A75AE488CB068D7A9D56333A2'
})
courses: List[CourseInfo] = response.json()

print("Adding courses to database...")
for course in courses:
    db.addClass(course)
