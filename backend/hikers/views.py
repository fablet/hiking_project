# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.views.generic import (DetailView, ListView, UpdateView,
                                  TemplateView, RedirectView)

from hikers.forms import (HikerBasicInfoForm, HikerStatsForm, HikerAddressForm,
                          HikerDiaryForm, HikerPhotoForm)
from hikers.models import (Hiker, HikerAddress, HikerDiaryEntry, HikerPhoto,
                           FutureHike, MyHike)
from hikers.utils import (HikerCreateView, HikerUpdateView, HikerDeleteView,
                          get_hiker)
from mixins.permission_mixins import HikerAccessMixin, ProfileAccessMixin


class HikerProfileView(ProfileAccessMixin, DetailView):
    """View for displaying a Hiker'sbasic profile information."""
    model = Hiker
    template_name = 'hikers/hiker_profile.html'
    slug_url_kwarg = 'user_slug'
    context_object_name = 'hiker'
    queryset = Hiker.objects.prefetch_related(
        'address').select_related('hiker')


class HikerBasicInfoUpdateView(ProfileAccessMixin, UpdateView):
    model = Hiker
    template_name = 'forms/photo_forms.html'
    slug_url_kwarg = 'user_slug'
    queryset = Hiker.objects.select_related('hiker')
    form_class = HikerBasicInfoForm


class HikerStatsUpdateView(ProfileAccessMixin, UpdateView):
    model = Hiker
    template_name = 'forms/basic_form.html'
    slug_url_kwarg = 'user_slug'
    form_class = HikerStatsForm


class HikerAddressUpdateView(ProfileAccessMixin, UpdateView):
    model = HikerAddress
    template_name = 'forms/basic_form.html'
    form_class = HikerAddressForm
    slug_field = 'hiker__slug'
    slug_url_kwarg = 'user_slug'


class HikerDiaryEntriesView(ProfileAccessMixin, ListView):
    """View for displaying all diary entries by current user."""
    model = HikerDiaryEntry
    template_name = 'hikers/hiker_diaries.html'
    context_object_name = 'diaries'
    hiker = None

    def get_queryset(self):
        """Filter queryset to only return diaries for the user profile defined
        by url kwargs. ProfileAccessMixin handles bad user_slug.
        :return: queryset of diary entries made by current hiker.
        """
        self.hiker = Hiker.objects.get(slug=self.kwargs['user_slug'])
        return HikerDiaryEntry.objects.filter(
            hiker=self.hiker).prefetch_related(
            'diary_photos').select_related('hike')


class HikerDairyEntryCreateView(ProfileAccessMixin, HikerCreateView):
    model = HikerDiaryEntry
    form_class = HikerDiaryForm
    template_name = 'forms/basic_form.html'


class HikerDairyEntryUpdateView(ProfileAccessMixin, HikerUpdateView):
    model = HikerDiaryEntry
    form_class = HikerDiaryForm
    template_name = 'forms/basic_form.html'
    slug_url_kwarg = 'diary_slug'


class HikerDairyEntryDeleteView(ProfileAccessMixin, HikerDeleteView):
    model = HikerDiaryEntry
    template_name = 'hikers/delete.html'
    slug_url_kwarg = 'diary_slug'
    success_url_name = 'hikers:diaries'


class HikerPhotosView(ProfileAccessMixin, ListView):
    """View for displaying all photos by current user."""
    model = HikerPhoto
    template_name = 'hikers/hiker_photos.html'
    context_object_name = 'photos'
    hiker = None

    def get_queryset(self):
        """Filter queryset to only return photos for the user profile defined
        by url kwargs. ProfileAccessMixin handles bad user_slug.
        :return: queryset of current hiker photos.
        """
        self.hiker = Hiker.objects.get(slug=self.kwargs['user_slug'])
        return HikerPhoto.objects.filter(
            hiker=self.hiker).select_related('diary_entry', 'hike')


class HikerPhotosCreateView(ProfileAccessMixin, HikerCreateView):
    # todo: add method to select hike from diary_entry. client side??
    model = HikerPhoto
    form_class = HikerPhotoForm
    template_name = 'forms/photo_forms.html'

    def get_form(self, form_class=None):
        form = super(HikerPhotosCreateView, self).get_form(form_class)
        hiker = get_hiker(self.request.user)
        form.fields['diary_entry'].queryset = HikerDiaryEntry.objects.filter(
            hiker=hiker)
        return form


class HikerPhotosUpdateView(ProfileAccessMixin, HikerUpdateView):
    model = HikerPhoto
    form_class = HikerPhotoForm
    template_name = 'forms/photo_forms.html'
    slug_url_kwarg = 'photo_slug'

    def get_form(self, form_class=None):
        form = super(HikerPhotosUpdateView, self).get_form(form_class)
        hiker = get_hiker(self.request.user)
        form.fields['diary_entry'].queryset = HikerDiaryEntry.objects.filter(
            hiker=hiker)
        return form


class HikerPhotoDeleteView(ProfileAccessMixin, HikerDeleteView):
    model = HikerPhoto
    template_name = 'hikers/delete.html'
    slug_url_kwarg = 'photo_slug'
    success_url_name = 'hikers:photos'


class HikerHikesView(ProfileAccessMixin, ListView):
    """View for displaying all hikes by current user including those marked as
    future hikes."""
    model = MyHike
    template_name = 'hikers/hiker_hikes.html'
    context_object_name = 'hikes'
    future_hikes = None
    hiker = None

    def get_queryset(self):
        """Filter queryset to only return hikes for the user profile defined
        by url kwargs. ProfileAccessMixin handles bad user_slug.
        :return: queryset of rated hikes by current hiker.
        """
        self.hiker = Hiker.objects.get(slug=self.kwargs['user_slug'])
        self.future_hikes = FutureHike.objects.filter(hiker=self.hiker
                                                      ).select_related('hike')
        return MyHike.objects.filter(
            hiker=self.hiker).select_related('hike')


class ProfileRedirect(HikerAccessMixin, TemplateView):
    """View to offer redirection options for users attempting to access a
    hiker profile other than their own.
    """
    template_name = 'hikers/hiker_redirect.html'


class InactiveRedirect(TemplateView):
    """View to offer redirection options for inactive users attempting to
    access views that require active, authenticated accounts.
    """

    system_admin_email = getattr(settings, 'ADMINS', None)
    system_admin_email = system_admin_email[0][1] if system_admin_email else ''
    template_name = 'hikers/inactive_redirect.html'


class ProfileIndexRedirect(HikerAccessMixin, RedirectView):
    """View to redirect selections of hikers or hikers/profile to logged in
    user's profile, or login.
    """
    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('hikers:profile',
                            kwargs={'user_slug': self.request.user.hiker.slug})


class PermissionDeniedRedirect(HikerAccessMixin, TemplateView):
    """View to offer redirection options for users attempting to access a
    hiker profile other than their own.
    """
    template_name = 'hikers/denied_redirect.html'