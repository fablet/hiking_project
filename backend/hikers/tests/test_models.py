# -*- coding: utf-8 -*-

# Imports from Django
from django.core.exceptions import ValidationError
from django.test import TestCase

# Imports from Third Party Modules
from datetime import datetime

# Local Imports
from hikes.tests.factories import HikeFactory

# Local imports
from ..models import FutureHike, Hiker, HikerDiaryEntry, HikerPhoto, MyHike
from .factories import (
    FutureHikeFactory,
    HikerAddressFactory,
    HikerDiaryEntryFactory,
    HikerFactory,
    HikerPhotoFactory,
    MyHikeFactory,
)


class HikerModelsTests(TestCase):

    def setUp(self):  # noqa
        self.test_hike = HikeFactory()
        self.test_hiker = HikerFactory()

    def test_hiker_unicode(self):
        self.assertIsInstance(self.test_hiker, Hiker)
        self.assertEquals(self.test_hiker.hiker.username,
                          self.test_hiker.__str__())

    def test_diary_unicode(self):
        date_fmt = '%Y-%m-%d'
        diary0 = HikerDiaryEntryFactory(hike=self.test_hike)
        self.assertIsInstance(diary0, HikerDiaryEntry)
        self.assertIn(diary0.title, diary0.__str__())
        self.assertIn(diary0.hike.name, diary0.__str__())

        diary1 = HikerDiaryEntryFactory()
        self.assertIn(diary1.title, diary1.__str__())
        self.assertIn(diary1.created.strftime(date_fmt), diary1.__str__())

        diary2 = HikerDiaryEntryFactory(title='', hike=self.test_hike)
        self.assertIn(diary2.hike.name, diary2.__str__())
        self.assertIn(diary2.created.strftime(date_fmt), diary2.__str__())

        diary3 = HikerDiaryEntryFactory(title='')
        self.assertEquals(diary3.created.strftime(date_fmt),
                          diary3.__str__())

    def test_photo_unicode(self):
        date_fmt = '%Y-%m-%d'
        photo0 = HikerPhotoFactory(hike=self.test_hike)
        self.assertIsInstance(photo0, HikerPhoto)
        self.assertIn(photo0.title, photo0.__str__())
        self.assertIn(photo0.hike.name, photo0.__str__())

        photo1 = HikerPhotoFactory()
        self.assertIn(photo1.title, photo1.__str__())
        self.assertIn(photo1.created.strftime(date_fmt), photo1.__str__())

        photo2 = HikerPhotoFactory(title='', hike=self.test_hike)
        self.assertIn(photo2.hike.name, photo2.__str__())
        self.assertIn(photo2.created.strftime(date_fmt), photo2.__str__())

        photo3 = HikerPhotoFactory(title='')
        self.assertIn(photo3.created.strftime(date_fmt), photo3.__str__())

    def test_future_hike_unicode(self):
        future_hike = FutureHikeFactory(hike=self.test_hike,
                                        hiker=self.test_hiker)
        self.assertIsInstance(future_hike, FutureHike)
        self.assertEquals(future_hike.hike.name, future_hike.__str__())

    def test_my_hike_unicode(self):
        my_hike = MyHikeFactory(hike=self.test_hike, hiker=self.test_hiker,
                                rating='0never', last_hiked=None)
        self.assertIsInstance(my_hike, MyHike)
        self.assertIn(my_hike.hike.name, my_hike.__str__())
        self.assertIn(my_hike.rating, my_hike.__str__())

    def test_my_hike_update_future(self):
        FutureHike.objects.all().delete()
        my_hike = MyHike(hike=self.test_hike, hiker=self.test_hiker,
                         rating='0never')
        self.assertFalse(FutureHike.objects.filter(
            hike=self.test_hike, hiker=self.test_hiker).exists())
        my_hike.update_future_hikes()
        self.assertTrue(FutureHike.objects.filter(
            hike=self.test_hike, hiker=self.test_hiker).exists())
        my_hike.rating = '1loved'
        my_hike.last_hiked = datetime.today()
        my_hike.update_future_hikes()
        self.assertFalse(FutureHike.objects.filter(
            hike=self.test_hike, hiker=self.test_hiker).exists())

    def test_validate_last_hiked(self):
        forgot_date = MyHike(hike=self.test_hike, hiker=self.test_hiker,
                             rating='6hated')
        never_hiked = MyHike(hike=self.test_hike, hiker=self.test_hiker,
                             rating='0never', last_hiked=datetime.today())
        with self.assertRaises(ValidationError):
            forgot_date.last_hiked_validator()
        with self.assertRaises(ValidationError):
            never_hiked.last_hiked_validator()

    def test_absolute_urls(self):
        address = HikerAddressFactory(hiker=self.test_hiker)
        diary = HikerDiaryEntryFactory(hiker=self.test_hiker)
        photo = HikerPhotoFactory(hiker=self.test_hiker)
        future_hike = FutureHikeFactory(hiker=self.test_hiker)
        myhike = MyHikeFactory(hiker=self.test_hiker)
        self.assertIn(self.test_hiker.slug, address.get_absolute_url())
        self.assertIn(self.test_hiker.slug, diary.get_absolute_url())
        self.assertIn(self.test_hiker.slug, photo.get_absolute_url())
        self.assertIn(self.test_hiker.slug, future_hike.get_absolute_url())
        self.assertIn(self.test_hiker.slug, myhike.get_absolute_url())
        self.assertIn(self.test_hiker.slug, self.test_hiker.get_absolute_url())

    def test_delete_urls(self):
        diary = HikerDiaryEntryFactory(hiker=self.test_hiker)
        photo = HikerPhotoFactory(hiker=self.test_hiker)
        self.assertIn(self.test_hiker.slug, diary.get_delete_url())
        self.assertIn(self.test_hiker.slug, photo.get_delete_url())
        self.assertIn(diary.slug, diary.get_delete_url())
        self.assertIn(photo.slug, photo.get_delete_url())
        new_diary = HikerDiaryEntry()
        new_photo = HikerPhoto()
        self.assertIsNone(new_diary.get_delete_url())
        self.assertIsNone(new_photo.get_delete_url())
