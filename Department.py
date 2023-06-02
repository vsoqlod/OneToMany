# department.py
from orm_base import Base
from sqlalchemy import Column, Integer, UniqueConstraint, Identity
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List  # Use this for the list of courses offered by the department

class Department(Base):
    __tablename__ = "departments"  # Give SQLAlchemy th name of the table.
    abbreviation: Mapped[str] = mapped_column('abbreviation', String(10),
                                              nullable=False, primary_key=True)
    name: Mapped[str] = mapped_column('name', String(50), nullable=False)
    courses: Mapped[List["Course"]] = relationship("Course", back_populates="department")
    chair_name: Mapped[str] = mapped_column('chair_name', String(80), nullable=False)
    building: Mapped[str] = mapped_column('building', String(10), nullable=False)
    office: Mapped[int] = mapped_column('office', Integer, nullable=False)
    description: Mapped[str] = mapped_column('description', String(80), nullable=False)

    __table_args__ = (
    UniqueConstraint("name", name="departments_uk_01"), UniqueConstraint("chair_name", name="departments_uk_02"),
    UniqueConstraint("building", name="departments_uk_03"), UniqueConstraint("office", name="departments_uk_04"),
    UniqueConstraint("description", name="departments_uk_05"))

    def __init__(self, name: str, abbreviation: str, chair_name: str, building: str, office: int, description: str):
        self.name = name
        self.abbreviation = abbreviation
        self.chair_name = chair_name
        self.building = building
        self.office = office
        self.description = description

    def add_course(self, course):
        if course not in self.courses:
            self.courses.add(course)

    def remove_course(self, course):
        if course in self.courses:
            self.courses.remove(course)

    def get_courses(self):
        return self.courses

    def __str__(self):
        return f"Department name: {self.name} \nAbbreviation: {self.abbreviation} \nChair name: {self.chair_name}," \
               f" \nBuilding: {self.building} \nOffice: {self.office} \nDescription: {self.description} \n# of sections: {len(self.course)}"