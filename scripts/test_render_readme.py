"""Check the preview behaviors that previously diverged from repository rendering."""
import unittest
import xml.etree.ElementTree as ET

from render_readme import render_body


class RenderTests(unittest.TestCase):
    def test_two_space_children_stay_with_their_parent(self):
        body = render_body('- Success\n\n  - Read warnings\n  - Check facts\n- Failure\n\n  1. Locate\n  2. Repair\n- Next\n')
        tree = ET.fromstring('<root>' + body + '</root>')
        parents = tree.findall('./ul/li')
        self.assertEqual(3, len(parents))
        self.assertEqual(2, len(parents[0].findall('./ul/li')))
        self.assertEqual(2, len(parents[1].findall('./ol/li')))

    def test_chinese_and_duplicate_anchors(self):
        body = render_body('## 2. 开始使用\n\n## 2. 开始使用\n')
        tree = ET.fromstring('<root>' + body + '</root>')
        self.assertEqual(['2-开始使用', '2-开始使用-1'], [node.get('id') for node in tree])

    def test_raw_title_and_tables_remain_rendered(self):
        body = render_body('<h1 align="center">Project</h1>\n\n| Item | State |\n|---|---|\n| Local | Ready |\n')
        tree = ET.fromstring('<root>' + body + '</root>')
        self.assertEqual('center', tree.find('h1').get('align'))
        self.assertEqual('Ready', tree.find('./table/tbody/tr/td[2]').text)


if __name__ == '__main__':
    unittest.main()
