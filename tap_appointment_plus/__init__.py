import argparse
import requests
import requests.auth
import singer

from base64 import b64encode
from datetime import datetime
from funcy import partial

import tap_appointment_plus.config
import tap_appointment_plus.schemas as schemas
from tap_appointment_plus.logger import LOGGER as logger


BASE_URL = 'https://ws.appointment-plus.com/'


def build_request(config):
    auth_header = 'Basic ' + b64encode(b':'.join([
        config['site_id'].encode('latin1'),
        config['api_key'].encode('latin1')])
    ).decode('ascii')

    return {
        'data': {'response_type': 'json'},
        'headers': {'Authorization': auth_header}
    }


def _make_request(url_path, request_dict):
    return requests.post(
        BASE_URL + url_path,
        **request_dict)


def _process_iso_date(d):
    return datetime.strptime(d, '%Y-%m-%dT%H:%M:%SZ')


def sync_appointments(endpoint, config):
    start_date = _process_iso_date(
        config['start_date']).strftime('%Y%m%d%H%M')

    return sync_endpoint(
        endpoint,
        config,
        {'updated': start_date})


def sync_events(endpoint, config):
    start_date = _process_iso_date(
        config['start_date']).strftime('%Y%m%d')

    return sync_endpoint(
        endpoint,
        config,
        {'start_date': start_date})


def sync_customers(endpoint, config):
    start_date = _process_iso_date(
        config['start_date']).strftime('%Y%m%d%H%M')

    return sync_endpoint(
        endpoint,
        config,
        {'updated': start_date})


def sync_customer_packages(endpoint, config):
    start_date = _process_iso_date(
        config['start_date']).strftime('%Y%m%d%H%M')

    return sync_endpoint(
        endpoint,
        config,
        {'updated': start_date})


def sync_staff(endpoint, config):
    return sync_endpoint(
        endpoint,
        config,
        {'show_deleted': 'yes'})


def sync_endpoint(endpoint, config, params={}):
    table_name = endpoint['name']

    logger.info("Syncing data from object '{}'.".format(endpoint['url']))

    singer.write_schema(
        table_name,
        endpoint['schema'],
        key_properties=endpoint['key_properties'])

    request = build_request(config)
    request['params'] = params
    result = _make_request(endpoint['url'], request)

    data = result.json()
    logger.info("Received {} records.".format(data.get('count', 0)))

    if data.get('data'):
        singer.write_records(table_name, data['data'])

    return result


endpoints = [
    {'name': 'appointments',
     'url': 'Appointments/GetAppointments',
     'schema': schemas.appointments,
     'key_properties': ['appt_id'],
     'sync_fn': sync_appointments},

    {'name': 'coupons',
     'url': 'POS/GetCoupons',
     'schema': schemas.coupons,
     'key_properties': ['coupon_id'],
     'sync_fn': sync_endpoint},

    {'name': 'custom_fields',
     'url': 'CustomFields/GetCustomFields',
     'schema': schemas.custom_fields,
     'key_properties': ['id', 'c_id', 'field_name'],
     'sync_fn': sync_endpoint},

    {'name': 'customers',
     'url': 'Customers/GetCustomers',
     'schema': schemas.customers,
     'key_properties': ['customer_id'],
     'sync_fn': sync_customers},

    {'name': 'customer_packages',
     'url': 'Customers/GetPackages',
     'schema': schemas.customer_packages,
     'key_properties': ['customer_package_id'],
     'sync_fn': sync_endpoint},

    {'name': 'events',
     'url': 'Events/GetEvents',
     'schema': schemas.events,
     'key_properties': ['c_id', 'service_id', 'event_template_id'],
     'sync_fn': sync_events},

    {'name': 'locations',
     'url': 'Locations/GetLocations',
     'schema': schemas.locations,
     'key_properties': ['location_id'],
     'sync_fn': sync_endpoint},

    {'name': 'packages',
     'url': 'Packages/GetPackages',
     'schema': schemas.packages,
     'key_properties': ['c_id', 'item_id', 'package_type_id'],
     'sync_fn': sync_endpoint},

    {'name': 'payment_types',
     'url': 'Payments/GetPaymentTypes',
     'schema': schemas.payment_types,
     'key_properties': ['payment_type_id'],
     'sync_fn': sync_endpoint},

    {'name': 'rooms',
     'url': 'Rooms/GetRooms',
     'schema': schemas.rooms,
     'key_properties': ['c_id', 'room_id'],
     'sync_fn': sync_endpoint},

    {'name': 'services',
     'url': 'Services/GetServices',
     'schema': schemas.services,
     'key_properties': ['c_id', 'service_id'],
     'sync_fn': sync_endpoint},

    {'name': 'staff',
     'url': 'Staff/GetStaff',
     'schema': schemas.staff,
     'key_properties': ['c_id', 'employee_id'],
     'sync_fn': sync_staff},
]


def do_sync(args):
    logger.info('Starting sync.')

    config = tap_appointment_plus.config.load(args.config)

    for endpoint in endpoints:
        endpoint['sync_fn'](endpoint, config)

    logger.info('Done.')


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-c', '--config', help='Config file', required=True)
    parser.add_argument(
        '-s', '--state', help='State file')

    args = parser.parse_args()

    try:

        do_sync(args)
    except RuntimeError:
        logger.fatal("Run failed.")
        exit(1)


if __name__ == '__main__':
    main()
