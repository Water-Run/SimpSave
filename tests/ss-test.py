"""
@file ss-test.py
@author WaterRun
@version 10.0
@date 2025-11-07
@description Comprehensive test suite for all SimpSave engines
             - Basic functionality tests (~70 tests)
             - Edge case tests (~30 tests)
             - Performance tests (all engines)
"""

import simpsave
import pytest
import time
import random
import string
import math
import json
import tempfile
import os
import shutil
from typing import Dict, List, Any
from datetime import datetime


# ============================================================================
# Test Configuration
# ============================================================================

TEST_DIR = tempfile.mkdtemp()
SIMP_FILE = os.path.join(TEST_DIR, 'test.simpsave')
INI_FILE = os.path.join(TEST_DIR, 'test.ini')
XML_FILE = os.path.join(TEST_DIR, 'test.xml')
YML_FILE = os.path.join(TEST_DIR, 'test.yml')
JSON_FILE = os.path.join(TEST_DIR, 'test.json')
TOML_FILE = os.path.join(TEST_DIR, 'test.toml')
SQLITE_FILE = os.path.join(TEST_DIR, 'test.db')
REDIS_URL = 'redis://localhost:6379/0'

# All available engines with their test files
ALL_ENGINES = [
    ('SimpEngine', simpsave.SimpEngine, SIMP_FILE),
    ('IniEngine', simpsave.IniEngine, INI_FILE),
    ('XmlEngine', simpsave.XmlEngine, XML_FILE),
    ('YmlEngine', simpsave.YmlEngine, YML_FILE),
    ('JsonEngine', simpsave.JsonEngine, JSON_FILE),
    ('TomlEngine', simpsave.TomlEngine, TOML_FILE),
    ('SqliteEngine', simpsave.SqliteEngine, SQLITE_FILE),
    ('RedisEngine', simpsave.RedisEngine, REDIS_URL),
]


def setup_module():
    """Setup test environment"""
    os.makedirs(TEST_DIR, exist_ok=True)


def teardown_module():
    """Cleanup test environment"""
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)
    
    # Clean Redis
    try:
        engine = simpsave.RedisEngine()
        if engine.check_available():
            engine.delete(REDIS_URL)
    except:
        pass


def get_available_engines():
    """Get list of available engines for testing"""
    available = []
    for name, engine_class, test_file in ALL_ENGINES:
        try:
            engine = engine_class()
            if engine.check_available():
                available.append((name, engine_class, test_file))
        except:
            pass
    return available


# ============================================================================
# Basic Type Tests (10 tests per engine)
# ============================================================================

@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_write_read_integer(engine_name, engine_class, test_file):
    """Test write and read integer values"""
    engine = engine_class()
    engine.delete(test_file)
    
    # Positive integer
    assert engine.write('int_positive', 42, test_file)
    assert engine.read('int_positive', test_file) == 42
    
    # Negative integer
    assert engine.write('int_negative', -100, test_file)
    assert engine.read('int_negative', test_file) == -100
    
    # Zero
    assert engine.write('int_zero', 0, test_file)
    assert engine.read('int_zero', test_file) == 0
    
    engine.delete(test_file)


@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_write_read_float(engine_name, engine_class, test_file):
    """Test write and read float values"""
    engine = engine_class()
    engine.delete(test_file)
    
    # Positive float
    assert engine.write('float_positive', 3.14159, test_file)
    assert abs(engine.read('float_positive', test_file) - 3.14159) < 1e-10
    
    # Negative float
    assert engine.write('float_negative', -2.71828, test_file)
    assert abs(engine.read('float_negative', test_file) - (-2.71828)) < 1e-10
    
    # Very small float
    assert engine.write('float_small', 0.000001, test_file)
    assert abs(engine.read('float_small', test_file) - 0.000001) < 1e-15
    
    engine.delete(test_file)


@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_write_read_string(engine_name, engine_class, test_file):
    """Test write and read string values"""
    engine = engine_class()
    engine.delete(test_file)
    
    # Simple string
    assert engine.write('str_simple', 'hello', test_file)
    assert engine.read('str_simple', test_file) == 'hello'
    
    # String with spaces
    assert engine.write('str_spaces', 'hello world', test_file)
    assert engine.read('str_spaces', test_file) == 'hello world'
    
    # Empty string
    assert engine.write('str_empty', '', test_file)
    assert engine.read('str_empty', test_file) == ''
    
    engine.delete(test_file)


@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_write_read_boolean(engine_name, engine_class, test_file):
    """Test write and read boolean values"""
    engine = engine_class()
    engine.delete(test_file)
    
    assert engine.write('bool_true', True, test_file)
    assert engine.read('bool_true', test_file) == True
    
    assert engine.write('bool_false', False, test_file)
    assert engine.read('bool_false', test_file) == False
    
    engine.delete(test_file)


@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_write_read_none(engine_name, engine_class, test_file):
    """Test write and read None value"""
    engine = engine_class()
    engine.delete(test_file)
    
    assert engine.write('none_value', None, test_file)
    assert engine.read('none_value', test_file) is None
    
    engine.delete(test_file)


@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_write_read_list(engine_name, engine_class, test_file):
    """Test write and read list values"""
    engine = engine_class()
    engine.delete(test_file)
    
    # Simple list
    simple_list = [1, 2, 3, 4, 5]
    assert engine.write('list_simple', simple_list, test_file)
    assert engine.read('list_simple', test_file) == simple_list
    
    # Mixed type list
    mixed_list = [1, 'a', True, None, 3.14]
    assert engine.write('list_mixed', mixed_list, test_file)
    assert engine.read('list_mixed', test_file) == mixed_list
    
    # Empty list
    assert engine.write('list_empty', [], test_file)
    assert engine.read('list_empty', test_file) == []
    
    engine.delete(test_file)


@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_write_read_dict(engine_name, engine_class, test_file):
    """Test write and read dictionary values"""
    engine = engine_class()
    engine.delete(test_file)
    
    # Simple dict
    simple_dict = {'a': 1, 'b': 2, 'c': 3}
    assert engine.write('dict_simple', simple_dict, test_file)
    assert engine.read('dict_simple', test_file) == simple_dict
    
    # Mixed value dict
    mixed_dict = {'int': 42, 'str': 'hello', 'bool': True, 'none': None}
    assert engine.write('dict_mixed', mixed_dict, test_file)
    assert engine.read('dict_mixed', test_file) == mixed_dict
    
    # Empty dict
    assert engine.write('dict_empty', {}, test_file)
    assert engine.read('dict_empty', test_file) == {}
    
    engine.delete(test_file)


@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_write_read_tuple(engine_name, engine_class, test_file):
    """Test write and read tuple values"""
    engine = engine_class()
    engine.delete(test_file)
    
    # Simple tuple
    simple_tuple = (1, 2, 3)
    assert engine.write('tuple_simple', simple_tuple, test_file)
    assert engine.read('tuple_simple', test_file) == simple_tuple
    
    # Mixed tuple
    mixed_tuple = (1, 'a', True, None)
    assert engine.write('tuple_mixed', mixed_tuple, test_file)
    assert engine.read('tuple_mixed', test_file) == mixed_tuple
    
    # Empty tuple
    assert engine.write('tuple_empty', (), test_file)
    assert engine.read('tuple_empty', test_file) == ()
    
    engine.delete(test_file)


@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_write_read_set(engine_name, engine_class, test_file):
    """Test write and read set values"""
    engine = engine_class()
    engine.delete(test_file)
    
    # Simple set
    simple_set = {1, 2, 3, 4, 5}
    assert engine.write('set_simple', simple_set, test_file)
    assert engine.read('set_simple', test_file) == simple_set
    
    # Mixed set
    mixed_set = {1, 'a', 'b', 'c'}
    assert engine.write('set_mixed', mixed_set, test_file)
    assert engine.read('set_mixed', test_file) == mixed_set
    
    # Empty set
    assert engine.write('set_empty', set(), test_file)
    assert engine.read('set_empty', test_file) == set()
    
    engine.delete(test_file)


@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_has_operation(engine_name, engine_class, test_file):
    """Test has() operation"""
    engine = engine_class()
    engine.delete(test_file)
    
    # Non-existent key
    assert engine.has('nonexistent', test_file) == False
    
    # Existing key
    engine.write('exists', 'value', test_file)
    assert engine.has('exists', test_file) == True
    
    engine.delete(test_file)


# ============================================================================
# Edge Case Tests - Numbers (5 tests per engine)
# ============================================================================

@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_large_integer(engine_name, engine_class, test_file):
    """Test very large integer values"""
    engine = engine_class()
    engine.delete(test_file)
    
    # Python supports arbitrary precision integers
    large_int = 10**100
    assert engine.write('large_int', large_int, test_file)
    assert engine.read('large_int', test_file) == large_int
    
    # Negative large integer
    neg_large = -(10**100)
    assert engine.write('neg_large', neg_large, test_file)
    assert engine.read('neg_large', test_file) == neg_large
    
    engine.delete(test_file)


@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_extreme_float(engine_name, engine_class, test_file):
    """Test extreme float values"""
    engine = engine_class()
    engine.delete(test_file)
    
    # Very small float
    small_float = 1e-300
    assert engine.write('small_float', small_float, test_file)
    assert abs(engine.read('small_float', test_file) - small_float) < 1e-310
    
    # Very large float
    large_float = 1e300
    assert engine.write('large_float', large_float, test_file)
    assert abs(engine.read('large_float', test_file) - large_float) < 1e290
    
    engine.delete(test_file)


@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_special_float_infinity(engine_name, engine_class, test_file):
    """Test infinity float values"""
    engine = engine_class()
    engine.delete(test_file)
    
    # Positive infinity
    assert engine.write('pos_inf', float('inf'), test_file)
    result = engine.read('pos_inf', test_file)
    assert math.isinf(result) and result > 0
    
    # Negative infinity
    assert engine.write('neg_inf', float('-inf'), test_file)
    result = engine.read('neg_inf', test_file)
    assert math.isinf(result) and result < 0
    
    engine.delete(test_file)


@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_special_float_nan(engine_name, engine_class, test_file):
    """Test NaN (Not a Number) float value"""
    engine = engine_class()
    engine.delete(test_file)
    
    assert engine.write('nan_value', float('nan'), test_file)
    result = engine.read('nan_value', test_file)
    assert math.isnan(result)
    
    engine.delete(test_file)


@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_float_precision(engine_name, engine_class, test_file):
    """Test float precision preservation"""
    engine = engine_class()
    engine.delete(test_file)
    
    # Test various precision levels
    test_values = [
        0.1 + 0.2,  # Famous floating point issue
        1/3,
        math.pi,
        math.e,
        1.23456789012345
    ]
    
    for i, value in enumerate(test_values):
        key = f'precision_{i}'
        assert engine.write(key, value, test_file)
        # Allow small floating point error
        assert abs(engine.read(key, test_file) - value) < 1e-10
    
    engine.delete(test_file)


# ============================================================================
# Edge Case Tests - Strings (5 tests per engine)
# ============================================================================

@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_unicode_strings(engine_name, engine_class, test_file):
    """Test various Unicode strings"""
    engine = engine_class()
    engine.delete(test_file)
    
    # Chinese
    assert engine.write('unicode_cn', '你好世界', test_file)
    assert engine.read('unicode_cn', test_file) == '你好世界'
    
    # Japanese
    assert engine.write('unicode_jp', 'こんにちは世界', test_file)
    assert engine.read('unicode_jp', test_file) == 'こんにちは世界'
    
    # Emoji
    assert engine.write('unicode_emoji', '😀😃😄😁🎉', test_file)
    assert engine.read('unicode_emoji', test_file) == '😀😃😄😁🎉'
    
    # Mixed
    assert engine.write('unicode_mixed', 'Hello 世界 🌍', test_file)
    assert engine.read('unicode_mixed', test_file) == 'Hello 世界 🌍'
    
    engine.delete(test_file)


@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_special_characters(engine_name, engine_class, test_file):
    """Test strings with special characters"""
    engine = engine_class()
    engine.delete(test_file)
    
    # Escape sequences
    escape_str = 'Line1\nLine2\tTab\rCarriage"Quote\'Single\\Backslash'
    assert engine.write('escape_chars', escape_str, test_file)
    assert engine.read('escape_chars', test_file) == escape_str
    
    engine.delete(test_file)


@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_very_long_string(engine_name, engine_class, test_file):
    """Test very long string (100KB)"""
    engine = engine_class()
    engine.delete(test_file)
    
    # 100 KB string
    long_string = 'A' * (1024 * 100)
    assert engine.write('long_string', long_string, test_file)
    assert engine.read('long_string', test_file) == long_string
    assert len(engine.read('long_string', test_file)) == 1024 * 100
    
    engine.delete(test_file)


@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_string_with_nulls(engine_name, engine_class, test_file):
    """Test string containing null bytes"""
    engine = engine_class()
    engine.delete(test_file)
    
    # String with null bytes
    null_string = 'Hello\x00World'
    assert engine.write('null_string', null_string, test_file)
    assert engine.read('null_string', test_file) == null_string
    
    engine.delete(test_file)


@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_multiline_string(engine_name, engine_class, test_file):
    """Test multiline strings"""
    engine = engine_class()
    engine.delete(test_file)
    
    multiline = """This is line 1
This is line 2
This is line 3
    Indented line
"""
    assert engine.write('multiline', multiline, test_file)
    assert engine.read('multiline', test_file) == multiline
    
    engine.delete(test_file)


# ============================================================================
# Edge Case Tests - Collections (5 tests per engine)
# ============================================================================

@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_nested_list(engine_name, engine_class, test_file):
    """Test deeply nested list structures"""
    engine = engine_class()
    engine.delete(test_file)
    
    # 10 levels of nesting
    nested = [1, [2, [3, [4, [5, [6, [7, [8, [9, [10]]]]]]]]]]
    assert engine.write('nested_list', nested, test_file)
    assert engine.read('nested_list', test_file) == nested
    
    engine.delete(test_file)


@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_nested_dict(engine_name, engine_class, test_file):
    """Test deeply nested dictionary structures"""
    engine = engine_class()
    engine.delete(test_file)
    
    nested = {
        'l1': {
            'l2': {
                'l3': {
                    'l4': {
                        'l5': {
                            'value': 'deep'
                        }
                    }
                }
            }
        }
    }
    assert engine.write('nested_dict', nested, test_file)
    assert engine.read('nested_dict', test_file) == nested
    
    engine.delete(test_file)


@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_mixed_nested_structure(engine_name, engine_class, test_file):
    """Test complex mixed nested structures"""
    engine = engine_class()
    engine.delete(test_file)
    
    complex_structure = {
        'list': [1, 2, {'nested_dict': ['a', 'b', (1, 2, 3)]}],
        'dict': {'key': [1, 2, {'deep': (1, 2)}]},
        'tuple': (1, [2, 3], {'a': 1}),
        'set': {1, 2, 3}
    }
    assert engine.write('complex_mixed', complex_structure, test_file)
    assert engine.read('complex_mixed', test_file) == complex_structure
    
    engine.delete(test_file)


@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_large_list(engine_name, engine_class, test_file):
    """Test list with many elements"""
    engine = engine_class()
    engine.delete(test_file)
    
    large_list = list(range(1000))
    assert engine.write('large_list', large_list, test_file)
    assert engine.read('large_list', test_file) == large_list
    
    engine.delete(test_file)


@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_large_dict(engine_name, engine_class, test_file):
    """Test dictionary with many keys"""
    engine = engine_class()
    engine.delete(test_file)
    
    large_dict = {f'key_{i}': i for i in range(1000)}
    assert engine.write('large_dict', large_dict, test_file)
    assert engine.read('large_dict', test_file) == large_dict
    
    engine.delete(test_file)


# ============================================================================
# Operation Tests (10 tests per engine)
# ============================================================================

@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_has_existing_key(engine_name, engine_class, test_file):
    """Test has() with existing key"""
    engine = engine_class()
    engine.delete(test_file)
    
    engine.write('exists', 'value', test_file)
    assert engine.has('exists', test_file) == True
    
    engine.delete(test_file)


@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_has_nonexistent_key(engine_name, engine_class, test_file):
    """Test has() with non-existent key"""
    engine = engine_class()
    engine.delete(test_file)
    
    assert engine.has('nonexistent_key_12345', test_file) == False
    
    engine.delete(test_file)


@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_remove_existing_key(engine_name, engine_class, test_file):
    """Test remove() with existing key"""
    engine = engine_class()
    engine.delete(test_file)
    
    engine.write('to_remove', 'value', test_file)
    assert engine.has('to_remove', test_file) == True
    assert engine.remove('to_remove', test_file) == True
    assert engine.has('to_remove', test_file) == False
    
    engine.delete(test_file)


@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_remove_nonexistent_key(engine_name, engine_class, test_file):
    """Test remove() with non-existent key"""
    engine = engine_class()
    engine.delete(test_file)
    
    assert engine.remove('never_existed', test_file) == False
    
    engine.delete(test_file)


@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_overwrite_existing_key(engine_name, engine_class, test_file):
    """Test overwriting existing key"""
    engine = engine_class()
    engine.delete(test_file)
    
    engine.write('overwrite', 'original', test_file)
    assert engine.read('overwrite', test_file) == 'original'
    
    engine.write('overwrite', 'updated', test_file)
    assert engine.read('overwrite', test_file) == 'updated'
    
    engine.write('overwrite', 12345, test_file)
    assert engine.read('overwrite', test_file) == 12345
    
    engine.delete(test_file)


@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_read_nonexistent_key(engine_name, engine_class, test_file):
    """Test read() with non-existent key raises KeyError"""
    engine = engine_class()
    engine.delete(test_file)
    
    with pytest.raises(KeyError):
        engine.read('this_key_does_not_exist', test_file)
    
    engine.delete(test_file)


@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_match_simple_pattern(engine_name, engine_class, test_file):
    """Test match() with simple pattern"""
    engine = engine_class()
    engine.delete(test_file)
    
    engine.write('test_001', 'a', test_file)
    engine.write('test_002', 'b', test_file)
    engine.write('prod_001', 'c', test_file)
    
    result = engine.match(r'^test_', test_file)
    assert len(result) == 2
    assert 'test_001' in result
    assert 'test_002' in result
    
    engine.delete(test_file)


@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_match_complex_pattern(engine_name, engine_class, test_file):
    """Test match() with complex regex pattern"""
    engine = engine_class()
    engine.delete(test_file)
    
    engine.write('user_001_active', 'Alice', test_file)
    engine.write('user_002_inactive', 'Bob', test_file)
    engine.write('user_003_active', 'Charlie', test_file)
    engine.write('admin_001', 'Admin', test_file)
    
    # Match active users
    active = engine.match(r'user_\d+_active', test_file)
    assert len(active) == 2
    
    # Match all with numbers
    numbered = engine.match(r'_\d{3}', test_file)
    assert len(numbered) == 4
    
    engine.delete(test_file)


@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_match_no_results(engine_name, engine_class, test_file):
    """Test match() returns empty dict when no matches"""
    engine = engine_class()
    engine.delete(test_file)
    
    engine.write('test', 'value', test_file)
    
    result = engine.match(r'^nonexistent_pattern', test_file)
    assert result == {}
    assert len(result) == 0
    
    engine.delete(test_file)


@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_delete_all_keys(engine_name, engine_class, test_file):
    """Test delete() removes all keys"""
    engine = engine_class()
    engine.delete(test_file)
    
    # Write multiple keys
    for i in range(10):
        engine.write(f'delete_test_{i}', i, test_file)
    
    # Verify they exist
    assert engine.has('delete_test_0', test_file)
    assert engine.has('delete_test_5', test_file)
    
    # Delete all
    assert engine.delete(test_file) == True
    
    # Verify they're gone
    for i in range(10):
        assert engine.has(f'delete_test_{i}', test_file) == False
    
    engine.delete(test_file)


# ============================================================================
# Key Name Tests (5 tests per engine)
# ============================================================================

@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_key_with_spaces(engine_name, engine_class, test_file):
    """Test key containing spaces"""
    engine = engine_class()
    engine.delete(test_file)
    
    key = 'key with spaces'
    assert engine.write(key, 'value', test_file)
    assert engine.read(key, test_file) == 'value'
    
    engine.delete(test_file)


@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_key_with_special_chars(engine_name, engine_class, test_file):
    """Test key with special characters"""
    engine = engine_class()
    engine.delete(test_file)
    
    key = 'key_with_special@chars#123'
    assert engine.write(key, 'value', test_file)
    assert engine.read(key, test_file) == 'value'
    
    engine.delete(test_file)


@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_key_unicode(engine_name, engine_class, test_file):
    """Test key with Unicode characters"""
    engine = engine_class()
    engine.delete(test_file)
    
    key = '用户_001_测试'
    assert engine.write(key, 'value', test_file)
    assert engine.read(key, test_file) == 'value'
    
    engine.delete(test_file)


@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_key_very_long(engine_name, engine_class, test_file):
    """Test very long key name"""
    engine = engine_class()
    engine.delete(test_file)
    
    # 500 character key
    key = 'k' * 500
    assert engine.write(key, 'value', test_file)
    assert engine.read(key, test_file) == 'value'
    
    engine.delete(test_file)


@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_key_numeric_string(engine_name, engine_class, test_file):
    """Test key that looks like a number"""
    engine = engine_class()
    engine.delete(test_file)
    
    key = '12345'
    assert engine.write(key, 'value', test_file)
    assert engine.read(key, test_file) == 'value'
    
    engine.delete(test_file)


# ============================================================================
# Batch Operation Tests (5 tests per engine)
# ============================================================================

@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_batch_write_read(engine_name, engine_class, test_file):
    """Test batch writing and reading"""
    engine = engine_class()
    engine.delete(test_file)
    
    # Write 100 keys
    for i in range(100):
        assert engine.write(f'batch_{i}', f'value_{i}', test_file)
    
    # Read all
    for i in range(100):
        assert engine.read(f'batch_{i}', test_file) == f'value_{i}'
    
    engine.delete(test_file)


@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_sequential_overwrites(engine_name, engine_class, test_file):
    """Test multiple overwrites of same key"""
    engine = engine_class()
    engine.delete(test_file)
    
    key = 'sequential'
    
    for i in range(10):
        engine.write(key, i, test_file)
        assert engine.read(key, test_file) == i
    
    engine.delete(test_file)


@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_interleaved_operations(engine_name, engine_class, test_file):
    """Test interleaved write/read/remove operations"""
    engine = engine_class()
    engine.delete(test_file)
    
    engine.write('int1', 1, test_file)
    assert engine.read('int1', test_file) == 1
    
    engine.write('int2', 2, test_file)
    assert engine.has('int1', test_file)
    
    engine.remove('int1', test_file)
    assert not engine.has('int1', test_file)
    assert engine.has('int2', test_file)
    
    engine.delete(test_file)


@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_mixed_type_batch(engine_name, engine_class, test_file):
    """Test batch operations with mixed types"""
    engine = engine_class()
    engine.delete(test_file)
    
    test_data = {
        'int': 42,
        'float': 3.14,
        'str': 'hello',
        'bool': True,
        'none': None,
        'list': [1, 2, 3],
        'dict': {'a': 1},
        'tuple': (1, 2),
        'set': {1, 2, 3}
    }
    
    # Write all
    for key, value in test_data.items():
        assert engine.write(f'mixed_{key}', value, test_file)
    
    # Read and verify all
    for key, value in test_data.items():
        assert engine.read(f'mixed_{key}', test_file) == value
    
    engine.delete(test_file)


@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_remove_multiple_keys(engine_name, engine_class, test_file):
    """Test removing multiple keys"""
    engine = engine_class()
    engine.delete(test_file)
    
    # Write keys
    keys = [f'remove_multi_{i}' for i in range(20)]
    for key in keys:
        engine.write(key, 'value', test_file)
    
    # Remove all
    for key in keys:
        assert engine.remove(key, test_file) == True
    
    # Verify all removed
    for key in keys:
        assert engine.has(key, test_file) == False
    
    engine.delete(test_file)


# ============================================================================
# Error Handling Tests (3 tests per engine)
# ============================================================================

@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_read_after_delete(engine_name, engine_class, test_file):
    """Test reading after delete raises KeyError"""
    engine = engine_class()
    engine.delete(test_file)
    
    engine.write('temp', 'value', test_file)
    engine.remove('temp', test_file)
    
    with pytest.raises(KeyError):
        engine.read('temp', test_file)
    
    engine.delete(test_file)


@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_empty_key_name(engine_name, engine_class, test_file):
    """Test empty string as key name"""
    engine = engine_class()
    engine.delete(test_file)
    
    # Empty key should work
    assert engine.write('', 'value', test_file)
    assert engine.read('', test_file) == 'value'
    
    engine.delete(test_file)


@pytest.mark.parametrize("engine_name,engine_class,test_file", get_available_engines())
def test_duplicate_removes(engine_name, engine_class, test_file):
    """Test removing same key multiple times"""
    engine = engine_class()
    engine.delete(test_file)
    
    engine.write('dup_remove', 'value', test_file)
    
    assert engine.remove('dup_remove', test_file) == True
    assert engine.remove('dup_remove', test_file) == False
    assert engine.remove('dup_remove', test_file) == False
    
    engine.delete(test_file)


# ============================================================================
# Performance Test Framework
# ============================================================================

class PerformanceTest:
    """Performance testing framework for storage engines"""
    
    def __init__(self):
        self.results = {}
        
    def generate_random_string(self, length: int = 10) -> str:
        """Generate random alphanumeric string"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    def generate_simple_data(self, count: int) -> Dict[str, Any]:
        """Generate simple data (strings, numbers, booleans)"""
        data = {}
        for i in range(count):
            key = f'simple_{i:06d}'
            # Mix of different simple types
            value_type = i % 4
            if value_type == 0:
                value = self.generate_random_string(20)
            elif value_type == 1:
                value = random.randint(-1000000, 1000000)
            elif value_type == 2:
                value = random.uniform(-1000.0, 1000.0)
            else:
                value = random.choice([True, False, None])
            data[key] = value
        return data
    
    def generate_medium_data(self, count: int) -> Dict[str, Any]:
        """Generate medium complexity data (lists, dicts with 2-3 levels)"""
        data = {}
        for i in range(count):
            key = f'medium_{i:06d}'
            value = {
                'id': i,
                'name': self.generate_random_string(15),
                'email': f'{self.generate_random_string(8)}@example.com',
                'age': random.randint(18, 80),
                'active': random.choice([True, False]),
                'tags': [self.generate_random_string(6) for _ in range(5)],
                'metadata': {
                    'created': datetime.now().isoformat(),
                    'score': random.uniform(0, 100),
                    'settings': {
                        'theme': random.choice(['light', 'dark']),
                        'lang': random.choice(['en', 'zh', 'ja'])
                    }
                }
            }
            data[key] = value
        return data
    
    def generate_complex_data(self, count: int) -> Dict[str, Any]:
        """Generate highly nested complex data (5-7 levels deep)"""
        data = {}
        for i in range(count):
            key = f'complex_{i:06d}'
            value = {
                'id': i,
                'user': {
                    'profile': {
                        'basic': {
                            'name': self.generate_random_string(20),
                            'email': f'{self.generate_random_string(10)}@example.com',
                        },
                        'address': {
                            'street': self.generate_random_string(30),
                            'city': self.generate_random_string(15),
                            'coordinates': {
                                'lat': random.uniform(-90, 90),
                                'lon': random.uniform(-180, 180),
                                'metadata': {
                                    'accuracy': random.uniform(0, 100),
                                    'source': self.generate_random_string(10)
                                }
                            }
                        }
                    },
                    'preferences': {
                        'notifications': {
                            'email': {
                                'enabled': random.choice([True, False]),
                                'frequency': random.choice(['daily', 'weekly', 'monthly']),
                            }
                        }
                    }
                },
                'history': [
                    {
                        'timestamp': datetime.now().isoformat(),
                        'action': random.choice(['login', 'logout', 'update']),
                        'details': {
                            'ip': f'{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}',
                        }
                    }
                    for _ in range(3)
                ]
            }
            data[key] = value
        return data
    
    def test_write_performance(self, engine, file: str, data: Dict) -> float:
        """Test write performance"""
        start_time = time.time()
        for key, value in data.items():
            engine.write(key, value, file)
        end_time = time.time()
        return end_time - start_time
    
    def test_read_performance(self, engine, file: str, keys: List[str]) -> float:
        """Test read performance"""
        start_time = time.time()
        for key in keys:
            engine.read(key, file)
        end_time = time.time()
        return end_time - start_time
    
    def run_engine_test(self, engine_name: str, engine, file: str):
        """Run complete test suite for an engine"""
        print(f"\n{'='*80}")
        print(f"Testing Engine: {engine_name}")
        print(f"{'='*80}")
        
        # Generate test data
        print(f"\nGenerating test data...")
        simple_data = self.generate_simple_data(4000)
        medium_data = self.generate_medium_data(900)
        complex_data = self.generate_complex_data(100)
        
        total_count = len(simple_data) + len(medium_data) + len(complex_data)
        print(f"  Simple data: {len(simple_data)} records")
        print(f"  Medium data: {len(medium_data)} records")
        print(f"  Complex data: {len(complex_data)} records")
        print(f"  Total: {total_count} records")
        
        # Clean up
        print(f"\nCleaning existing data...")
        engine.delete(file)
        
        # Test writes
        print(f"\nTesting write performance...")
        
        print(f"  Writing simple data...")
        simple_write_time = self.test_write_performance(engine, file, simple_data)
        
        print(f"  Writing medium data...")
        medium_write_time = self.test_write_performance(engine, file, medium_data)
        
        print(f"  Writing complex data...")
        complex_write_time = self.test_write_performance(engine, file, complex_data)
        
        total_write_time = simple_write_time + medium_write_time + complex_write_time
        write_ops = total_count / total_write_time if total_write_time > 0 else 0
        
        print(f"\n  Write Results:")
        print(f"    Simple:  {len(simple_data)/simple_write_time:.0f} ops/s ({simple_write_time:.3f}s)")
        print(f"    Medium:  {len(medium_data)/medium_write_time:.0f} ops/s ({medium_write_time:.3f}s)")
        print(f"    Complex: {len(complex_data)/complex_write_time:.0f} ops/s ({complex_write_time:.3f}s)")
        print(f"    Total:   {write_ops:.0f} ops/s ({total_write_time:.3f}s)")
        
        # Test reads
        print(f"\nTesting read performance...")
        
        simple_keys = list(simple_data.keys())
        medium_keys = list(medium_data.keys())
        complex_keys = list(complex_data.keys())
        
        print(f"  Reading simple data...")
        simple_read_time = self.test_read_performance(engine, file, simple_keys)
        
        print(f"  Reading medium data...")
        medium_read_time = self.test_read_performance(engine, file, medium_keys)
        
        print(f"  Reading complex data...")
        complex_read_time = self.test_read_performance(engine, file, complex_keys)
        
        total_read_time = simple_read_time + medium_read_time + complex_read_time
        read_ops = total_count / total_read_time if total_read_time > 0 else 0
        
        print(f"\n  Read Results:")
        print(f"    Simple:  {len(simple_data)/simple_read_time:.0f} ops/s ({simple_read_time:.3f}s)")
        print(f"    Medium:  {len(medium_data)/medium_read_time:.0f} ops/s ({medium_read_time:.3f}s)")
        print(f"    Complex: {len(complex_data)/complex_read_time:.0f} ops/s ({complex_read_time:.3f}s)")
        print(f"    Total:   {read_ops:.0f} ops/s ({total_read_time:.3f}s)")
        
        # Clean up
        print(f"\nCleaning up...")
        engine.delete(file)
        
        # Store results
        self.results[engine_name] = {
            'write_ops': write_ops,
            'read_ops': read_ops,
            'write_time': total_write_time,
            'read_time': total_read_time,
            'simple_write': len(simple_data)/simple_write_time if simple_write_time > 0 else 0,
            'simple_read': len(simple_data)/simple_read_time if simple_read_time > 0 else 0,
            'medium_write': len(medium_data)/medium_write_time if medium_write_time > 0 else 0,
            'medium_read': len(medium_data)/medium_read_time if medium_read_time > 0 else 0,
            'complex_write': len(complex_data)/complex_write_time if complex_write_time > 0 else 0,
            'complex_read': len(complex_data)/complex_read_time if complex_read_time > 0 else 0,
            'total_count': total_count
        }
    
    def print_comparison_report(self):
        """Print performance comparison report with JsonEngine as baseline (1.0)"""
        print(f"\n{'='*80}")
        print(f"PERFORMANCE COMPARISON REPORT")
        print(f"{'='*80}")
        
        if not self.results:
            print("No results available")
            return
        
        # Find baseline (JsonEngine)
        baseline_name = None
        for name in self.results.keys():
            if 'JsonEngine' in name:
                baseline_name = name
                break
        
        if baseline_name is None:
            baseline_name = list(self.results.keys())[0]
        
        baseline = self.results[baseline_name]
        
        print(f"\nBaseline Engine: {baseline_name} = 1.0x")
        print(f"Total Records: {baseline['total_count']}")
        print(f"\n{'-'*80}")
        
        # Print header
        print(f"\n{'Engine':<20} {'Write (ops/s)':<15} {'Ratio':<10} {'Read (ops/s)':<15} {'Ratio':<10}")
        print(f"{'-'*80}")
        
        # Sort by write performance
        sorted_results = sorted(
            self.results.items(),
            key=lambda x: x[1]['write_ops'],
            reverse=True
        )
        
        for engine_name, results in sorted_results:
            write_ratio = results['write_ops'] / baseline['write_ops'] if baseline['write_ops'] > 0 else 0
            read_ratio = results['read_ops'] / baseline['read_ops'] if baseline['read_ops'] > 0 else 0
            
            write_symbol = '✓' if write_ratio >= 1.0 else '✗'
            read_symbol = '✓' if read_ratio >= 1.0 else '✗'
            
            print(f"{engine_name:<20} "
                  f"{results['write_ops']:>13.0f} "
                  f"{write_symbol} {write_ratio:>6.2f}x "
                  f"{results['read_ops']:>13.0f} "
                  f"{read_symbol} {read_ratio:>6.2f}x")
        
        # Detailed breakdown
        print(f"\n{'-'*80}")
        print(f"DETAILED BREAKDOWN BY DATA COMPLEXITY")
        print(f"{'-'*80}\n")
        
        for complexity in ['simple', 'medium', 'complex']:
            print(f"\n{complexity.upper()} Data:")
            print(f"{'Engine':<20} {'Write (ops/s)':<15} {'Ratio':<10} {'Read (ops/s)':<15} {'Ratio':<10}")
            print(f"{'-'*80}")
            
            baseline_write = baseline[f'{complexity}_write']
            baseline_read = baseline[f'{complexity}_read']
            
            sorted_by_complexity = sorted(
                self.results.items(),
                key=lambda x: x[1][f'{complexity}_write'],
                reverse=True
            )
            
            for engine_name, results in sorted_by_complexity:
                write_ratio = results[f'{complexity}_write'] / baseline_write if baseline_write > 0 else 0
                read_ratio = results[f'{complexity}_read'] / baseline_read if baseline_read > 0 else 0
                
                write_symbol = '✓' if write_ratio >= 1.0 else '✗'
                read_symbol = '✓' if read_ratio >= 1.0 else '✗'
                
                print(f"{engine_name:<20} "
                      f"{results[f'{complexity}_write']:>13.0f} "
                      f"{write_symbol} {write_ratio:>6.2f}x "
                      f"{results[f'{complexity}_read']:>13.0f} "
                      f"{read_symbol} {read_ratio:>6.2f}x")
        
        print(f"\n{'-'*80}")
        print(f"LEGEND:")
        print(f"  ✓ = Performance >= baseline")
        print(f"  ✗ = Performance < baseline")
        print(f"  Ratio = Performance relative to {baseline_name}")
        print(f"{'-'*80}")
        
        # Save to JSON
        self.save_json_report()
    
    def save_json_report(self, filename: str = 'performance_report.json'):
        """Save detailed results to JSON file"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'test_configuration': {
                'simple_data_count': 4000,
                'medium_data_count': 900,
                'complex_data_count': 100,
                'total_count': 5000
            },
            'results': self.results
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\nDetailed results saved to: {filename}")


def test_performance_all_engines():
    """Run performance tests on all available engines"""
    perf = PerformanceTest()
    
    print("\n" + "="*80)
    print("COMPREHENSIVE PERFORMANCE TEST")
    print("Testing: 4000 simple + 900 medium + 100 complex = 5000 records")
    print("="*80)
    
    available_engines = get_available_engines()
    
    for i, (engine_name, engine_class, test_file) in enumerate(available_engines, 1):
        print(f"\n[{i}/{len(available_engines)}] Testing {engine_name}...")
        try:
            engine = engine_class()
            if engine.check_available():
                perf.run_engine_test(engine_name, engine, test_file)
            else:
                print(f"{engine_name} not available, skipping")
        except Exception as e:
            print(f"{engine_name} test failed: {e}")
    
    # Print comparison report
    perf.print_comparison_report()


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--perf-only':
        print("Running performance tests only...")
        test_performance_all_engines()
    else:
        # Run functional tests
        print("Running functional tests...")
        pytest.main([__file__, '-v'])
        
        # Ask to run performance tests
        print("\n" + "="*80)
        response = input("Run performance tests? (y/n): ").strip().lower()
        if response == 'y':
            test_performance_all_engines()