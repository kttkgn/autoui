from app.crud.base import CRUDBase
from app.models.testcase import TestCase
from app.schemas.project import TestCaseCreate, TestCaseUpdate

testcase_crud = CRUDBase[TestCase, TestCaseCreate, TestCaseUpdate](TestCase) 