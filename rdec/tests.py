from django.test import TestCase
from django.utils import timezone

from rdec.views import format_ical_date_string


class UtilTests(TestCase):
    def test_datetime_formatter1(self):
        # January 18, 1998, at 11 PM
        dt = timezone.datetime(1998, 1, 18, 23, 0, 0)
        s = format_ical_date_string(dt)
        self.assertEqual(s, '19980118T230000')

    def test_datetime_formatter2(self):
        # January 19, 1998, at 0735
        dt = timezone.datetime(1998, 1, 19, 7, 35, 0)
        s = format_ical_date_string(dt)
        self.assertEqual(s, '19980119T073500')

