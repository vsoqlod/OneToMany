import logging
from menu_definitions import menu_main, debug_select
from db_connection import engine, Session
from orm_base import metadata
# Note that until you import your SQLAlchemy declarative classes, such as Student, Python
# will not execute that code, and SQLAlchemy will be unaware of the mapped table.
from Department import Department
from Course import Course
from Option import Option
from Menu import Menu
from Sections import Sections
from sqlalchemy import Time


def add_department(session: Session):

    unique_abbreviation: bool = False
    unique_chair_name: bool = False
    unique_room: bool = False
    unique_description: bool = False
    name: str = ''
    abbreviation: str = ''
    chair_name: str = ''
    building: str = ''
    office: int = 0
    description: str = ''

    # Note that there is no physical way for us to duplicate the student_id since we are
    # using the Identity "type" for studentId and allowing PostgreSQL to handle that.
    # See more at: https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-identity-column/
    while not unique_abbreviation or not unique_chair_name or not unique_room or not unique_description:
        name = input("Department name--> ")
        abbreviation = input("Abbreviation--> ")
        chair_name = input("Chair name--> ")
        building = input("Building name--> ")
        office = int(input("Office--> "))
        description = input("Description--> ")

        name_count: int = session.query(Department).filter(Department.name == name).count()
        unique_name = name_count == 0

        if not unique_name:
            print("We already have a department with that name.  Try again.")
        if unique_name:
            chair_name_count: int = session.query(Department).filter(Department.chair_name == chair_name).count()
            unique_chair_name = chair_name_count == 0
            if not unique_chair_name:
                print("We already have a department with name and that chair name.  Try again.")
            if unique_chair_name:
                abbreviation_count = session.query(Department).filter(Department.abbreviation == abbreviation).count()
                unique_abbreviation = abbreviation_count == 0
                if not unique_abbreviation:
                    print("We already have a department with that chair name and department abbreviation.  Try again.")
                if unique_abbreviation:
                    building_count: int = session.query(Department).filter(Department.building == building,
                                                                           Department.office == office).count()
                    unique_room = building_count == 0
                    if not unique_room:
                        print(
                            "We already have a department with that chair name, department abbreviation, and room."
                            "  Try again.")
                    if unique_room:
                        description_count: int = session.query(Department)\
                            .filter(Department.description == description).count()
                        unique_description = description_count == 0
                        if not unique_chair_name:
                            print(
                                "We already have a department with that chair name, department abbreviation, room,"
                                " and description.  Try again.")

    newDepartment = Department(name, abbreviation, chair_name, building, office, description)
    session.add(newDepartment)


def add_course(session: Session):
    """
    Prompt the user for the information for a new course and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    print("Which department offers this course?")
    department: Department = select_department(sess)
    unique_number: bool = False
    unique_name: bool = False
    unique_description: bool = False

    course_number: int = -1
    course_name: str = ''
    course_description: str = ''
    course_units: int = -1

    while not unique_number or not unique_name or not unique_description:
        course_name = input("Course full name--> ")
        course_number = int(input("Course number--> "))
        course_description = input('Please enter the course description--> ')

        course_name_count: int = session.query(Course).filter(Course.department_abbreviation == department.abbreviation,
                                                              Course.name == course_name).count()
        unique_name = course_name_count == 0
        if not unique_name:
            print("We already have a course by that name in that department.  Try again.")
        if unique_name:

            course_number_count: int = session.query(Course).filter(
                Course.department_abbreviation == department.abbreviation,
                Course.course_number == course_number).count()
            unique_number = course_number_count == 0
            if not unique_number:
                print("We already have a course in this department with that number.  Try again.")
            if unique_number:

                course_description_count: int = session.query(Course).filter(
                    Course.department_abbreviation == department.abbreviation,
                    Course.description == course_description).count()
                unique_description = course_description_count == 0
                if not unique_description:
                    print("We already have a course in this department with that description.  Try again.")

    course_units = int(input('How many units for this course--> '))
    course = Course(department, course_number, course_name, course_description, course_units)
    session.add(course)


def add_sections(session: Session):
    print("Which course offers this section?")
    course: Course = select_course(sess)  # department abb, course #

    unique_location: bool = False  # year, semester, schedule, start time, building, room
    unique_professor: bool = False  # year, semester, schedule, start time, instructor

    section_number: int = -1
    semester: str = ''
    section_year: int = -1
    building: str = ''
    room: int = -1
    schedule: str = ''
    start_time: Time = None
    instructor: str = ''

    while not unique_location or not unique_professor:
        section_number = int(input("Section number--> "))
        semester = input("Semester full name--> ")
        while semester != "Fall" and semester != "Spring" and semester != "Winter" and semester != "Summer I" and semester != " Summer II":
            print("Invalid semester option. Try again.")
            semester = input("Semester full name--> ")

        section_year = int(input("Section year --> "))
        building = input("Section building--> ")
        room = int(input("Section room--> "))
        schedule = input("Section schedule--> ")
        while schedule != 'MW' and schedule != 'TuTh' and schedule != "MWF" and schedule != "F" and schedule != "S":
            print("Invalid schedule option. Try again.")
            schedule = input("Section schedule--> ")

        start_time = input("Section start time--> ")
        instructor = input("Section instructor--> ")

        unique_location_count: int = session.query(Sections).filter(Sections.section_year == section_year,
                                                                   Sections.semester == semester,
                                                                   Sections.schedule == schedule,
                                                                   Sections.start_time == start_time,
                                                                   Sections.building == building,
                                                                   Sections.room == room).count()
        unique_location = unique_location_count == 0
        if not unique_location:
            print("We already have a section at that location.  Try again.")
        if unique_location:

            unique_professor_count: int = session.query(Sections).filter(Sections.section_year == section_year,
                                                                        Sections.semester == semester,
                                                                        Sections.schedule == schedule,
                                                                        Sections.start_time == start_time,
                                                                        Sections.instructor == instructor).count()
            unique_professor = unique_professor_count == 0
            if not unique_professor:
                print("An instructor is already teaching that section.  Try again.")

    section = Sections(course, section_number, semester, section_year, building, room, schedule, start_time, instructor)
    session.add(section)


def select_department(sess: Session) -> Department:
    """
    Prompt the user for a specific department by the department abbreviation.
    :param sess:    The connection to the database.
    :return:        The selected department.
    """
    found: bool = False
    abbreviation: str = ''
    while not found:
        abbreviation = input("Enter the department abbreviation--> ")
        abbreviation_count: int = sess.query(Department). \
            filter(Department.abbreviation == abbreviation).count()
        found = abbreviation_count == 1
        if not found:
            print("No department with that abbreviation.  Try again.")
    return_student: Department = sess.query(Department). \
        filter(Department.abbreviation == abbreviation).first()
    return return_student


def select_course(sess: Session) -> Course:
    """
    Select a course by the combination of the department abbreviation and course number.
    Note, a similar query would be to select the course on the basis of the department
    abbreviation and the course name.
    :param sess:    The connection to the database.
    :return:        The selected student.
    """
    found: bool = False
    department_abbreviation: str = ''
    course_number: int = -1
    while not found:
        department_abbreviation = input("Department abbreviation--> ")
        course_number = int(input("Course Number--> "))
        name_count: int = sess.query(Course).filter(Course.department_abbreviation == department_abbreviation,
                                                    Course.course_number == course_number).count()
        found = name_count == 1
        if not found:
            print("No course by that number in that department.  Try again.")
    course = sess.query(Course).filter(Course.department_abbreviation == department_abbreviation,
                                       Course.course_number == course_number).first()
    return course


def select_sections(sess: Session) -> Sections:
    """
    Select a course by the combination of the department abbreviation and course number.
    Note, a similar query would be to select the course on the basis of the department
    abbreviation and the course name.
    :param sess:    The connection to the database.
    :return:        The selected student.
    """
    found: bool = False
    section_year: int = -1
    semester: str = ''
    schedule: str = ''
    start_time: str = ''
    instructor: str = ''

    while not found:
        section_year = input("Section Year--> ")
        semester = input("Semester--> ")
        schedule = input("Schedule--> ")
        start_time = input("Start Time--> ")
        instructor = input("Instructor--> ")

        instructor_count: int = sess.query(Sections).filter(Sections.section_year == section_year,
                                                            Sections.semester == semester,
                                                            Sections.schedule == schedule,
                                                            Sections.start_time == start_time,
                                                            Sections.instructor == instructor).count()

        found = instructor_count == 1
        if not found:
            print("No section with that instructor in that course.  Try again.")
    sections = sess.query(Sections).filter(Sections.section_year == section_year, Sections.semester == semester,
                                           Sections.schedule == schedule, Sections.start_time == start_time,
                                           Sections.instructor == instructor).first()
    return sections


def delete_department(session: Session):
    """
    Prompt the user for a department by the abbreviation and delete it.
    :param session: The connection to the database.
    :return:        None
    """
    print("deleting a department")
    department = select_department(session)
    n_courses = session.query(Course).filter(Course.department_abbreviation == department.abbreviation).count()
    if n_courses > 0:
        print(f"Sorry, there are {n_courses} courses in that department.  Delete them first, "
              "then come back here to delete the department.")
    else:
        session.delete(department)


def delete_course(session: Session):
    """
    Prompt the user for a department by the abbreviation and delete it.
    :param session: The connection to the database.
    :return:        None
    """
    print("deleting a course")
    course = select_course(session)
    n_sections = session.query(Sections).filter(Sections.course_number == course.course_number).count()
    if n_sections > 0:
        print(f"Sorry, there are {n_sections} courses in that department.  Delete them first, "
              "then come back here to delete the department.")
    else:
        session.delete(course)


def delete_sections(session: Session):
    """
    Prompt the user for a department by the abbreviation and delete it.
    :param session: The connection to the database.
    :return:        None
    """
    print("deleting a section")
    old_section = select_sections(session)
    session.delete(old_section)


def list_departments(session: Session):
    """
    List all departments, sorted by the abbreviation.
    :param session:     The connection to the database.
    :return:            None
    """
    # session.query returns an iterator.  The list function converts that iterator
    # into a list of elements.  In this case, they are instances of the Student class.
    departments: [Department] = list(session.query(Department).order_by(Department.abbreviation))
    for department in departments:
        print(department)


def list_courses(sess: Session):
    """
    List all courses currently in the database.
    :param sess:    The connection to the database.
    :return:        None
    """
    # session.query returns an iterator.  The list function converts that iterator
    # into a list of elements.  In this case, they are instances of the Student class.
    courses: [Course] = list(sess.query(Course).order_by(Course.course_number))
    for course in courses:
        print(course)


# def move_course_to_new_department(sess: Session):
#     """
#     Take an existing course and move it to an existing department.  The course has to
#     have a department when the course is created, so this routine just moves it from
#     one department to another.
#
#     The change in department has to occur from the Course end of the association because
#     the association is mandatory.  We cannot have the course not have any department for
#     any time the way that we would if we moved it to a new department from the department
#     end.
#
#     Also, the change in department requires that we make sure that the course will not
#     conflict with any existing courses in the new department by name or number.
#     :param sess:    The connection to the database.
#     :return:        None
#     """
#     print("Input the course to move to a new department.")
#     course = select_course(sess)
#     old_department = course.department
#     print("Input the department to move that course to.")
#     new_department = select_department(sess)
#     if new_department == old_department:
#         print("Error, you're not moving to a different department.")
#     else:
#         # check to be sure that we are not violating the {departmentAbbreviation, name} UK.
#         name_count: int = sess.query(Course).filter(Course.departmentAbbreviation == new_department.abbreviation,
#                                                     Course.name == course.name).count()
#         unique_name = name_count == 0
#         if not unique_name:
#             print("We already have a course by that name in that department.  Try again.")
#         if unique_name:
#             # Make sure that moving the course will not violate the {departmentAbbreviation,
#             # course number} uniqueness constraint.
#             number_count = sess.query(Course). \
#                 filter(Course.departmentAbbreviation == new_department.abbreviation,
#                        Course.courseNumber == course.courseNumber).count()
#             if number_count != 0:
#                 print("We already have a course by that number in that department.  Try again.")
#             else:
#                 course.set_department(new_department)


def select_student_from_list(session):
    """
    This is just a cute little use of the Menu object.  Basically, I create a
    menu on the fly from data selected from the database, and then use the
    menu_prompt method on Menu to display characteristic descriptive data, with
    an index printed out with each entry, and prompt the user until they select
    one of the Students.
    :param session:     The connection to the database.
    :return:            None
    """
    # query returns an iterator of Student objects, I want to put those into a list.  Technically,
    # that was not necessary, I could have just iterated through the query output directly.
    students: [Department] = list(sess.query(Department).order_by(Department.lastName, Department.firstName))
    options: [Option] = []  # The list of menu options that we're constructing.
    for student in students:
        # Each time we construct an Option instance, we put the full name of the student into
        # the "prompt" and then the student ID (albeit as a string) in as the "action".
        options.append(Option(student.lastName + ', ' + student.firstName, student.studentId))
    temp_menu = Menu('Student list', 'Select a student from this list', options)
    # text_studentId is the "action" corresponding to the student that the user selected.
    text_studentId: str = temp_menu.menu_prompt()
    # get that student by selecting based on the int version of the student id corresponding
    # to the student that the user selected.
    returned_student = sess.query(Department).filter(Department.studentId == int(text_studentId)).first()
    # this is really just to prove the point.  Ideally, we would return the student, but that
    # will present challenges in the exec call, so I didn't bother.
    print("Selected student: ", returned_student)


def list_department_courses(sess):
    department = select_department(sess)
    dept_courses: [Course] = department.get_courses()
    print("Course for department: " + str(department))
    for dept_course in dept_courses:
        print(dept_course)

def list_courses_sections(sess):
    course = select_course(sess)
    course_sections: [Sections] = course.get_sections()
    print("Sections for course: " + str(course))
    for course_sections in course_sections:
        print(course_sections)


if __name__ == '__main__':
    print('Starting off')
    logging.basicConfig()
    # use the logging factory to create our first logger.
    # for more logging messages, set the level to logging.DEBUG.
    # logging_action will be the text string name of the logging level, for instance 'logging.INFO'
    logging_action = debug_select.menu_prompt()
    # eval will return the integer value of whichever logging level variable name the user selected.
    logging.getLogger("sqlalchemy.engine").setLevel(eval(logging_action))
    # use the logging factory to create our second logger.
    # for more logging messages, set the level to logging.DEBUG.
    logging.getLogger("sqlalchemy.pool").setLevel(eval(logging_action))

    metadata.drop_all(bind=engine)  # start with a clean slate while in development

    # Create whatever tables are called for by our "Entity" classes.
    metadata.create_all(bind=engine)

    with Session() as sess:
        main_action: str = ''
        while main_action != menu_main.last_action():
            main_action = menu_main.menu_prompt()
            print('next action: ', main_action)
            exec(main_action)
        sess.commit()
    print('Ending normally')
