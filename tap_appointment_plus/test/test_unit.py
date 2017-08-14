import unittest
import voluptuous

import tap_appointment_plus
import tap_appointment_plus.config


class TestUnit(unittest.TestCase):

    def generate_config(self):
        return {
            'site_id': 'abc',
            'api_key': 'def',
            'start_date': '2017-01-01T00:00:00Z',
            'user_agent': 'test <test@fishtownanalytics.com>'
        }

    def test__build_request(self):
        config = self.generate_config()

        self.assertEqual(
            tap_appointment_plus.build_request(config),
            {'data': 'response_type=json',
             'headers': {'Authorization': 'Basic abc:def',
                         'User-Agent': 'test <test@fishtownanalytics.com>'}})

    def test__validate_config(self):
        valid_config = {
            'site_id': 'abc',
            'api_key': 'def',
            'start_date': '2017-01-01T00:00:00Z',
            'user_agent': 'testing <test@fishtownanalytics.com>'
        }

        tap_appointment_plus.config.validate(valid_config)

        with self.assertRaises(voluptuous.error.Invalid):
            tap_appointment_plus.config.validate({})

        with self.assertRaises(voluptuous.error.Invalid):
            invalid = valid_config.copy()
            invalid['start_date'] = 100
            tap_appointment_plus.config.validate(invalid)
