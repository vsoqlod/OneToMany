# course.py
from orm_base import Base
from sqlalchemy import Integer, UniqueConstraint, ForeignKeyConstraint
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from Department import Department
from typing import List
# from Sections import Sections


class Course(Base):
    __tablename__ = "courses"  # Give SQLAlchemy th name of the table.
    department_abbreviation: Mapped[str] = mapped_column('department_abbreviation', String(10), primary_key=True)
    course_number: Mapped[int] = mapped_column('course_number', Integer, nullable=False, primary_key=True)
    name: Mapped[str] = mapped_column('name', String(50), nullable=False)
    description: Mapped[str] = mapped_column('description', String(500), nullable=False)
    units: Mapped[int] = mapped_column('units', Integer, nullable=False)
    sections: Mapped[List["Sections"]] = relationship(back_populates="courses")
    department: Mapped["Department"] = relationship(back_populates="courses")

    __table_args__ = (UniqueConstraint("department_abbreviation", "name", name="courses_uk_01"),
                      ForeignKeyConstraint([department_abbreviation],
                                           [Department.abbreviation]))

    def __init__(self, department: Department, course_number: int, name: str, description: str, units: int):
        self.set_department(department)
        self.course_number = course_number
        self.name = name
        self.description = description
        self.units = units

    def set_department(self, department: Department):
        """
        Accept a new department withoug checking for any uniqueness.
        I'm going to assume that either a) the caller checked that first
        and/or b) the database will raise its own exception.
        :param department:  The new department for the course.
        :return:            None
        """
        self.department = department
        self.department_abbreviation = department.abbreviation

    def add_sections(self, sections):
        if sections not in self.sections:
            self.sections.add(sections)

    def remove_sections(self, sections):
        if sections in self.sections:
            self.sections.remove(sections)

    def get_sections(self):
        return self.sections

    def __str__(self):
        return f"Department abbrev: {self.department_abbreviation} number: {self.course_number} name: {self.name} units: {self.units}"
