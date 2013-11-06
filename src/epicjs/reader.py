'''
Created on 5 lis 2013

@author: karol
'''
from collections import OrderedDict
from epicjs.entity.koans import Koan
from epicjs.dao.koans import Meditation


def parse_meditation(lines):
    lines = [l for l in lines if l.strip() if l.strip()]
    title_line = lines[0]
    rest = lines[1:]
    slug, title = title_line.replace('//', '').strip().split('|')
    koans = OrderedDict()
    current = None
    comment_bracket_cnt = 0
    for line in rest:
        if line.strip().startswith('//'):
            current = line.replace('//', '').strip()
            koans[current] = {
                'hint': [],
                'code': [],
                'slug': current.split('|')[0],
                'name': current.split('|')[1]
            }
        elif line.strip().startswith('/*'):
            koans[current]['hint'].append(line)
            comment_bracket_cnt += 1
        elif line.strip().startswith('*/'):
            koans[current]['hint'].append(line)
            comment_bracket_cnt -= 1
        else:
            if comment_bracket_cnt != 0:
                koans[current]['hint'].append(line)
            else:
                koans[current]['code'].append(line)
    
    for koan in koans.values():
        koan['hint'] = "\n".join(koan['hint'])
        koan['code'] = '\n'.join(koan['code'])

    
    ks = [Koan(k['slug'], k['name'], k['hint'], k['code']) for k in koans.values()]  
    m = Meditation(slug, title)
    for k in ks: m.add_koan(k)
    return m         