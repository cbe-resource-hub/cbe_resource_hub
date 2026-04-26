from django.db import IntegrityError
from django.utils.html import strip_tags

from cms.models import Page, SiteSetting
from cms.tests.base import CMSBaseTestCase


class TestCMSPageCreation(CMSBaseTestCase):

    def test_page_creation(self):
        self.assertIsNotNone(self.page)
        self.assertEqual(self.page.slug, 'page-title')
        self.assertEqual(self.page.title, 'Page title')
        self.assertEqual(self.page.content, '<h2>Page content</h2>')
        self.assertEqual(self.page.is_published, True)

    def test_page_creation_with_meta_title(self):
        self.assertEqual(self.page.title, self.page.meta_title)

    def test_page_creation_with_meta_description(self):
        self.assertEqual(self.page.meta_description, strip_tags(self.page.content))

    def test_page_creation_with_slug_generation(self):
        self.page2 = Page.objects.create(
            title="Page title2",
            slug="",
        )
        self.assertEqual(self.page2.slug, 'page-title2')

    def test_page_creation_with_non_unique_slug(self):
        self.page3 = Page.objects.create(
            title="Page title",
            slug="",
        )
        self.assertEqual(self.page3.slug, 'page-title-1')
        self.page4 = Page.objects.create(
            title="Page title",
            slug="",
        )
        self.assertEqual(self.page4.slug, 'page-title-2')

    def test_page_is_saved_with_is_published_as_false_by_default(self):
        self.page4 = Page.objects.create(
            title="Page title 4",
        )
        self.assertEqual(self.page4.is_published, False)

    def test_page_creation_with_duplicate_slug_throws_integrity_error(self):
        with self.assertRaises(IntegrityError):
            Page.objects.create(
                title="Page title 5",
                slug="page-title",
            )

    def test_page_creation_without_title_raises_error(self):
        with self.assertRaises(IntegrityError):
            Page.objects.create(
                title=None,
                slug="no-title-page",
            )

    def test_page_update_without_title_raises_error(self):
        with self.assertRaises(IntegrityError):
            Page.objects.filter(pk=self.page.pk).update(
                title=None,
            )

    def test_page_update_without_slug_raises_error(self):
        with self.assertRaises(IntegrityError):
            Page.objects.filter(pk=self.page.pk).update(
                slug=None,
            )

    def test_page_create_without_content_raises_error(self):
        with self.assertRaises(IntegrityError):
            Page.objects.create(
                title="No Content Page",
                content=None,
            )

    def test_page_update_without_content_raises_error(self):
        with self.assertRaises(IntegrityError):
            Page.objects.filter(pk=self.page.pk).update(
                content=None,
            )

    def test_page_create_without_is_published_raises_error(self):
        with self.assertRaises(IntegrityError):
            Page.objects.create(
                title="No is_published Page",
                is_published=None,
            )


class TestCMSSiteSettingsCreation(CMSBaseTestCase):

    def test_create_site_name_site_setting(self):
        self.assertIsNotNone(self.site_name_site_setting)

    def test_create_site_indexing_site_setting(self):
        self.assertIsNotNone(self.site_indexing_site_setting)

    def test_create_contact_phone_site_setting(self):
        self.assertIsNotNone(self.contact_phone_site_setting)

    def test_create_contact_email_site_setting(self):
        self.assertIsNotNone(self.contact_email_site_setting)

    def test_create_meta_description_site_setting(self):
        self.assertIsNotNone(self.meta_description_site_setting)

    def test_create_meta_keywords_site_setting(self):
        self.assertIsNotNone(self.meta_keywords_site_setting)

    def test_create_site_setting_with_duplicate_key_raises_integrity_error(self):
        with self.assertRaises(IntegrityError):
            SiteSetting.objects.create(
                key="site_name",
                value="Test Duplicate key",
            )

    def test_create_site_setting_with_no_value_raises_integrity_error(self):
        with self.assertRaises(IntegrityError):
            SiteSetting.objects.create(
                key="no_value",
                value=None,
            )

    def test_update_site_setting_with_no_value_raises_integrity_error(self):
        with self.assertRaises(IntegrityError):
            SiteSetting.objects.filter(pk=self.site_name_site_setting.pk).update(
                value=None,
            )

    def test_create_site_setting_with_no_key_raises_integrity_error(self):
        with self.assertRaises(IntegrityError):
            SiteSetting.objects.create(
                key=None,
                value="no key"
            )

    def test_update_site_setting_with_no_key_raises_integrity_error(self):
        with self.assertRaises(IntegrityError):
            SiteSetting.objects.filter(pk=self.site_name_site_setting.pk).update(
                key=None,
            )
