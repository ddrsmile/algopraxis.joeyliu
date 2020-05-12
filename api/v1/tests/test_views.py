# -*- coding: utf-8 -*-
import random

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import QuerySet
from rest_framework.test import APIClient

from api.models import (
    Difficulty,
    LangMode,
    InputType,
    ParserType,

    Problem,
    CodeSet,
    Solution,
)


class APIViewTest(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super(APIViewTest, cls).setUpClass()
        cls.client = APIClient()

    @classmethod
    def tearDownClass(cls) -> None:
        super(APIViewTest, cls).tearDownClass()

    @classmethod
    def setUpTestData(cls) -> None:
        cls.admin_user = User.objects.create(username='admin_user', is_superuser=True)
        cls.admin_user.set_password('admin_user')
        cls.admin_user.save()
        cls.member_user = User.objects.create(username='member_user',)
        cls.member_user.set_password('member_user')
        cls.member_user.save()

        # create 5 problems
        for i in range(1, 6):
            p = Problem.objects.create(
                title=f'test title {i}',
                description=f'test description {i}',
                difficulty=random.choice(Difficulty.values),
                parser_type=random.choice(ParserType.values),
                input_type=random.choice(InputType.values),
                test_case=f'test case {i}'
            )
            p.tags.add(f'tag{i}')

            # leave 5th problem for the operations
            if i == 5:
                break

            nums = random.choice(range(len(LangMode.values)))
            # ensure 1st and 2nd has the solutions of admin user and member user respectively.
            if i == 1 or i == 2:
                nums = nums or nums + 1

            for n in range(1, nums+1):
                user = cls.admin_user if i % 2 == 1 else cls.member_user
                lang_mode = n
                CodeSet.objects.create(
                    problem=p,
                    lang_mode=lang_mode,
                    start_code=f'test start code for {lang_mode} of problem {i}'
                )
                Solution.objects.create(
                    problem=p,
                    user=user,
                    lang_mode=lang_mode,
                    code=f'test code for {lang_mode} of problem {i} by user {user.username}'
                )

    def tearDown(self) -> None:
        self.client.logout()

    def compare_children(self, qs: QuerySet, json_list: list) -> None:
        self.assertEqual(qs is not None, json_list is not None)
        self.assertEqual(len(qs), len(json_list))
        for obj, json in zip(qs, json_list):
            for key, val in json.items():
                self.assertEqual(val, getattr(obj, key))

    def test_problem_list_api_view(self) -> None:
        resp = self.client.get(reverse('api:v1:problem_list'))
        data = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['count'], Problem.objects.count())
        self.assertIsNone(data['next'])
        self.assertIsNone(data['prev'])
        self.assertEqual(data['page_range'], [1])

    def test_problem_list_api_view_pagination_param(self) -> None:
        resp = self.client.get(reverse('api:v1:problem_list') + '?page_size=2&page=2')
        data = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['count'], Problem.objects.count())
        self.assertEqual(data['next'], 3)
        self.assertEqual(data['prev'], 1)
        self.assertEqual(data['page_range'], [1, 2, 3])

    def test_problem_detail_api_view_anonymous(self) -> None:
        problem_id = random.choice(range(1, 5))
        resp = self.client.get(reverse('api:v1:problem_detail', kwargs={'pk': problem_id}))
        data = resp.json()
        self.compare_children(CodeSet.objects.filter(problem_id=problem_id).all(), data.get('code_sets'))
        self.compare_children(Solution.objects.filter(problem_id=problem_id, user_id=None).all(),
                              data.get('solutions'))

    def test_problem_detail_api_view_with_own_solution(self) -> None:
        problem_id = 1
        self.client.login(username='admin_user', password='admin_user')
        resp = self.client.get(reverse('api:v1:problem_detail', kwargs={'pk': problem_id}))
        data = resp.json()

        self.compare_children(CodeSet.objects.filter(problem_id=problem_id).all(), data.get('code_sets'))
        self.compare_children(Solution.objects.filter(problem_id=problem_id, user_id=self.admin_user.id).all(),
                              data.get('solutions'))

    def test_problem_detail_api_view_without_own_solution(self) -> None:
        problem_id = 2
        self.client.login(username='admin_user', password='admin_user')
        resp = self.client.get(reverse('api:v1:problem_detail', kwargs={'pk': problem_id}))
        data = resp.json()

        self.compare_children(CodeSet.objects.filter(problem_id=problem_id).all(), data.get('code_sets'))
        self.compare_children(Solution.objects.filter(problem_id=problem_id, user_id=self.admin_user.id).all(),
                              data.get('solutions'))

    def test_code_test_creation_api_view_integrity_check(self) -> None:
        resp = self.client.post(reverse('api:v1:code_set_create'),
                                data={'problem_id': 5, 'lang_mode': 1, 'start_code': 'test start code'},
                                content_type='application/json')
        self.assertEqual(resp.status_code, 201)

        resp = self.client.post(reverse('api:v1:code_set_create'),
                                data={'problem_id': 5, 'lang_mode': 1, 'start_code': 'test start code'},
                                content_type='application/json')
        self.assertEqual(resp.status_code, 400)

    def test_execute_api_view_success(self) -> None:
        resp = self.client.post(reverse('api:v1:execute'),
                                data={
                                    'problem_id': 5,
                                    'lang_mode': 1,
                                    'code': 'test start code',
                                    'inputs': 'test inputs'
                                },
                                content_type='application/json')
        self.assertEqual(resp.status_code, 200)

    def test_solution_api_view_permission_read_only(self) -> None:
        resp = self.client.get(reverse('api:v1:solution_rud', kwargs={'pk': 1}))
        self.assertEqual(resp.status_code, 200)

    def test_solution_api_view_update_anonymous(self) -> None:
        resp = self.client.put(reverse('api:v1:solution_rud', kwargs={'pk': 1}),
                               data={
                                   'id': 1,
                                   'lang_mode': 1,
                                   'code': 'updated test code',
                               },
                               content_type='application/json')
        self.assertEqual(resp.status_code, 403)

    def test_solution_api_view_update_others(self) -> None:
        self.client.login(username='admin_user', password='admin_user')
        others = Solution.objects.filter(user_id=self.member_user.id).first()
        resp = self.client.put(reverse('api:v1:solution_rud', kwargs={'pk': others.id}),
                               data={
                                   'id': others.id,
                                   'lang_mode': others.lang_mode,
                                   'code': 'updated test code',
                               },
                               content_type='application/json')
        self.assertEqual(resp.status_code, 403)

    def test_solution_api_view_update_own(self) -> None:
        self.client.login(username='admin_user', password='admin_user')
        own = Solution.objects.filter(user_id=self.admin_user.id).first()
        resp = self.client.put(reverse('api:v1:solution_rud', kwargs={'pk': own.id}),
                               data={
                                   'id': own.id,
                                   'lang_mode': own.lang_mode,
                                   'code': 'updated test code',
                               },
                               content_type='application/json')
        updated = Solution.objects.get(id=own.id)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(updated.code, 'updated test code')

    def test_execute_api_view_validation_fail(self) -> None:
        resp = self.client.post(reverse('api:v1:execute'),
                                data={
                                    'problem_id': 5,
                                    'lang_mode': len(LangMode.values) + 1,
                                    'code': 'test start code',
                                    'inputs': 'test inputs'
                                },
                                content_type='application/json')
        self.assertEqual(resp.status_code, 400)
