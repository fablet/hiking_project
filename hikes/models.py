# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import SlugifiedNameBase


class Region(SlugifiedNameBase):
    """Class for holding list of Regions: ie: 'Oregon Coast', 'Columbia Gorge'.
    """
    name = models.CharField(max_length=50, unique=True)
    num_trailheads = models.IntegerField(default=1)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Trailhead(SlugifiedNameBase):
    """Class for capturing base information about trailheads, the places where
    hikes start. presumptively the best approximation of parking locations.
    """
    region = models.ForeignKey(Region, on_delete=models.CASCADE,
                               related_name='trailheads')
    name = models.CharField(max_length=200)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    num_hikes = models.IntegerField(default=1)

    class Meta:
        ordering = ['region', '-num_hikes']
        unique_together = ('region', 'name')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Trailhead, self).save(*args, **kwargs)
        trailhead_count = Trailhead.objects.filter(region=self.region).count()
        self.region.num_trailheads = trailhead_count
        self.region.save()

    # def miles_from_user(self):
    #     pass
    #
    # def hours_from_user(self):
    #     pass


class Hike(SlugifiedNameBase):
    """Class for capturing hike specific details."""
    DIFFICULTY = (
        ('0easy', _('Easy')),
        ('1moderate', _('Moderate')),
        ('2difficult', _('Difficult')),
    )
    HIKE_TYPES = (
        ('loop', _('Loop')),
        ('out_and_back', _('Out and Back')),
        ('lollipop', _('Lollipop/Dog Bone')),
        ('point_to_point', _('Point-to-Point/Destination')),
    )
    trailhead = models.ForeignKey(Trailhead, on_delete=models.CASCADE,
                                  related_name='hikes')
    name = models.CharField(max_length=180, unique=True)

    hike_type = models.CharField(max_length=50, default='loop',
                                 choices=HIKE_TYPES)
    description = models.TextField()

    # likes = models.IntegerField(default=0) - move to popularity/reviews app?
    trail_map = models.FileField(upload_to='trail_maps', blank=True)

    # specs
    difficulty_level = models.CharField(max_length=20, default="0easy",
                                        choices=DIFFICULTY)
    difficulty_level_explanation = models.CharField(max_length=250, blank=True)
    distance = models.FloatField(default=0.0)
    elevation = models.IntegerField(default=0)
    high_point = models.IntegerField(default=0)

    class Meta:
        ordering = ['difficulty_level', 'distance']
        unique_together = ('trailhead', 'name')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Hike, self).save(*args, **kwargs)
        hike_count = Hike.objects.filter(trailhead=self.trailhead).count()
        self.trailhead.num_hikes = hike_count
        self.trailhead.save()
