#!/usr/bin/env python3
import os
import argparse
import shutil
import sys
import logging
from tempfile import NamedTemporaryFile
from minimizer import minimize
import zlib
from marshal import dumps


dry_run = False
minimize_code = False


def obfuscate(src_file, dst_file):
    logging.debug(f'obfuscating {src_file} -> {dst_file}')
    if dry_run:
        return
    with open(src_file, 'r') as infile:
        code = infile.read()
    if minimize_code:
        logging.debug(f'minimizing {src_file}')
        code = minimize(code)
    level_1 = compile(code, 'level_1', 'exec')
    level_1 = dumps(level_1)
    level_2 = b'from marshal import loads\nexec(loads(%r))' % level_1
    level_2 = compile(level_2, 'level_2', 'exec')
    level_2 = dumps(level_2)
    level_3 = b'from marshal import loads\nexec(loads(%r))' % level_2
    level_3 = compile(level_3, 'level_2', 'exec')
    level_3 = dumps(level_3)
    level_4 = b'from marshal import loads\nimport zlib\nexec(loads(zlib.decompress(%r)))' % zlib.compress(level_3)
    with open(dst_file, 'wb') as outfile:
        outfile.write(level_4)


def process_file(src_file, dst_file):
    if not os.path.exists(src_file):
        raise FileNotFoundError(src_file)
    if not src_file.endswith('.py'):
        raise ValueError("Input file not .py extension!")
    out_dir = os.path.dirname(dst_file)
    if not dry_run:
        if not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)
        obfuscate(src_file, dst_file)


def process_directory(src_dir, dst_dir):
    if not os.path.exists(src_dir):
        raise FileNotFoundError(src_dir)
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir, exist_ok=True)
    if src_dir == dst_dir:
        raise ValueError("Destination path same as Source path!")
    logging.info(f'Processing {src_dir} -> {dst_dir}')
    for root, dirs, files in os.walk(src_dir):
        if not dry_run:
            for d in dirs:
                logging.debug(f'Creating directory: {d}')
                os.makedirs(os.path.join(dst_dir, d))
        for file in files:
            src = os.path.join(root, file)
            dst = os.path.join(dst_dir, file)
            if file.endswith('.py'):
                process_file(src, dst)
            else:
                logging.debug(f'copying {src} -> {dst}')
                if not dry_run:
                    shutil.copyfile(src, dst)


def main():
    parser = argparse.ArgumentParser(
        prog='obfuscate',
        description='Creates duplicated version of python directory with obfuscated code'
    )
    parser.add_argument('src', metavar='src', type=str,
                        help='path to root of python project')
    parser.add_argument('dst', metavar='dst', type=str,
                        help='directory to which project will be copied')
    parser.add_argument('-m', '--minimize', action='store_true')
    parser.add_argument('-n', '--dry-run', action='store_true')
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="count", default=1)
    args = parser.parse_args()
    args.verbose = 40 - (10 * args.verbose) if args.verbose > 0 else 0
    logging.basicConfig(level=args.verbose, format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.debug(args.__dict__)
    global dry_run
    dry_run = args.dry_run
    global minimize_code
    minimize_code = args.minimize
    if dry_run:
        logging.info("DRY RUN!!!")
    try:
        if not os.path.exists(args.src):
            raise FileNotFoundError(args.src)
        if os.path.isdir(args.src):
            process_directory(args.src, args.dst)
        else:
            process_file(args.src, args.dst)
        logging.info('Complete')
    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
