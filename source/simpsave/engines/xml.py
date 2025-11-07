"""
@file xml.py
@author WaterRun
@version 10
@date 2025-11-07
@description XML engine for SimpSave
"""

import os
import re
import xml.etree.ElementTree as ET
from xml.dom import minidom
from .base import BaseEngine
from ..utils import validate_basic_type, ensure_file_exists, serialize_value, deserialize_value


class XmlEngine(BaseEngine):
    r"""
    XML Engine
    """

    @classmethod
    def check_available(cls) -> bool:
        return True  # xml.etree.ElementTree is in standard library

    @classmethod
    def get_default_suffix(cls) -> str:
        return '.xml'

    def _load_xml(self, file: str) -> ET.Element:
        r"""
        Load the XML file
        :param file: Path to the XML file
        :return: Root element
        """
        if not os.path.isfile(file):
            raise FileNotFoundError(f'The specified .xml file does not exist: {file}')
        
        tree = ET.parse(file)
        return tree.getroot()

    def _dump_xml(self, root: ET.Element, file: str) -> None:
        r"""
        Dump XML tree to file
        :param root: Root element
        :param file: File path
        """
        xml_str = ET.tostring(root, encoding='unicode')
        dom = minidom.parseString(xml_str)
        pretty_xml = dom.toprettyxml(indent='  ', encoding='utf-8')
        
        with open(file, 'wb') as f:
            f.write(pretty_xml)

    def _find_entry(self, root: ET.Element, key: str) -> ET.Element:
        r"""
        Find entry element by key
        :param root: Root element
        :param key: Key to find
        :return: Entry element or None
        """
        for entry in root.findall('entry'):
            if entry.get('key') == key:
                return entry
        return None

    def write(self, key: str, value: any, file: str) -> bool:
        validate_basic_type(value)
        value_type = type(value).__name__
        ensure_file_exists(file)

        try:
            root = None
            if os.path.exists(file) and os.path.getsize(file) > 0:
                try:
                    root = self._load_xml(file)
                except Exception:
                    pass
            
            if root is None:
                root = ET.Element('simpsave')

            value = serialize_value(value)
            
            entry = self._find_entry(root, key)
            if entry is None:
                entry = ET.SubElement(root, 'entry')
                entry.set('key', key)
            
            entry.set('type', value_type)
            entry.text = str(value)
            
            self._dump_xml(root, file)
            return True
        except Exception:
            return False

    def read(self, key: str, file: str) -> any:
        root = self._load_xml(file)
        entry = self._find_entry(root, key)
        
        if entry is None:
            raise KeyError(f'Key {key} does not exist in file {file}')
        
        value_type = entry.get('type')
        value_str = entry.text or ''
        
        return deserialize_value(value_str, value_type)

    def has(self, key: str, file: str) -> bool:
        if not os.path.isfile(file):
            return False
        try:
            root = self._load_xml(file)
            entry = self._find_entry(root, key)
            return entry is not None
        except Exception:
            return False

    def remove(self, key: str, file: str) -> bool:
        if not os.path.isfile(file):
            return False
        try:
            root = self._load_xml(file)
            entry = self._find_entry(root, key)
            
            if entry is None:
                return False
            
            root.remove(entry)
            self._dump_xml(root, file)
            return True
        except Exception:
            return False

    def match(self, regex: str, file: str) -> dict:
        if not os.path.isfile(file):
            return {}
        try:
            root = self._load_xml(file)
            pattern = re.compile(regex)
            result = {}
            
            for entry in root.findall('entry'):
                k = entry.get('key', '')
                if pattern.match(k):
                    result[k] = self.read(k, file)
            
            return result
        except Exception:
            return {}

    def delete(self, file: str) -> bool:
        if not os.path.isfile(file):
            return False
        try:
            os.remove(file)
            return True
        except IOError:
            return False