from django.test import TestCase
from apps.tasks.models import (Tag, Project, ProjectFile, Task, Status, Priorities)
from django.core.files.base import ContentFile
from django.utils import timezone
from django.db.models import Q, F, Count, Max, Avg, ExpressionWrapper
from django.db.models.functions import ExtractWeekDay, ExtractIsoWeekDay
from datetime import datetime, timedelta
from faker import Faker
import random
from django.contrib.auth import get_user_model
import calendar
from django.core.paginator import Paginator

class TestTag(TestCase):

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.create_db()

    def setUp(self):
        self.create_db()

    @staticmethod
    def create_db():
        now = timezone.now()
        _, last_day = calendar.monthrange(now.year, now.month)
        User = get_user_model()
        User.objects.create(first_name='da', last_name='das', username='das')
        all_statuses = [choice.value for choice in Status]
        all_priorities = [choice.value for choice in Priorities]
        all_users = [user for user in User.objects.all()]
        Tag.objects.create(name='Разработка UI-кита и редизайн макета')
        Tag.objects.create(name='Настройка CI/CD, после сконфигурировать Docker')
        tag_1 = Tag(name='Backend')
        tag_2 = Tag(name='Frontend')
        tag_3 = Tag(name='Q&A')
        tag_4 = Tag(name='Design')
        tag_5 = Tag(name='DevOPS')
        Tag.objects.bulk_create([tag_1, tag_2, tag_3, tag_4, tag_5])
        fake = Faker()
        projects = [Project(name=fake.unique.word(),
                            description=fake.paragraph(nb_sentences=random.randint(2, 5)),
                            created_at=timezone.now())
                    for _ in range(10)]
        projects += [Project(name='New titanic project :D',
                          description='blablabla'),
                  Project(name='Another titanic',
                          description='blabla')]
        Project.objects.bulk_create(projects)
        for project in Project.objects.filter(name='Another titanic'):
            for i in range(5):
                our_file = ProjectFile(name=f'file_{i}.txt')
                our_file.file.save(f'file_{i}.txt',
                                   ContentFile(fake.paragraph(nb_sentences=random.randint(2, 5))),
                                   save=True)
                our_file.save()
                project.files.add(our_file)
                project.save()
        for project in Project.objects.all():
            for tag in Tag.objects.all():
                task = Task.objects.create(title=fake.unique.word(),
                                    description=fake.paragraph(nb_sentences=random.randint(2, 5)),
                                    status=random.choice(all_statuses),
                                    priority=random.choice(all_priorities),
                                    project=project,
                                    assignee=random.choice(all_users),
                                    deadline=timezone.now() + timedelta(days=random.randint(1, last_day))
                                    )
                task.tags.add(tag)
                task.save()
        another_task = Task.objects.create(title=fake.unique.word(),
                            description=fake.paragraph(nb_sentences=random.randint(2, 5)),
                            status=Status.NEW,
                            priority=Priorities.URGENT,
                            project=projects[0],
                            assignee=random.choice(all_users),
                            deadline=timezone.now() + timedelta(days=last_day)
                            )
        another_task.tags.add(tag_1)
        another_task.save()
        another_task = Task.objects.create(title=fake.unique.word(),
                                           description=fake.paragraph(nb_sentences=random.randint(2, 5)),
                                           status=Status.IN_PROGRESS,
                                           priority=Priorities.URGENT,
                                           project=projects[0],
                                           assignee=random.choice(all_users),
                                           deadline=timezone.now() + timedelta(days=last_day)
                                           )
        another_task.tags.add(tag_1)
        another_task.save()
        another_task = Task.objects.create(title=fake.unique.word(),
                                           description=fake.paragraph(nb_sentences=random.randint(2, 5)),
                                           status=Status.IN_PROGRESS,
                                           priority=Priorities.URGENT,
                                           project=projects[-2],
                                           assignee=random.choice(all_users),
                                           deadline=timezone.now() + timedelta(days=last_day),
                                           # created_at=timezone.now() - timedelta(weeks=5)
                                           )
        another_task.tags.add(tag_1)
        another_task.created_at = timezone.now() - timedelta(weeks=5)
        another_task.save()


    def test_tag_by_name(self):
        # self.create_db()
        self.assertEqual(Tag.objects.filter(name='Разработка UI-кита и редизайн макета').count(), 1)

    def test_tag_by_specific_tag(self):
        # self.create_db()
        self.assertEqual(Tag.objects.filter(name__icontains='de').count(), 2)

    def test_projects_by_date(self):
        # self.create_db()
        naive_date = datetime(year=2026, month=1, day=1)
        above_date = timezone.make_aware(naive_date)
        self.assertEqual(Project.objects.filter(created_at__gte=above_date).count(), Project.objects.all().count())

    def test_gte_or_contains_ti(self):
        # self.create_db()
        naive_date = datetime(year=2026, month=1, day=1)
        above_date = timezone.make_aware(naive_date)
        self.assertGreaterEqual(Project.objects.filter(Q(created_at__gte=above_date) & Q(name__icontains='ti')).count(), 2)

    def test_5_files_in_pr(self):
        # self.create_db()
        self.assertEqual(Project.objects.get(name='Another titanic').files.all().count(), 5)

    def test_st_new_pr_urg(self):
        # self.create_db()
        self.assertGreaterEqual(Task.objects.filter(status=Status.NEW, priority=Priorities.URGENT).count(), 1)

    def test_specific_task(self):
        task = Task.objects.all().first()
        task.status = Status.PENDING
        task.save()
        self.assertEqual(Task.objects.get(id = task.id).status, Status.PENDING)

    def test_st_pr_or_not_tag(self):
        self.assertGreaterEqual(Task.objects.filter(Q(status=Status.NEW, priority=Priorities.URGENT) | ~Q(tags__name__in=['Backend'])).count(), 1)

    def test_update_st_next_month(self):
        self.assertEqual(Task.objects.filter(deadline__month=timezone.now().month + 1).count(), 3)
        self.assertEqual(Task.objects.filter(deadline__month=timezone.now().month + 1).update(priority=Priorities.CRITICAL), 3)

    def test_task_due_date_by_week(self):
        self.assertEqual(Task.objects.all().update(deadline=F('deadline') + timedelta(weeks=1)), Task.objects.all().count())

    def test_not_assigned(self):
        self.assertEqual(Task.objects.filter(assignee__isnull=True).count(), 0)

    def test_task_with_tag(self):
        self.assertEqual(Task.objects.filter(tags__name='Frontend').count(), 12)

    def test_projects_by_period(self):
        now = timezone.now()
        creation_date = now - timedelta(days=7)
        # Search approach via ProjectFile table:
        # all_files_names = {file.name for file in ProjectFile.objects.filter(created_at__gte=creation_date)}
        # Search approach via Project table:
        all_files_names = {file.name for project in Project.objects.filter(created_at__gte=creation_date) for file in project.files.all()}
        self.assertGreaterEqual(Project.objects.filter(files__name__in=all_files_names).count(), 1)

    def test_new_status(self):
        self.assertGreaterEqual(Task.objects.filter(status=Status.NEW).update(status=Status.IN_PROGRESS), 1)

    def test_mass_due_date(self):
        self.assertGreaterEqual(Task.objects.filter(status=Status.IN_PROGRESS).update(deadline=F('deadline') + timedelta(days=3)), 1)

    def test_mass_filter_by_date(self):
        yesterday = timezone.now() - timedelta(days=1)
        projects_many_files = Project.objects.annotate(files_count=Count('files')).filter(created_at__gt=yesterday, files_count__gte=5).count()
        self.assertGreaterEqual(projects_many_files, 1)
        print(projects_many_files)
        projects_max_files = Project.objects.annotate(max_files = Max('files')).all()
        print(projects_max_files)

    def test_critical_or_urgent(self):
        cur_date = timezone.now()
        _, last_day = calendar.monthrange(cur_date.year, cur_date.month)
        self.assertGreaterEqual(Task.objects.filter(Q(priority=Priorities.CRITICAL) | Q(priority=Priorities.URGENT) & Q(deadline__day__range =[cur_date.day, last_day])).count(), 1)

    def test_not_in_status(self):
        self.assertGreaterEqual(Task.objects.filter(~Q(status__in=[Status.PENDING, Status.CLOSED])).count(), 1)

    def test_upd_priority(self):
        one_month_ago = timezone.now() - timedelta(weeks=5)
        self.assertEqual(Task.objects.filter(project__name='New titanic project :D', created_at__lt=one_month_ago).update(priority=Priorities.CRITICAL), 1)

        #####################################################################################
        ## Practice 30.07.2026 ##############################################################

    def test_current_month(self):
        cur_date = timezone.now()
        for project in Project.objects.filter(created_at__gte=datetime(cur_date.year, cur_date.month, 1)):
            self.assertEqual(project.created_at.month, timezone.now().month)

    def test_files_per_week_day(self):
        cur_day = timezone.now().isoweekday()
        for projectfile in ProjectFile.objects.annotate(day_of_weak=ExtractIsoWeekDay('created_at')).filter(day_of_weak=cur_day):
            self.assertEqual(projectfile.created_at.isoweekday(), cur_day)

    def test_projects_all(self):
        self.assertGreater(Project.objects.all().count(), 1)

    def test_count_files_by_project(self):
        # self.assertEqual(ProjectFile.objects.values('projects__name').annotate(files_count=Count('id')).
        #                  values('projects__name', 'files_count').count(), 1)
        for project in Project.objects.values('name').annotate(files_count=Count('files__id')).values('name', 'files_count'):
            print(project['name'], project['files_count'])
            self.assertEqual(project['files_count'], Project.objects.get(name=project['name']).files.count())

    def test_avg_avg_tasks_quan(self):
        self.assertEqual(Project.objects.annotate(tasks_count=Count('tasks__id')).aggregate(avg_tasks=Avg('tasks_count'))['avg_tasks'], 7.25)

    def test_tasks_per_user(self):
        User = get_user_model()
        for user in User.objects.values('username').annotate(tasks_count=Count('tasks__id')).values('username', 'tasks_count'):
            print(f'Username: {user['username']}, tasks count: {user['tasks_count']}')
            self.assertEqual(user['tasks_count'], User.objects.get(username=user['username']).tasks.count())

    def test_sort_tasks(self):
        for task in Task.objects.order_by('priority', 'deadline').values('title', 'priority', 'deadline'):
            print(task)
            assert 'title' in task
            assert 'deadline' in task
            assert task['deadline'] is not None

    def test_sort_users_by_tasks(self):
        User = get_user_model()
        for user in (User.objects.values('username')
            .annotate(tasks_count=Count('tasks__id')).order_by('-tasks_count').values('username', 'tasks_count')):
            print(user)

    def test_all_tasks_with_pagination(self):
        all_tasks = Task.objects.all().values('title', 'status', 'priority', 'assignee__username').order_by('id')
        pagination = Paginator(all_tasks, per_page=10)
        # for page_number in range(1, pagination.num_pages + 1):
        for page_number in pagination.page_range:
            page = pagination.get_page(page_number)
            print(page)
            for task in page:
                print(task)
            print("-" * 50)