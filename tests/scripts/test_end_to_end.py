from tempfile import NamedTemporaryFile
import os
import pytest
import subprocess

def test_end_to_end(testpath):

    objects = 'tests/data/single/text-file.txt'
    dmd_file = 'tests/data/import_description/metadata/dc_description.xml'
    dmd_target = 'tests/data/single'
    file_to_sign = 'mets.xml'
    signature_filename = os.path.join (os.path.abspath(testpath), 'signature.sig')
    private_key = 'tests/data/rsa-keys.crt'

    environment = os.environ.copy()
    environment['PYTHONPATH'] = '.'

    command = ['python', 'siptools/scripts/import_object.py',
        '--workspace', testpath, objects, '--skip_inspection', '--format_name',
        'text/plain', '--format_version', '1.0', '--digest_algorithm', 'MD5',
        '--message_digest', '1qw87geiewgwe9', '--date_created',
        '2017-01-11T10:14:13', '--charset', 'ISO-8859-15']
    #child=subprocess.Popen(command)
    child = subprocess.Popen(command, env=environment)
    streamdata = child.communicate()[0]
    assert child.returncode == 0

    command = ['python', 'siptools/scripts/premis_event.py', 'creation',
            '2017-01-11T10:14:13', '--event_detail', 'Testing',
            '--event_outcome', 'success', '--event_outcome_detail',
            'Outcome detail', '--workspace', testpath, '--agent_name',
            'Demo Application', '--agent_type', 'software', '--event_target',
            objects]
    child = subprocess.Popen(command, env=environment)
    streamdata = child.communicate()[0]
    assert child.returncode == 0

    command = ['python', 'siptools/scripts/import_description.py', dmd_file,
            '--workspace', testpath, '--dmdsec_target', dmd_target,
            '--desc_root', 'remove']
    child = subprocess.Popen(command, env=environment)
    streamdata = child.communicate()[0]
    assert child.returncode == 0

    command = ['python', 'siptools/scripts/compile_structmap.py',
               '--workspace', testpath]
    child = subprocess.Popen(command, env=environment)
    streamdata = child.communicate()[0]
    assert child.returncode == 0

    command = ['python', 'siptools/scripts/compile_mets.py',
            '--workspace', testpath, 'ch', 'CSC', 
            'contract-id-1234', '--create_date', '2017-01-11T10:14:13',
            '--copy_files', '--clean']
    child = subprocess.Popen(command, env=environment)
    streamdata = child.communicate()[0]
    assert child.returncode == 0

    command = ['python', 'siptools/scripts/sign_mets.py',
            file_to_sign, signature_filename, private_key]
    child = subprocess.Popen(command, env=environment)
    streamdata = child.communicate()[0]
    assert child.returncode == 0

    command = ['python', 'siptools/scripts/compress.py', 
        '--tar_filename', os.path.join(testpath, 'sip.tar'), testpath]
    child = subprocess.Popen(command, env=environment)
    streamdata = child.communicate()[0]
    assert child.returncode == 0

    command = ['check-xml-schematron-features', '-s',
            '/usr/share/dpres-xml-schemas/schematron/mets_internal.sch',
            os.path.join(testpath, file_to_sign)]
    child = subprocess.Popen(command, env=environment)
    streamdata = child.communicate()[0]
    assert child.returncode == 0

    command = ['check-xml-schematron-features', '-s',
            '/usr/share/dpres-xml-schemas/schematron/mets_premis.sch',
            os.path.join(testpath, file_to_sign)]
    child = subprocess.Popen(command, env=environment)
    streamdata = child.communicate()[0]
    assert child.returncode == 0

    command = ['check-xml-schematron-features', '-s',
            '/usr/share/dpres-xml-schemas/schematron/mets_mdtype.sch',
            os.path.join(testpath, file_to_sign)]
    child = subprocess.Popen(command, env=environment)
    streamdata = child.communicate()[0]
    assert child.returncode == 0

