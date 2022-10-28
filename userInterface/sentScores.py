from models import Students
from score_requests import selectScore


def sentScores():
    students = Students.objects.filter(is_subscribe=True, is_exist=True).order_by("priority")
    zkzhs = []
    for s in students:
        selectScore(s.zkzh, s.student_name)
    
