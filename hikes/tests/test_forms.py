# -*- coding: utf-8 -*-

from django.test import TestCase

from hikes.models import Region
from hikes.forms import TrailheadForm, HikeForm
from hikes.tests.factories import CountryRegionFactory


class HikesFormsTests(TestCase):

    def setUp(self):  # noqa
        self.co_region = CountryRegionFactory()

    def test_trailhead_form_clean(self):
        new_region_form = {'name': 'my new region trailhead',
                           'new_region': 'My New Region',
                           'co_region': self.co_region.slug}

        form1 = TrailheadForm(data=new_region_form)
        form1.is_valid()
        form1.clean()
        self.assertTrue(
            Region.objects.filter(name=new_region_form['new_region']).exists())

    def test_hike_init(self):
        form = HikeForm()
        self.assertEquals('Hike Name', form.fields['name'].label)
