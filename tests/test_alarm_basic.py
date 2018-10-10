import unittest
import unittest.mock as mock
import inspect
import os
import sys
import io
import logging


# try:
    # from .context import alarm  # python 3
# except Exception:
    # from context import alarm
    # package workorund ??


from context import alarm
# TODO: setup logging to file    
logging.disable(logging.CRITICAL)


class MyOutput():
    """Helper class for testing print statements"""
    def __init__(self):
        self.data = []
    
    def write(self, s):
        self.data.append(s)

    def __str__(self):
        return "".join(self.data)


class TestAlarm(unittest.TestCase):
    def setUp(self):
        # print('setUp')
        self.logPoint()
        # self.maxDiff = None
        self.directory = 'd:\mp3\podcast\Alarm' + os.sep + 'unitTest'
        # self.directory = 'd:\mp3\podcast\Alarm' + 'unitTest'
        if not os.path.isdir(self.directory):
            os.mkdir(self.directory)

        self.mp3_files = [
            'petak_19.05.2017bm.mp3',
            '2017.05.23_utorak.bm.mp3',
            '2017.05.24_sreda_24.05.2017.mp3',
            '2017.05.26_petak.bm.mp3',
            'cetvrtak_25.05.20171.mp3',
            'petak_26.05.2017bm.mp3',
            'ponedeljak_22.05.2017bm.mp3',
            'ponedeljak_29.05.2017.mp3', # no sufix after year
            'utorak_23.05.2017bm.mp3',
        ]
        self.mp3_files.sort()

        non_mp3_files = [
            'not.mp3.txt',
            'test.txt',
        ]

        for file in self.mp3_files:
            with open(self.directory + os.sep + file, 'a') as file_on_disk:
                # touch file, create empty file
                pass
        
        for file in non_mp3_files:
            with open(self.directory + os.sep + file, 'a') as file_on_disk:
                # touch file, create empty file
                pass
        
        # read mp3 files from working directory
        self.filename_objects = alarm.read_mp3_filenames(self.directory)
        # TODO: remove print, for debug
        # print('filename_objects #', len(self.filename_objects))
        self.process_new_filenames()
        
        self.expected_new_filenames = [
            '2017.05.23_utorak.bm.mp3',
            '2017.05.24_sreda_24.05.2017.mp3',
            '2017.05.26_petak.bm.mp3',
            '201.05.25_cetvrtak.71.mp3',
            '2017.05.19_petak.bm.mp3',
            '2017.05.26_petak.bm.mp3',
            '2017.05.22_ponedeljak.bm.mp3',
            '2017.05.29_ponedeljak.mp3',
            '2017.05.23_utorak.bm.mp3',
        ]
        self.expected_new_filenames.sort()
        
        self.mp3_new_files_on_disk = [
            '2017.05.23_utorak.bm.mp3',
            '2017.05.24_sreda_24.05.2017.mp3',
            '2017.05.26_petak.bm.mp3',
            '201.05.25_cetvrtak.71.mp3',
            '2017.05.19_petak.bm.mp3',
            'petak_26.05.2017bm.mp3',
            '2017.05.22_ponedeljak.bm.mp3',
            'utorak_23.05.2017bm.mp3',
            '2017.05.29_ponedeljak.mp3',
        ]
        self.mp3_new_files_on_disk.sort()
    
    def tearDown(self):
        self.logPoint()
        files = os.listdir(self.directory)
        for file in files:
            os.remove(self.directory + os.sep + file)
        os.rmdir(self.directory)

    def logPoint(self):
        return  # not using currently
        currentTest = self.id().split('.')[-1]
        callingFunction = inspect.stack()[1][3]
        print('in {0} - {1}()'.format(currentTest, callingFunction))

    def get_old_filenames(self):
        """extract old filenames as string from filenameObjects """
        files = []
        for file in self.filename_objects:
            files.append(file.get_old())
        files.sort()
        return files

    def get_new_filenames(self):
        """extract new filenames as string from filenameObjects """
        files = []
        for file in self.filename_objects:
            files.append(file.get_new())
        files.sort()
        return files

    def process_new_filenames(self):
        """execute adding new filename in filenameObjects """
        for file in self.filename_objects:
            alarm.new_mp3_filename(file)
        return None

    def test_read_mp3_filenames(self):
        expected = self.mp3_files[:]
        test = self.get_old_filenames()
        self.assertEqual(test, expected)

    def test_new_mp3_filename(self):
        for item in self.filename_objects:
            if item.get_old() == 'petak_19.05.2017bm.mp3':
                self.assertEqual(item.get_new(), '2017.05.19_petak.bm.mp3')
                break
        else:
            self.assertTrue(False)

    def test_new_mp3_filenames(self):
        # process new filenames 
        expected = self.expected_new_filenames
        alarm.new_mp3_filenames(self.filename_objects)
        test = self.get_new_filenames()
        self.assertEqual(expected, test)

    def test_rename_mp3_filenames(self):
        alarm.rename_mp3_filenames(self.filename_objects, self.directory)
        expected = self.mp3_new_files_on_disk
        self.filename_objects = alarm.read_mp3_filenames(self.directory)
        test = self.get_old_filenames()
        self.assertEqual(expected, test)
        

class TestAppConfig(unittest.TestCase):
    def setUp(self):
        self.create_configuration_file()

    def tearDown(self):
        # self.delete_configuration_file()
        pass

    def create_configuration_file(self):
        configuration = [
        '<?xml version="1.0" ?>',
        '<root>',
        '    <config>',
        '        <directory>setting1</directory>',
        '        <directoryMonth>setting2</directoryMonth>',
        '        <weekdays>',
        '            <weekday>setting3</weekday>',
        '            <weekday>setting4</weekday>',
        '        </weekdays>',
        '    </config>',
        '</root>',
        '',
        ]
        self.config_filename = 'test_config.xml'
        
        with open(self.config_filename, 'w') as config_file:
            config_file.write('\n'.join(configuration))

    def load_txt_file(self, filename):
        with open(filename, 'r') as config_file:
            return config_file.read()
        
    def delete_configuration_file(self):
        os.remove(self.config_filename)

    def test_config_string(self):
        test_conf = alarm.AppConfig(self.config_filename)
        self.assertEqual(
            str(test_conf),
            ' Configuration loaded from ' + self.config_filename
       )

    def test_config_repr(self):
        test_conf = alarm.AppConfig(self.config_filename)
        self.assertEqual(repr(test_conf), 'AppConfig(test_config.xml)')

    def test_config_directory_exists(self):
        test_conf = alarm.AppConfig(self.config_filename)
        self.assertIn('directory', test_conf.configuration)

    def test_config_directory(self):
        test_conf = alarm.AppConfig(self.config_filename)
        self.assertEqual(test_conf.configuration['directory'], 'setting1')

    def test_config_directory_month_exists(self):
        test_conf = alarm.AppConfig(self.config_filename)
        self.assertIn('directoryMonth', test_conf.configuration)

    def test_config_directory_month(self):
        test_conf = alarm.AppConfig(self.config_filename)
        self.assertEqual(test_conf.configuration['directoryMonth'], 'setting2')

    def test_config_weekdays_exists(self):
        test_conf = alarm.AppConfig(self.config_filename)
        self.assertIn('weekdays', test_conf.configuration)

    def test_config_weekdays(self):
        test_conf = alarm.AppConfig(self.config_filename)
        self.assertEqual(
            test_conf.configuration['weekdays'],
            ['setting3', 'setting4']
        )

    def test_set_config(self):
        test_conf = alarm.AppConfig(self.config_filename)
        # TODO: add support for setting and writing config
        self.assertIsNone(
            test_conf.set_config({'itemA': 'settingA', 'itemB': 'settingB'})
        )

    def test_config_get(self):
        test_conf = alarm.AppConfig(self.config_filename)
        expected = {
            'directory': 'setting1',
            'directoryMonth': 'setting2',
            'weekdays': ['setting3', 'setting4'],
        }
        self.assertEqual(test_conf.get_config(), expected)

    def test_config_default(self):
        test_conf = alarm.AppConfig(self.config_filename)
        test_conf.default_config()
        self.assertEqual(
            test_conf.configuration['weekdays'],
            ['ponedeljak', 'utorak', 'sreda', 'cetvrtak', 'petak']
        )
        self.assertEqual(test_conf.configuration['loglevel'],  'INFO')
        self.assertEqual(
            test_conf.configuration['directory'],
            'd:\mp3\podcast\Alarm'
        )
        self.assertEqual(test_conf.configuration['directoryMonth'], '201708')

    def test_config_print(self):
        expected = [
            'directory: setting1',
            'directoryMonth: setting2',
            'weekdays: [\'setting3\', \'setting4\']',
            '',
            ]
        expected = "\n".join(expected)
        test_conf = alarm.AppConfig(self.config_filename)
        
        # backup stdout
        stdout_org = sys.stdout
        # create fake stdout
        my_stdout = MyOutput()
        try:
            # redirect output
            sys.stdout = my_stdout
            # capture print() in fake stdout
            test_conf.print_config()
        except Exception:
            raise Exception
        finally:
            # reset output
            sys.stdout = stdout_org
        self.assertEqual(str(my_stdout), expected)

    def test_write_config_xml(self):
        # Load config file, write under different name and compare them as strings
        test_configuration = alarm.AppConfig(self.config_filename)
        # save original config filename
        config_filename_original = self.config_filename
        test_configuration.config_filename = 'test_config_write.xml'
        # write second config file
        test_configuration.write_config_xml()
        test = self.load_txt_file(self.config_filename)
        expected = self.load_txt_file(config_filename_original)
        self.assertEqual(test, expected)
        # delete econd config file
        self.delete_configuration_file()
        # restore original config file name for tearDown() removal
        self.config_filename = config_filename_original

    def test_write_config(self):
        #Load config file, write under different name and compare them as strings
        test_configuration = alarm.AppConfig(self.config_filename)
        # save original config filename
        config_filename_original = self.config_filename
        test_configuration.config_filename = 'test_config_write.xml'
        # write second config file
        test_configuration.write_config()
        test = self.load_txt_file(self.config_filename)
        expected = self.load_txt_file(config_filename_original)
        self.assertEqual(test, expected)
        # delete econd config file
        self.delete_configuration_file()
        # restore original config file name for tearDown() removal
        self.config_filename = config_filename_original


class TestFilenameOldNew(unittest.TestCase):
    def setUp(self):
        self.old = 'old_test'
        self.new = ''
        
    def test_filenameoldnew_empty_string(self):
        expected = '{0} ---> {1}'.format(self.old, self.new)
        test = alarm.FilenameOldNew(self.old)
        self.assertEqual(str(test), expected)

    def test_filenameoldnew_set_old_string(self):
        old_2 = 'old_test2'
        expected = '{0} ---> {1}'.format(old_2, self.new)
        test = alarm.FilenameOldNew(self.old)
        test.set_old(old_2)
        self.assertEqual(str(test), expected)

    def test_filenameoldnew_set_new_string(self):
        self.new = 'new_test'
        expected = '{0} ---> {1}'.format(self.old, self.new)
        test = alarm.FilenameOldNew(self.old)
        test.set_new(self.new)
        self.assertEqual(str(test), expected)

    def test_filenameoldnew_repr(self):
        expected = 'FilenameOldNew({0})'.format(self.old)
        test = alarm.FilenameOldNew(self.old)
        self.assertEqual(repr(test), expected)

class TestMain(unittest.TestCase):
    def setUp(self):
        help_expected = [
            'alarm.py [-c]',
            'Rename alarm podcast mp3 files',
            '-c             console mode',
            '-h or --help   this help message',
            '', # original print adds last \n
        ]
        self.help_expected = '\n'.join(help_expected)

    def test_main_gui(self):
        # Create a mock alarm.main_gui.
        with mock.patch('alarm.main_gui') as main_gui:

            # When called, it will return this value:
            fake_result = 'main_gui(): Fake success'
            main_gui.return_value = fake_result

            # Run the test!
            backup_config_file = alarm.CONFIG_FILE
            alarm.CONFIG_FILE = 'test_main_config.xml'
            test = alarm.main(['alarm.py'])
            self.assertEqual(test, 'main_gui(): Fake success')

            # We can ask the mock what its arguments were.
            alarm.CONFIG_FILE = backup_config_file

    def test_main_console(self):
        # Create a mock alarm.main_console.
        with mock.patch('alarm.main_console') as main_console:

            # When called, it will return this value:
            fake_result = 'main_console(): Fake success'
            main_console.return_value = fake_result

            # Run the test!
            backup_config_file = alarm.CONFIG_FILE
            alarm.CONFIG_FILE = 'test_main_config.xml'
            test = alarm.main(['alarm.py', '-c'])
            self.assertEqual(test, 'main_console(): Fake success')

            # We can ask the mock what its arguments were.
            alarm.CONFIG_FILE = backup_config_file
            
    def test_main_help_msg1(self):
        # backup config file
        backup_config_file = alarm.CONFIG_FILE
        alarm.CONFIG_FILE = 'test_main_config.xml'

        # backup stdout
        stdout_org = sys.stdout
        # create fake stdout
        my_stdout = MyOutput()
        try:
            # redirect output
            sys.stdout = my_stdout
            # capture print() in fake stdout
            test = alarm.main(['alarm.py', '-h'])
        except Exception:
            raise Exception
        finally:
            # reset output
            sys.stdout = stdout_org
            # reset config_file
            alarm.CONFIG_FILE = backup_config_file
        # Test main return
        self.assertEqual(test, 0)
        # Test print message
        self.assertMultiLineEqual(str(my_stdout), self.help_expected)

    def test_main_help_msg2(self):
        # backup config file
        backup_config_file = alarm.CONFIG_FILE
        alarm.CONFIG_FILE = 'test_main_config.xml'
        # backup stdout
        stdout_org = sys.stdout
        # create fake stdout
        my_stdout = MyOutput()
        try:
            # redirect output
            sys.stdout = my_stdout
            # capture print() in fake stdout
            test = alarm.main(['alarm.py', '--help'])
        except Exception:
            raise Exception
        finally:
            # reset output
            sys.stdout = stdout_org
            # reset config_file
            alarm.CONFIG_FILE = backup_config_file
        # Test main return
        self.assertEqual(test, 0)
        # Test print message
        self.assertMultiLineEqual(str(my_stdout), self.help_expected)

    def test_main_invalid_argument(self):
        # backup config file
        backup_config_file = alarm.CONFIG_FILE
        alarm.CONFIG_FILE = 'test_main_config.xml'
        arg_test = '42'
        # backup stdout
        stdout_org = sys.stdout
        # create fake stdout
        my_stdout = MyOutput()
        try:
            # redirect output
            sys.stdout = my_stdout
            # capture print() in fake stdout
            test = alarm.main(['alarm.py', arg_test])
        except Exception:
            raise Exception
        finally:
            # reset output
            sys.stdout = stdout_org
            # reset config_file
            alarm.CONFIG_FILE = backup_config_file
        # Test main return
        self.assertEqual(test, 1)
        # Test print message
        error_expected = [
            'Unknown argument(s): ' + arg_test,
            '', # original print adds last \n
        ]
        error_expected = '\n'.join(error_expected)
        expected = self.help_expected + error_expected
        self.assertMultiLineEqual(str(my_stdout), expected)


if __name__ == '__main__':
    unittest.main()
