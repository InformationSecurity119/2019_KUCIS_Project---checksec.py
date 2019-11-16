import csv
import json
from argparse import ArgumentParser

import magic
from tabulate import tabulate

import Analyze_ELF
import Analyze_PE


def engine(file_path):
    # analyze magic_number
    # edit - no file error
    try:
        signature = magic.from_file(file_path)
    except IOError:
        print(file_path + 'is not exist!')
        exit(0)

    if 'ELF 32-bit' in signature:
        return Analyze_ELF.analyze_ELF_32(file_path)
    elif 'ELF 64-bit' in signature:
        return Analyze_ELF.analyze_ELF_64(file_path)
    elif signature.startswith('PE32'):
        return Analyze_PE.analyze_PE(file_path)
    else:
        raise AttributeError("Not Executable File : '%s'" % file_path)


def parse_args():
    parser = ArgumentParser(
        description='Check Security of Excutables')
    g = parser.add_mutually_exclusive_group()
    g.add_argument('-c', '--csv', dest='csv', action='store_true', default=False, help='save result as csv')
    g.add_argument('-j', '--json', dest='json', action='store_true', default=False, help='save result as json')
    parser.add_argument('-o', '--os', dest='os', action='store_true', default=False, help='check os security')
    parser.add_argument('-b', '--build', dest='build', action='store_true', default=False, help='check build information')
    parser.add_argument('file_paths', metavar='file_path', nargs='+')
    return parser.parse_args()


def main():
    args = parse_args()

    os_result = {}
    if args.os:
        pass

    results_by_file = {}
    for file_path in args.file_paths:
        results = {}
        results_by_file[file_path] = results
        results['security'] = engine(file_path)
        if args.build:
            results['build'] = {}

    if args.os:
        print(
            tabulate([os_result.keys(), os_result.values()], tablefmt='plain'))
        print()

    for file_path, results in results_by_file.items():
        print('filename: %s' % file_path)
        for r in results.values():
            print(tabulate([r.keys(), r.values()], tablefmt='plain'))
        print()

    if args.csv:
        columns = ['file_path']
        for r in results.values():
            columns += r.keys()

        with open('result.csv', 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(columns)

            for file_path, results in results_by_file.items():
                values = [file_path]
                for r in results.values():
                    values += r.values()
                w.writerow(values)

    elif args.json:
        with open('result.json', 'w') as f:
            json.dump(results, f, ensure_ascii=False)


if __name__ == '__main__':
    main()
