import kuzu


class database():
    def __init__(self) -> None:
        db = kuzu.Database('./classDB')
        self.conn = kuzu.Connection(db)

    def createTables(self) -> None:
        self.conn.execute(
            "CREATE NODE TABLE Class(course_id STRING, title STRING, course_code STRING, grade INT64, associatedAcademicGroupCode STRING, associatedAcademicCareer STRING, description STRING, PRIMARY KEY (course_id))")
        self.conn.execute(
            "CREATE REL TABLE LeadsTo(FROM Class TO Class)")
        self.conn.execute("CREATE REL TABLE RelatedTo (FROM Class TO Class)")
        self.conn.execute(
            "CREATE REL TABLE prerequisite (FROM Class TO Class)")

    def addClass(self, class_object) -> None:
        query = f"""
        CREATE(n:Class {{
            course_id: '{class_object['courseId']}',
            title: '{class_object['title']}',
            course_code: '{class_object['subjectCode']}{class_object['catalogNumber']}',
            grade: {int(class_object['catalogNumber'][0])},
            associatedAcademicGroupCode: '{class_object['associatedAcademicGroupCode']}',
            associatedAcademicCareer: '{class_object['associatedAcademicCareer']}',
            description: 'test'
        }})
        RETURN n;
        """
        try:
            self.conn.execute(query)
            print(f"Added class {class_object['title']} to database")
        except:
            print(f"Error adding class {class_object['title']} to database")
            return
