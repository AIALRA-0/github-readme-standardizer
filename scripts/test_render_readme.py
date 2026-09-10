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

    def test_centered_lead_and_hero_markup_remains_intact(self):
        body = render_body(
            '<div align="center"><h1>Project</h1><p>Value</p></div>\n\n'
            '<div align="center"><img src="hero.svg" alt="Structure" /><p>Figure 1. Structure</p></div>\n'
        )
        tree = ET.fromstring('<root>' + body + '</root>')
        blocks = tree.findall('div')
        self.assertEqual(2, len(blocks))
        self.assertTrue(all(block.get('align') == 'center' for block in blocks))
        self.assertEqual('Value', blocks[0].find('p').text)
        self.assertEqual('Figure 1. Structure', blocks[1].find('p').text)

    def test_centered_table_and_title_markup_remains_intact(self):
        body = render_body(
            '<div align="center">\n\nTable 1. Results\n\n'
            '| Item | State |\n|---|---|\n| Local | Ready |\n\n</div>\n'
        )
        tree = ET.fromstring('<root>' + body + '</root>')
        block = tree.find('div')
        self.assertEqual('center', block.get('align'))
        self.assertEqual('Table 1. Results', block.find('p').text)
        self.assertEqual('Ready', block.find('./table/tbody/tr/td[2]').text)


if __name__ == '__main__':
    unittest.main()
