from ConfigParser import ConfigParser
import os

__author__ = 'davedash'


def get_header():
    data = """
.. raw:: html

    <table id="myTable" class="tablesorter">
    <thead>
    <tr>
        <th>Key</th>
        <th>Company</th>
        <th>Team</th>
        <th>Female Engineers</th>
        <th>Total Engineers</th>
        <th>% Female</th>
        <th>Last Updated</th>
    </tr>
    </thead>
    <tbody>
"""
    return data


def get_footer(totals):
    return """
    </tbody>
    <tfoot>
    <tr>
        <th>TOTAL</th>
        <th></th>
        <th></th>
        <th>{totals[num_female]}</th>
        <th>{totals[total]}</th>
        <th>{percentage:.2%}</th>
        <th></th>
    </tr>
    </tfoot>
    </table>
""".format(totals=totals,
           percentage=1.0 * totals['num_female'] / totals['total'])


def get_body(parser, totals):
    data = ""
    for section in parser.sections():
        num_female = parser.getint(section, 'num_female_eng')
        total = parser.getint(section, 'num_eng')
        data += """
    <tr>
        <td>{key}</td>
        <td>{company}</td>
        <td>{team}</td>
        <td>{num_female}</td>
        <td>{total}</td>
        <td>{percentage:.2%}</td>
        <td>{last_updated}</td>
    </tr>
""".format(key=section,
           company=parser.get(section, 'company'),
           team=parser.get(section, 'team',),
           num_female=num_female,
           total=total,
           percentage=1.0 * num_female / total,
           last_updated=parser.get(section, 'last_updated'))
        totals['num_female'] += num_female
        totals['total'] += total
    return data


def main(filename=None):
    data = get_header()
    parser = ConfigParser(defaults={'team': 'N/A'})
    data_file = os.path.join(os.path.realpath(os.path.dirname(__file__)),
                             'data.txt')
    parser.read(data_file)
    totals = {'num_female': 0, 'total': 0}
    data += get_body(parser, totals)
    data += get_footer(totals)
    if filename:
        with open(filename, 'w') as f:
            f.write(data)
    else:
        print(data)


if __name__ == '__main__':
    main()
