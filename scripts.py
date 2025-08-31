import random
from datacenter.models import Schoolkid, Mark, Chastisement, Commendation, Lesson


def get_schoolkid(name):
    try:
        return Schoolkid.objects.get(full_name__icontains=name)
    except Schoolkid.DoesNotExist:
        print("Ученик не найден. Уточните ФИО.")
    except Schoolkid.MultipleObjectsReturned:
        print("Найдено несколько учеников. Укажите ФИО полностью.")


def fix_marks(schoolkid):
    Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]).update(points=5)


def remove_chastisements(schoolkid):
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(schoolkid, subject):
    commendations = ["Уже существенно лучше!", "Молодец!", "Отлично!", "Хорошо!", "Гораздо лучше, чем я ожидал!", "Ты меня приятно удивил!", "Хвалю!", "Великолепно!", "Прекрасно!", "Ты, как всегда, точен!", "Очень хороший ответ!", "Так держать!"]
    lesson = random.choice(Lesson.objects.filter(group_letter=schoolkid.group_letter, year_of_study=schoolkid.year_of_study, subject__title__contains=subject).order_by("-date"))
    Commendation.objects.create(text=random.choice(commendations), created=lesson.date, schoolkid=schoolkid, subject=lesson.subject, teacher=lesson.teacher)


def run_all(name, subject):
    schoolkid = get_schoolkid(name)
    if not schoolkid:
        return
    fix_marks(schoolkid)
    remove_chastisements(schoolkid)
    create_commendation(schoolkid, subject)


