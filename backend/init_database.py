import os
from dotenv import load_dotenv
import requests
from typing import List
from db import database
from qdrant_client.http.models import PointStruct
load_dotenv()


class CourseInfo:
    id: str
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
    'x-api-key': uw_api_key
})
courses: List[CourseInfo] = response.json()
filtered_courses = [
    course for course in courses if course['associatedAcademicGroupCode'] == 'ENG']
print(f"Adding {len(filtered_courses)} courses to database...")
points = []
for index, course in enumerate(filtered_courses):
    if course['associatedAcademicGroupCode'] != 'ENG':
        continue
    db.addClass(course)
    vectors = db.embedding_client.embed_query(course['description'])
    points.append(PointStruct(
        id=index, vector=vectors, payload={"course": course['title'], "id": f"{course['courseId']}{course['subjectCode']}{course['catalogNumber']}"}))
db.addPoints(points)


# Now we have to go through every single node in the database and add the relationships!
results = db.conn.execute("""
MATCH (n:Class)
RETURN n
""")
while results.has_next():
    node = results.get_next()
    # find all similarities
