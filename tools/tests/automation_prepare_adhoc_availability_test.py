import tempfile
import os
import sys
import pytest
import pandas as pd
from ruamel.yaml import YAML
from automation_prepare_adhoc_availability import (
    get_available_mentor_sort,
    get_unavailable_mentor_sort,
    get_availability_update_dict,
    update_mentor_availability,
    MONTHS_MAP,
    TYPE_LONG_TERM,
    TYPE_AD_HOC,
    TYPE_BOTH
)

yaml = YAML()


class TestGetAvailableMentorSort:
    def test_new_mentor_with_full_availability_returns_500(self):
        mentor = {'name': 'Test Mentor', 'hours': 2}
        current_availability = [4, 5, 6]
        
        result = get_available_mentor_sort(mentor, current_availability)
        
        assert result == 500

    def test_mentor_with_more_than_3_hours_returns_500(self):
        mentor = {'name': 'Test Mentor', 'hours': 4}
        current_availability = [4]
        
        result = get_available_mentor_sort(mentor, current_availability)
        
        assert result == 500

    def test_mentor_with_3_or_less_hours_returns_200(self):
        mentor = {'name': 'Test Mentor', 'hours': 3}
        current_availability = [4]
        
        result = get_available_mentor_sort(mentor, current_availability)
        
        assert result == 200

    def test_mentor_with_1_hour_returns_200(self):
        mentor = {'name': 'Test Mentor', 'hours': 1}
        current_availability = [4]
        
        result = get_available_mentor_sort(mentor, current_availability)
        
        assert result == 200


class TestGetUnavailableMentorSort:
    def test_disabled_mentor_returns_1(self):
        mentor = {'name': 'Test Mentor', 'disabled': True, 'type': TYPE_BOTH}
        
        result = get_unavailable_mentor_sort(mentor)
        
        assert result == 1

    def test_long_term_mentor_returns_10(self):
        mentor = {'name': 'Test Mentor', 'disabled': False, 'type': TYPE_LONG_TERM}
        
        result = get_unavailable_mentor_sort(mentor)
        
        assert result == 10

    def test_ad_hoc_mentor_returns_100(self):
        mentor = {'name': 'Test Mentor', 'disabled': False, 'type': TYPE_AD_HOC}
        
        result = get_unavailable_mentor_sort(mentor)
        
        assert result == 100

    def test_both_type_mentor_returns_100(self):
        mentor = {'name': 'Test Mentor', 'disabled': False, 'type': TYPE_BOTH}
        
        result = get_unavailable_mentor_sort(mentor)
        
        assert result == 100


class TestGetAvailabilityUpdateDict:
    def test_returns_dict_with_mentor_hours(self):
        data = {
            'Mentor Name': ['Alice Smith', 'Bob Jones'],
            'Availability (Hours)': [5, 3]
        }
        df = pd.DataFrame(data)
        
        result = get_availability_update_dict(df)
        
        assert result['Alice Smith'] == 5
        assert result['Bob Jones'] == 3

    def test_empty_hours_returns_none(self):
        data = {
            'Mentor Name': ['Alice Smith'],
            'Availability (Hours)': ['']
        }
        df = pd.DataFrame(data)
        
        result = get_availability_update_dict(df)
        
        assert result['Alice Smith'] is None

    def test_nan_hours_returns_none(self):
        data = {
            'Mentor Name': ['Alice Smith'],
            'Availability (Hours)': [pd.NA]
        }
        df = pd.DataFrame(data)
        
        result = get_availability_update_dict(df)
        
        assert result['Alice Smith'] is None

    def test_strips_whitespace_from_names(self):
        data = {
            'Mentor Name': ['  Alice Smith  '],
            'Availability (Hours)': [4]
        }
        df = pd.DataFrame(data)
        
        result = get_availability_update_dict(df)
        
        assert 'Alice Smith' in result


class TestUpdateMentorAvailability:
    def test_updates_mentor_availability_from_xlsx(self, monkeypatch):

        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as xlsx_file:
            xlsx_path = xlsx_file.name
            
        with tempfile.NamedTemporaryFile(suffix='.yml', mode='w', delete=False) as yml_file:
            yml_path = yml_file.name
            
        try:
            df = pd.DataFrame({
                'Mentor Name': ['Alice Smith'],
                'Availability (Hours)': [5]
            })
            df.to_excel(xlsx_path, index=False)
            
            mentors = [
                {
                    'name': 'Alice Smith',
                    'hours': 2,
                    'availability': [4, 5],
                    'sort': 200,
                    'type': TYPE_AD_HOC,
                    'disabled': False
                },
                {
                    'name': 'Bob Jones',
                    'hours': 3,
                    'availability': [4],
                    'sort': 100,
                    'type': TYPE_LONG_TERM,
                    'disabled': False
                }
            ]
            
            with open(yml_path, 'w') as f:
                yaml.dump(mentors, f)
            
            update_mentor_availability(4, xlsx_path, yml_path)
            
            with open(yml_path, 'r') as f:
                result = yaml.load(f)
            
            alice = next(m for m in result if m['name'] == 'Alice Smith')
            assert alice['hours'] == 5
            assert alice['availability'] == [4]
            assert alice['sort'] == 500 
            
            bob = next(m for m in result if m['name'] == 'Bob Jones')
            assert bob['availability'] == []
            assert bob['sort'] == 10 
            
        finally:
            os.remove(xlsx_path)
            os.remove(yml_path)

    def test_mentor_not_in_xlsx_becomes_unavailable(self, monkeypatch):
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as xlsx_file:
            xlsx_path = xlsx_file.name
            
        with tempfile.NamedTemporaryFile(suffix='.yml', mode='w', delete=False) as yml_file:
            yml_path = yml_file.name
            
        try:
            df = pd.DataFrame({
                'Mentor Name': ['Alice Smith'],
                'Availability (Hours)': [5]
            })
            df.to_excel(xlsx_path, index=False)
            
            mentors = [
                {'name': 'Alice Smith', 'hours': 2, 'availability': [4], 'sort': 200, 'type': TYPE_AD_HOC, 'disabled': False},
                {'name': 'Bob Jones', 'hours': 3, 'availability': [4], 'sort': 200, 'type': TYPE_BOTH, 'disabled': False}
            ]
            
            with open(yml_path, 'w') as f:
                yaml.dump(mentors, f)
            
            update_mentor_availability(4, xlsx_path, yml_path)
            
            with open(yml_path, 'r') as f:
                result = yaml.load(f)
            
            bob = next(m for m in result if m['name'] == 'Bob Jones')
            assert bob['availability'] == []
            assert bob['sort'] == 100
            
        finally:
            os.remove(xlsx_path)
            os.remove(yml_path)

    def test_keeps_existing_hours_when_xlsx_hours_empty(self):
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as xlsx_file:
            xlsx_path = xlsx_file.name
            
        with tempfile.NamedTemporaryFile(suffix='.yml', mode='w', delete=False) as yml_file:
            yml_path = yml_file.name
            
        try:
            df = pd.DataFrame({
                'Mentor Name': ['Alice Smith'],
                'Availability (Hours)': ['']
            })
            df.to_excel(xlsx_path, index=False)
            
            mentors = [
                {'name': 'Alice Smith', 'hours': 3, 'availability': [4], 'sort': 200, 'type': TYPE_AD_HOC, 'disabled': False}
            ]
            
            with open(yml_path, 'w') as f:
                yaml.dump(mentors, f)
            
            update_mentor_availability(4, xlsx_path, yml_path)
            
            with open(yml_path, 'r') as f:
                result = yaml.load(f)
            
            alice = result[0]
            assert alice['hours'] == 3 
            
        finally:
            os.remove(xlsx_path)
            os.remove(yml_path)