#!/usr/bin/env python
"""Renames alarm podcast mp3 files to be sorting friendly """
# TODO: GUI options, set working directory
# TODO: GUI rename checkbox

try:
    import Tkinter as tk  # Python 2
except ImportError:
    import tkinter as tk  # Python 3

import os
import sys
import logging
from xml.etree import ElementTree as ET
from xml.dom import minidom


LOG_FORMAT = '%(asctime)s  %(levelname)s  %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
LOGGER = logging.getLogger(__name__)

CONFIG_FILE = 'config.xml'


class AppConfig():
    """
    Creates configuratin data structure
    input: string, config file name in same directory
    """
    # pylint: disable-too-many-instance-attributes

    def __init__(self, config_file):
        LOGGER.debug('Initial configuration started.')
        self.config_file = config_file
        self.configuration = None
        self.configuration_list = None
        self.directory_work = None
        self.weekdays = None
        self.load_config()
        LOGGER.debug('Initial configuration finished.')

    def __str__(self):
        return ' Configuration loaded from {0}'.format(self.config_file)

    def __repr__(self):
        return str('{0}({1})'.format(
            self.__class__.__name__, self.config_file))

    def print_config(self):
        """
        Print configuration
        """
        for conf_key in self.configuration:
            print('{0}: {1}'.format(conf_key, self.configuration[conf_key]))

    def get_config(self):
        """
        output: list, configuration
        """
        return self.configuration

    def set_config(self, new_configuration):
        """Set new configuration"""
        # TODO: set_config
        pass

    def load_config(self):
        """Loads configuration to file"""
        self.load_config_xml()

    def write_config(self):
        """Writes configuration to file"""
        self.write_config_xml()

    def load_config_xml(self):
        """
        Loads configuration; config dictionary from XML self.config_file

        input: none,
        uses string, self.config_file
        dictionary, self.configuration
        list, self.configuration_list
        https://www.blog.pythonlibrary.org/2013/04/30/python-101-intro-to-xml-parsing-with-elementtree/
        """
        LOGGER.info('Loading configuration started.')
        self.configuration = {}
        # use configuration list to get ordered xml output file when saving xml
        self.configuration_list = []
        abs_file_path = os.path.abspath(os.path.join(self.config_file))
        LOGGER.info('Loading configuration file %s.', abs_file_path)
        root = ET.parse(abs_file_path)
        configtree = root.findall('config/')
        LOGGER.debug('Parsing configuration file')
        for config_node in configtree:
            LOGGER.debug('config item object %s.', config_node)
            LOGGER.debug(
                'tag %s, text %s, attribute %s.',
                config_node.tag, config_node.text, config_node.attrib)

            self.configuration[config_node.tag] = config_node.text
            self.configuration_list.append(config_node.tag)
        self.directory_work = ''.join(
            [self.configuration['directory'],
             os.sep,
             self.configuration['directoryMonth']]
        )
        LOGGER.info('Working directory set to %s.', self.directory_work)
        self.configuration['weekdays'] = []
        self.weekdays = root.findall('config/weekdays/')
        for day in self.weekdays:
            self.configuration['weekdays'].append(day.text)
            LOGGER.debug(day.text)
        LOGGER.debug('Weekdays set to %s.', self.configuration['weekdays'])
        LOGGER.info('Loading configuration finished.')

    def write_config_xml(self):
        """
        Writes configuration; config dictionary into XML self.config_file

        input: none,
        uses string, self.config_file
        dictionary, self.configuration
        list, self.configuration_list
        https://www.blog.pythonlibrary.org/2013/04/30/python-101-intro-to-xml-parsing-with-elementtree/
        """

        def prettify(elem):
            """
            Return a pretty-printed XML string for the Element.
            """
            rough_string = ET.tostring(elem, encoding='utf-8')
            reparsed = minidom.parseString(rough_string)
            return reparsed.toprettyxml(indent="\t")

        LOGGER.info('Writing configuration started.')
        root = ET.Element('root')
        config = ET.Element('config')
        root.append(config)
        for item in self.configuration_list:
            LOGGER.debug('item %s.', item)
            if item != 'weekdays':
                item_xml = ET.SubElement(config, item)
                item_xml.text = self.configuration[item]
            else:
                item_xml = ET.SubElement(config, item)
                for weekday in self.configuration['weekdays']:
                    day = ET.SubElement(item_xml, 'weekday')
                    day.text = weekday
            # item.attrib = self.configuration['configversion']

        tree = ET.ElementTree(root)
        # fix as in
        # https://everydayimlearning.blogspot.rs/2012/11/elementtree.html
        xml_string = prettify(tree.getroot())
        # replace tabs with whitespaces as prefered practice
        xml_string_spaces = xml_string.replace('\t', '    ')
        with open(self.config_file, "w") as file:
            file.write(xml_string_spaces)
        LOGGER.info('Writing configuration finished.')

    def default_config(self):
        """
        Default setup if needed
        """
        self.configuration['weekdays'] = [
            'ponedeljak',
            'utorak',
            'sreda',
            'cetvrtak',
            'petak',
        ]
        self.configuration['loglevel'] = 'INFO'
        self.configuration['directory'] = r'd:\mp3\podcast\Alarm'
        self.configuration['directoryMonth'] = '201708'


class FilenameOldNew():
    """keeps old and newfile name"""

    def __init__(self, old):
        self.old = old
        self.new = ''

    def __repr__(self):
        return str('{0}({1})'.format(self.__class__.__name__, self.old))

    def __str__(self):
        return str(self.old) + ' ---> ' + str(self.new)

    def get_old(self):
        """Return old filename """
        return self.old

    def get_new(self):
        """Return new filename """
        return self.new

    def set_old(self, text):
        """Set old filename """
        self.old = text

    def set_new(self, text):
        """Set new filename """
        self.new = text


def read_mp3_filenames(directory):
    """return list of mp3 files as FilenameOldNew objects from absolute path

    input: string, absolute path on filesystem
    output: list of strings, mp3 filenames
    """
    LOGGER.info('read_mp3_filenames() started.')
    file_names_all = os.listdir(directory)
    file_names_mp3 = []
    for filename in file_names_all:
        filename_lower = filename.lower()
        if filename_lower[-3:] == 'mp3':
            file_object = FilenameOldNew(filename)
            file_names_mp3.append(file_object)
            LOGGER.debug('%s added to mp3 list.', file_object)
        else:
            LOGGER.debug('%s is not mp3.', filename)
    processed = len(file_names_all)
    ignored = len(file_names_all) - len(file_names_mp3)
    LOGGER.info(
        'read_mp3_filenames(): %s filename(s) found, %s will be ignored.',
        processed, ignored
    )
    return file_names_mp3


def new_mp3_filename(file_name_object):
    """Create new string filename from input file name

    format YYYY.MM.DD_weekday*bm.mp3"""

    filename = file_name_object.get_old()
    LOGGER.debug('new_mp3_filename() started: %s.', filename)
    target_filename = ''
    weekdays = ['ponedeljak', 'utorak', 'sreda', 'cetvrtak', 'petak']
    for day in weekdays:
        weekday_test = filename.find(day)
        if weekday_test > 0:
            LOGGER.debug('%s already renamed to target format.', filename)
            target_filename = filename
        elif weekday_test == 0:
            LOGGER.debug('%s proccessing started.', filename)
            LOGGER.debug('filename: %s  weekday: %s.', filename, day)
            filename_temp = filename[(len(day) + 1):]
            temp_dd, temp_mm, temp_yyyy, temp_ext = filename_temp.split('.')
            if len(temp_yyyy) > 4:
                # add . at between YYYY and 'bm' string
                LOGGER.debug(
                    'Additional string present in year: %s.', temp_yyyy
                )
                temp_yyyy, temp_additional = temp_yyyy[0:-2], temp_yyyy[-2:]
            else:
                LOGGER.debug(
                    'Correct number of figures in year: %s.', temp_yyyy
                )
                temp_additional = None
            LOGGER.debug(
                'Rearanging timestamp in filename started: %s.', filename
            )
            temp_string = '_'.join([temp_dd, day])
            temp_dd = temp_string
            if temp_additional:
                temp_sufix = temp_additional + '.' + temp_ext
            else:
                temp_sufix = temp_ext
            filename_temp_list_order = [
                temp_yyyy, temp_mm,
                temp_dd,
                temp_sufix,
            ]
            target_filename = '.'.join(filename_temp_list_order)
            LOGGER.debug(
                'Rearanging timestamp in filename finished: %s.',
                target_filename
            )
        elif weekday_test == -1:
            LOGGER.debug('day %s not found in filename.', day)
    file_name_object.set_new(target_filename)


def new_mp3_filenames(file_name_objects):
    """Execute method for creating new filenames for each FilenameOldNew object

    input: list of FilenameOldNew objects
    """
    LOGGER.info('new_mp3_filenames(): started.')
    for filename in file_name_objects:
        new_mp3_filename(filename)
        LOGGER.debug('New filename: %s.', filename.get_new())
    LOGGER.info(
        'new_mp3_filenames(): %d filename(s) processed.',
        len(file_name_objects)
    )
    return None


def rename_mp3_filenames(mp3_files, input_directory):
    """Renames list of mp3 files in given directory, returns nothing.
    {weekday}_{DD}.{MM}.{YYYY}bm.mp3 -> {YYYY}.{MM}.{DD}_{weekday}.mp3
    """
    # asumed filename format, there can be problem later
    # eg. if there is weekday somewhere else than at beggining,
    # but wrong filename format
    # TODO: test for relative path, works with absolute path only
    counter = len(mp3_files)
    LOGGER.info('rename_mp3_filenames() started.')
    LOGGER.debug(input_directory)
    for file_name_object in mp3_files:
        old = file_name_object.get_old()
        new = file_name_object.get_new()
        if not os.path.isfile(input_directory + os.sep + new):
            LOGGER.debug('Target filename %s not found, go for rename.', new)
            LOGGER.debug('%s, %s', old, new)
            # rename file
            os.rename(
                input_directory + os.sep + old,
                input_directory + os.sep + new
            )
            LOGGER.debug('%s renamed to %s.', old, new)
        else:
            LOGGER.warning('%s skipped, already exists.', old)
            counter -= 1
    LOGGER.info('rename_mp3_filenames(): %d processed', counter)


class SimpleappTK(tk.Tk):
    """GUI

    input:  parent object
            config: dictionary
    """
    def __init__(self, parent, config):
        """Initial TK setup"""
        tk.Tk.__init__(self, parent)
        self.parent = parent
        self.config = config
        self.initialize()

    def initialize(self):
        """Setup GUI"""
        self.grid()
        column_ui = 0
        row_ui = 0
        # Label: original filenames column
        self.label_old_name = tk.StringVar()
        self.label_old_name.set('Old mp3 filenames')
        label_old_names = tk.Label(
            self,
            textvariable=self.label_old_name,
            anchor="w"
        )
        label_old_names.grid(column=column_ui, row=row_ui, sticky='EW')
        # Label: new filenames column
        self.label_new_name = tk.StringVar()
        self.label_new_name.set('New mp3 filenames')
        label_new_names = tk.Label(self, textvariable=self.label_new_name,
                                   anchor="w", fg="white", bg="blue")
        label_new_names.grid(column=column_ui + 1, row=row_ui, sticky='EW')
        row_ui = 1
        self.mp3_file_objects = read_mp3_filenames(self.config.directory_work)
        new_mp3_filenames(self.mp3_file_objects)
        # populate columns for old and new filenames
        for mp3_file_object in self.mp3_file_objects:
            LOGGER.debug(
                'GUI: mp3 file old name: %s', mp3_file_object.get_old()
            )
            self.label_old_mp3_filename = tk.StringVar()
            self.label_old_mp3_filename.set(mp3_file_object.get_old())
            label_old_mp3_filename = tk.Label(
                self,
                textvariable=self.label_old_mp3_filename,
                anchor="w"
            )
            label_old_mp3_filename.grid(
                column=column_ui,
                row=row_ui,
                sticky='EW'
            )
            LOGGER.debug(
                'GUI: mp3 file new name: %s', mp3_file_object.get_new()
            )
            if mp3_file_object.get_new() == mp3_file_object.get_old():
                # use default colors if there is no need to rename files
                fg_color = 'black'
                bg_color = 'SystemMenu'
            else:
                # use special colors to mark files that need to be renamed
                fg_color = 'white'
                bg_color = 'blue'
            self.label_new_mp3_filename = tk.StringVar()
            self.label_new_mp3_filename.set(mp3_file_object.get_new())
            label_new_mp3_filename = tk.Label(
                self, textvariable=self.label_new_mp3_filename,
                anchor="w",
                fg=fg_color,
                bg=bg_color
            )
            label_new_mp3_filename.grid(
                column=column_ui + 1,
                row=row_ui,
                sticky='EW'
            )
            row_ui = row_ui + 1
        # Command buttons on bottom
        column_ui = 0
        button_refresh = tk.Button(
            self,
            text=u"Refresh",
            command=self.on_button_refresh_click
        )
        button_refresh.grid(column=column_ui, row=row_ui)
        button_rename = tk.Button(
            self,
            text=u"Rename",
            command=self.on_button_rename_click
        )
        button_rename.grid(column=column_ui + 1, row=row_ui)
        button_exit = tk.Button(
            self,
            text=u"Exit",
            command=self.on_button_exit_click
        )
        button_exit.grid(column=column_ui + 2, row=row_ui)
        button_write_config = tk.Button(
            self,
            text=u"Write Config",
            command=self.on_button_write_config_click
        )
        button_write_config.grid(column=column_ui + 3, row=row_ui)
        # UI Grid configuration
        self.grid_columnconfigure(0, weight=1)

    def on_button_refresh_click(self):
        """Calls for repopulation of columns"""
        LOGGER.info('GUI: refresh GUI and mp3 files list.')
        self.initialize()

    def on_button_rename_click(self):
        """Calls execution of rename function"""
        LOGGER.info('GUI: Rename mp3 files.')
        rename_mp3_filenames(self.mp3_file_objects, self.config.directory_work)
        self.on_button_refresh_click()

    def on_button_exit_click(self):
        """Calls End program"""
        LOGGER.info('GUI: Exiting program.')
        self.destroy()

    def on_button_write_config_click(self):
        """Writes configuration to file by calling AppConfig.write_config()"""
        LOGGER.info('GUI: writing configuration started.')
        self.config.write_config()
        LOGGER.info('GUI: writing configuration finished.')


def main_gui(config):
    """Start gui part"""
    print('Start GUI')
    app = SimpleappTK(None, config)
    app.title('Alarm mp3 files renamer')
    app.mainloop()
    return 0

def main_console(config):
    """Start CLI part"""
    print('Start Console')
    LOGGER.info('Start.')
    mp3_files = read_mp3_filenames(config.directory_work)
    new_mp3_filenames(mp3_files)
    rename_mp3_filenames(mp3_files, config.directory_work)
    LOGGER.info('Finished.')
    return 0

def main(args):
    """main part"""
    LOGGER.info('Arguments: %s.', *args)
    # print(CONFIG_FILE)
    configuration = AppConfig(CONFIG_FILE)
    if len(args) > 1:
        help_msg = [
            'alarm.py [-c]',
            'Rename alarm podcast mp3 files',
            '-c             console mode',
            '-h or --help   this help message',
        ]
        help_msg = '\n'.join(help_msg)
        if args[1] == '-c':
            return main_console(configuration)
        elif args[1] == '-h' or args[1] == '--help':
            print(help_msg)
            return 0
        else:
            print(help_msg)
            error_msg = 'Unknown argument(s): ' + ' '.join(args[1:])
            print(error_msg)
            return 1
    else:
        return main_gui(configuration)


if __name__ == '__main__': # pragma: no cover
    sys.exit(main(sys.argv))
