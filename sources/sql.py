#! /usr/bin/python
# SQL driver

__author__ = 'Evgeniy Yakovenko'
__version__ = 'v.0.0.1'

import os
import pymssql
import configparser
from sources.func import check_text, get_formatted_text


class EcsHistorianDriver:
    def __init__(self):
        """Default connection settings"""
        self.__server_name = r'192.168.0.1'
        self.__server_port = 1433
        self.__user = r'TestUser'
        self.__password = '1234'
        self.__data_base_name = 'FlsHistorian'

    def __get_config(self, path):
        """Get config file"""
        config = configparser.ConfigParser()
        if os.path.exists(path):
            config.read(path)
            try:
                self.__server_name = config.get("SERVER_SETTINGS", "server_name")
                self.__server_port = int(config.get("SERVER_SETTINGS", "server_port"))
                self.__user = config.get("SERVER_SETTINGS", "user")
                self.__password = config.get("SERVER_SETTINGS", "password")
                self.__data_base_name = config.get("SERVER_SETTINGS", "data_base_name")
                return 1
            except configparser.NoSectionError or configparser.NoOptionError:
                self.__init__()
                return -1
        else:
            config.add_section("SERVER_SETTINGS")
            config.set("SERVER_SETTINGS", "server_name", self.__server_name)
            config.set("SERVER_SETTINGS", "server_port", str(self.__server_port))
            config.set("SERVER_SETTINGS", "user", self.__user)
            config.set("SERVER_SETTINGS", "password", self.__password)
            config.set("SERVER_SETTINGS", "data_base_name", self.__data_base_name)

            with open(path, "w") as config_file:
                config.write(config_file)
            return 0

    def __get_data_from_hist(self, query):
        """Connection to DB"""
        self.__get_config('../config.ini')
        conn = pymssql.connect(server=self.__server_name,
                               port=self.__server_port,
                               user=self.__user,
                               password=self.__password,
                               database=self.__data_base_name)
        cursor = conn.cursor()
        cursor.execute(query)  # cursor.executemany(query)
        result_request = cursor.fetchall()
        conn.commit()
        conn.close()
        return result_request

    def get_tags_list(self, tags_text):
        """Get data from ECS Historian - List of tags"""
        query = f"""
                SELECT [FlsHistorian].[dbo].[DimTagList].[ExternalDesignation]
                ,[FlsHistorian].[dbo].[DimTagList].[DescriptionDefault]
                ,[FlsHistorian].[dbo].[DimTagList].[UnitDefault]
                FROM [FlsHistorian].[dbo].[DimTagList]
                WHERE [FlsHistorian].[dbo].[DimTagList].[ExternalDesignation] 
                IN ({get_formatted_text(tags_text)});"""
        return self.__get_data_from_hist(query)

    def get_tags_hist_value(self, tag_list, start_time, end_time):
        """Get data from ECS Historian - List of tags with historian values"""
        if check_text(tag_list):
            query = f"""
                    SELECT [FlsHistorian].[dbo].[FactMinute].[TimeLocal]
                    ,[FlsHistorian].[dbo].[DimTagList].[ExternalDesignation]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value00]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value01]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value02]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value03]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value04]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value05]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value06]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value07]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value08]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value09]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value10]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value11]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value12]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value13]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value14]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value15]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value16]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value17]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value18]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value19]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value20]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value21]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value22]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value23]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value24]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value25]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value26]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value27]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value28]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value29]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value30]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value31]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value32]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value33]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value34]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value35]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value36]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value37]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value38]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value39]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value40]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value41]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value42]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value43]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value44]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value45]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value46]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value47]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value48]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value49]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value50]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value51]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value52]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value53]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value54]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value55]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value56]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value57]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value58]
                    ,[FlsHistorian].[dbo].[FactMinute].[Value59]
                FROM  [FlsHistorian].[dbo].[FactMinute], [FlsHistorian].[dbo].[DimTagList]
                WHERE  [FlsHistorian].[dbo].[DimTagList].[ExternalDesignation] 
                IN  ({get_formatted_text(tag_list)})
                AND [FlsHistorian].[dbo].[DimTagList].[TagId] = [FlsHistorian].[dbo].[FactMinute].[TagId] 
                AND ([FlsHistorian].[dbo].[FactMinute].[TimeLocal] 
                BETWEEN '{start_time}' 
                AND '{end_time}');
                """
            return self.__get_data_from_hist(query)
        else:
            return None

    def get_compared_dict(self, tags_list):
        """Сompare tags list with tags in DB"""
        if tags_list != '' and check_text(tags_list):
            get_tags_in_db = self.get_tags_list(tags_list)
            compared_dict = dict()
            no_matches_in_tags_list = ''
            actual_tag_list = ''
            tags_list = get_formatted_text(tags_list).replace("'", "").split(',')

            for i in range(len(tags_list)):
                compared_dict[tags_list[i]] = False
                for j in range(len(get_tags_in_db)):
                    if tags_list[i] == get_tags_in_db[j][0]:
                        compared_dict[tags_list[i]] = True

            for key in compared_dict:
                if compared_dict[key]:
                    actual_tag_list += key + ', '
                else:
                    no_matches_in_tags_list += key + ', '

            if len(actual_tag_list) >= 2:
                actual_tag_list = actual_tag_list[:-2]

            if len(no_matches_in_tags_list) >= 2:
                no_matches_in_tags_list = no_matches_in_tags_list[:-2]

            return {'good_list_tags': actual_tag_list, 'bad_list_tags': no_matches_in_tags_list,
                    'compared_dict': compared_dict}
        else:
            return None


if __name__ == '__main__':
    pass