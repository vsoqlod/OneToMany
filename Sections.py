from sqlalchemy import Column, Integer, String, Time, UniqueConstraint, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import text
from orm_base import Base
from typing import List
from Course import Course
from Department import Department


class Sections(Base):
    __tablename__ = 'sections'

    department_abbreviation: Mapped[str] = mapped_column('department_abbreviation', String(10), primary_key=True)
    course_number: Mapped[int] = mapped_column('course_number', Integer, primary_key=True)
    section_number: Mapped[int] = mapped_column('section_number', Integer, primary_key=True)
    semester: Mapped[str] = mapped_column('semester', String(10), nullable=False, primary_key=True,
                                          server_default=text("(CASE WHEN 1=0 THEN '' ELSE 'Fall' END)"))
    section_year: Mapped[int] = mapped_column('section_year', Integer, nullable=False, primary_key=True)
    building: Mapped[str] = mapped_column('building', String(6), nullable=False)
    room: Mapped[int] = mapped_column('room', Integer, nullable=False)
    schedule: Mapped[str] = mapped_column('schedule', String(6), nullable=False,
                                          server_default=text("(CASE WHEN 1=0 THEN '' ELSE 'MW' END)"))
    start_time: Mapped[Time] = mapped_column('start_time', Time, nullable = False)
    instructor: Mapped[str] = mapped_column('instructor', String(80), nullable=False)
    courses: Mapped[List["Course"]] = relationship(back_populates="sections")

    __table_args__ = (
        UniqueConstraint("section_year", "semester", "schedule", "start_time", "building", "room", name= "sections_uk_01"),
        UniqueConstraint("section_year", "semester", "schedule", "start_time", "instructor", name="sections_uk_02"),
        ForeignKeyConstraint([department_abbreviation, course_number], [Course.department_abbreviation, Course.course_number])
    )

    def __init__(self, course: Course, section_number: int, semester: str,
                 section_year: int, building: str, room: int, schedule: str, start_time: Time, instructor: str):
        self.set_course(course)
        self.section_number = section_number
        self.semester = semester
        self.section_year = section_year
        self.building = building
        self.room = room
        self.schedule = schedule
        self.start_time = start_time
        self.instructor = instructor

    def set_course(self, courses: Course):
        """
        Accept a new department withoug checking for any uniqueness.
        I'm going to assume that either a) the caller checked that first
        and/or b) the database will raise its own exception.
        :param department:  The new department for the course.
        :return:            None
        """
        self.courses = courses
        self.department_abbreviation = courses.department_abbreviation
        self.course_number = courses.course_number


    def __str__(self):
        return f"\nDepartment: {self.department_abbreviation}, \nCourse Number: {self.course_number}, " \
               f"\nSection Number: {self.section_number}, \nSemester: {self.semester}, \nSection Year: {self.section_year}," \
               f"\nBuilding: {self.building}, Room: {self.room}, \nSchedule: {self.schedule}," \
               f"\nStart Time: {self.start_time}, \nInstructor: {self.instructor}"
